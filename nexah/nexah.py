import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict, deque
import random
import copy


class NEXAH:

    def __init__(self, n_clusters=4, window=5):
        self.n_clusters = n_clusters
        self.window = window

    # --- Representation ---
    def _embed(self, trajectory):
        return np.array([
            trajectory[i:i+self.window]
            for i in range(len(trajectory) - self.window)
        ])

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

    # --- Stability ---
    def _detect_stable_states(self, transitions, threshold=0.9):
        return [
            s for s in transitions
            if s in transitions[s] and transitions[s][s] > threshold
        ]

    # --- Regime Shifts ---
    def _detect_regime_shifts(self, labels):
        return [
            i for i in range(1, len(labels))
            if labels[i] != labels[i-1]
        ]

    # --- Instability ---
    def _instability_score(self, labels, window=5):
        scores = []

        for i in range(len(labels)):
            segment = labels[max(0, i-window):i+1]

            changes = sum(
                1 for j in range(1, len(segment))
                if segment[j] != segment[j-1]
            )

            scores.append(changes / max(1, len(segment)-1))

        return scores

    # --- Escape Difficulty ---
    def _escape_difficulty(self, transitions):
        return {
            s: transitions[s].get(s, 0.0)
            for s in transitions
        }

    # --- State Scores ---
    def _score_states(self, transitions):
        scores = {}

        for s in transitions:
            stay = transitions[s].get(s, 0.0)
            outgoing = 1.0 - stay
            scores[s] = stay - 0.25 * outgoing

        return scores

    def _best_state(self, state_scores):
        return max(state_scores, key=state_scores.get) if state_scores else None

    # --- BFS Path ---
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

    # --- Minimal Intervention (fixed) ---
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

    # --- Control Layer ---
    def _optimize_transition(self, transitions, start, target):
        base = self._estimate_transition_dynamics(transitions, start, target)

        best = {
            "improvement": 0,
            "action": None
        }

        for a in transitions:
            for b in transitions[a]:

                modified = copy.deepcopy(transitions)

                # small push
                modified[a][b] += 0.05

                # renormalize
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
        trajectory = np.array(trajectory)

        states = self._embed(trajectory)

        kmeans = KMeans(n_clusters=self.n_clusters, n_init=10)
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
    print("Control suggestion:", res["control"])
