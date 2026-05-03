import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict, deque
import random
import copy


class NEXAH:

    def __init__(self, n_clusters=4, window=5, random_state=42, normalize=True):
        self.n_clusters = n_clusters
        self.window = window
        self.random_state = random_state
        self.normalize = normalize

        random.seed(random_state)
        np.random.seed(random_state)

    # --- Preprocessing ---
    def _preprocess(self, trajectory):
        trajectory = np.array(trajectory)

        # ensure 2D: (T,) -> (T,1)
        if trajectory.ndim == 1:
            trajectory = trajectory.reshape(-1, 1)

        # normalize
        if self.normalize:
            mean = np.mean(trajectory, axis=0)
            std = np.std(trajectory, axis=0) + 1e-8
            trajectory = (trajectory - mean) / std

        return trajectory

    # --- Representation ---
    def _embed(self, trajectory):
        T, D = trajectory.shape

        X = []
        for i in range(T - self.window):
            window_slice = trajectory[i:i+self.window].flatten()
            X.append(window_slice)

        return np.array(X)

    # --- Structure ---
    def _compute_transitions(self, labels):
        T = defaultdict(lambda: defaultdict(int))

        for i in range(len(labels) - 1):
            a, b = labels[i], labels[i+1]
            T[a][b] += 1

        P = {}
        for a in T:
            total = sum(T[a].values())
            P[a] = {b: T[a][b]/total for b in T[a]}

        return P

    # --- State Scores ---
    def _score_states(self, transitions):
        scores = {}
        for s in transitions:
            stay = transitions[s].get(s, 0.0)
            outgoing = 1.0 - stay
            scores[s] = stay - 0.25 * outgoing
        return scores

    def _best_state(self, scores):
        return max(scores, key=scores.get) if scores else None

    # --- BFS ---
    def _find_path_bfs(self, transitions, start, target):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == target:
                return path

            if node in visited:
                continue

            visited.add(node)

            for neighbor in transitions.get(node, {}):
                queue.append(path + [neighbor])

        return None

    # --- Probabilistic Navigation ---
    def _navigate_probabilistic(self, transitions, start, target, max_steps=50):
        path = [start]
        current = start

        for _ in range(max_steps):
            if current == target:
                break

            if current not in transitions:
                break

            next_states = list(transitions[current].keys())
            probs = list(transitions[current].values())

            current = random.choices(next_states, weights=probs)[0]
            path.append(current)

        return path

    # --- Transition Dynamics ---
    def _estimate_transition_dynamics(self, transitions, start, target, trials=200, max_steps=50):
        success = 0
        steps_list = []

        for _ in range(trials):
            current = start

            for step in range(max_steps):
                if current == target:
                    success += 1
                    steps_list.append(step)
                    break

                if current not in transitions:
                    break

                next_states = list(transitions[current].keys())
                probs = list(transitions[current].values())

                current = random.choices(next_states, weights=probs)[0]

        return {
            "hit_probability": success / trials,
            "expected_steps": (sum(steps_list)/len(steps_list)) if steps_list else None
        }

    # --- Minimal Intervention ---
    def _minimal_intervention(self, transitions, start, target):
        path = self._find_path_bfs(transitions, start, target)

        if path is None:
            return {"reachable": False, "cost": float("inf"), "path": None}

        cost = 0.0
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            prob = transitions[a].get(b, 0.0)
            cost += (1.0 - prob)

        return {
            "reachable": True,
            "path": path,
            "steps": len(path)-1,
            "cost": cost
        }

    # --- Control ---
    def _optimize_transition(self, transitions, start, target):
        base = self._estimate_transition_dynamics(transitions, start, target)

        best = {"improvement": 0}

        for a in transitions:
            for b in transitions[a]:

                modified = copy.deepcopy(transitions)

                modified[a][b] += 0.05

                total = sum(modified[a].values())
                for k in modified[a]:
                    modified[a][k] /= total

                new = self._estimate_transition_dynamics(modified, start, target)

                improvement = new["hit_probability"] - base["hit_probability"]

                if improvement > best["improvement"]:
                    best = {
                        "from": a,
                        "to": b,
                        "improvement": improvement,
                        "new_probability": new["hit_probability"]
                    }

        return best

    # --- MAIN ---
    def analyze(self, trajectory, target_state=None):

        trajectory = self._preprocess(trajectory)

        states = self._embed(trajectory)

        kmeans = KMeans(
            n_clusters=self.n_clusters,
            n_init=10,
            random_state=self.random_state
        )

        labels = kmeans.fit_predict(states)

        transitions = self._compute_transitions(labels)

        current = int(labels[-1])

        next_state = (
            max(transitions[current], key=transitions[current].get)
            if current in transitions else None
        )

        state_scores = self._score_states(transitions)
        best_state = self._best_state(state_scores)

        result = {
            "current_state": current,
            "next_state": next_state,
            "best_state": int(best_state),
            "transitions": transitions
        }

        if target_state is not None:
            result["path_bfs"] = self._find_path_bfs(transitions, current, target_state)
            result["path_prob"] = self._navigate_probabilistic(transitions, current, target_state)
            result["intervention"] = self._minimal_intervention(transitions, current, target_state)
            result["dynamics"] = self._estimate_transition_dynamics(transitions, current, target_state)
            result["control"] = self._optimize_transition(transitions, current, target_state)

        return result


# --- Example ---
if __name__ == "__main__":
    traj = np.sin(np.linspace(0, 20, 200))

    nx = NEXAH(n_clusters=3, window=10)
    res = nx.analyze(traj, target_state=0)

    print("Current:", res["current_state"])
    print("Best:", res["best_state"])
    print("Path:", res["path_bfs"])
    print("Dynamics:", res["dynamics"])
    print("Control:", res["control"])
