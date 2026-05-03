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

        if trajectory.ndim == 1:
            trajectory = trajectory.reshape(-1, 1)

        if self.normalize:
            mean = np.mean(trajectory, axis=0)
            std = np.std(trajectory, axis=0) + 1e-8
            trajectory = (trajectory - mean) / std

        return trajectory

    # --- Representation ---
    def _embed(self, trajectory):
        T, D = trajectory.shape

        return np.array([
            trajectory[i:i+self.window].flatten()
            for i in range(T - self.window)
        ])

    # --- Structure ---
    def _compute_transitions(self, labels):
        T = defaultdict(lambda: defaultdict(int))

        for i in range(len(labels) - 1):
            a, b = int(labels[i]), int(labels[i+1])
            T[a][b] += 1

        P = {}
        for a in T:
            total = sum(T[a].values())
            P[a] = {b: T[a][b] / total for b in T[a]}

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

    # --- Entropy ---
    def _transition_entropy(self, transitions):
        entropies = {}

        for s, probs in transitions.items():
            values = np.array(list(probs.values()))
            entropy = -np.sum(values * np.log(values + 1e-12))
            entropies[s] = float(entropy)

        return entropies

    # --- Signature ---
    def _state_signature(self, labels, transitions):
        state_counts = defaultdict(int)

        for label in labels:
            state_counts[int(label)] += 1

        total = len(labels)
        occupancy = {
            s: count / total
            for s, count in state_counts.items()
        }

        escape = self._escape_difficulty(transitions)
        entropy = self._transition_entropy(transitions)

        dominant_state = max(occupancy, key=occupancy.get)

        return {
            "n_states_observed": len(state_counts),
            "dominant_state": int(dominant_state),
            "occupancy": occupancy,
            "escape_difficulty": escape,
            "transition_entropy": entropy
        }

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

    # --- Minimal Intervention ---
    def _minimal_intervention(self, transitions, start, target):
        path = self._find_path_bfs(transitions, start, target)

        if path is None:
            return {
                "reachable": False,
                "cost": float("inf"),
                "path": None
            }

        cost = 0.0

        for i in range(len(path) - 1):
            a, b = path[i], path[i+1]
            prob = transitions[a].get(b, 0.0)
            cost += (1.0 - prob)

        return {
            "reachable": True,
            "path": path,
            "steps": len(path) - 1,
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
            "expected_steps": (
                sum(steps_list) / len(steps_list)
                if steps_list else None
            )
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

                modified[a][b] += 0.05

                total = sum(modified[a].values())
                for k in modified[a]:
                    modified[a][k] /= total

                new = self._estimate_transition_dynamics(
                    modified, start, target
                )

                improvement = (
                    new["hit_probability"]
                    - base["hit_probability"]
                )

                if improvement > best["improvement"]:
                    best = {
                        "from": a,
                        "to": b,
                        "improvement": improvement,
                        "new_probability": new["hit_probability"]
                    }

        return best

    # --- MAIN ANALYZE ---
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

        stable_states = self._detect_stable_states(transitions)
        regime_shifts = self._detect_regime_shifts(labels)
        instability = self._instability_score(labels)
        escape_difficulty = self._escape_difficulty(transitions)
        state_scores = self._score_states(transitions)
        best_state = self._best_state(state_scores)
        signature = self._state_signature(labels, transitions)

        result = {
            "config": {
                "n_clusters": self.n_clusters,
                "window": self.window,
                "random_state": self.random_state,
                "normalize": self.normalize
            },
            "current_state": current,
            "next_state": None if next_state is None else int(next_state),
            "best_state": None if best_state is None else int(best_state),
            "stable_states": stable_states,
            "regime_shifts": regime_shifts,
            "instability": instability,
            "escape_difficulty": escape_difficulty,
            "state_scores": state_scores,
            "signature": signature,
            "transitions": transitions
        }

        if target_state is not None:
            result["path_bfs"] = self._find_path_bfs(
                transitions, current, target_state
            )
            result["path_prob"] = self._navigate_probabilistic(
                transitions, current, target_state
            )
            result["intervention"] = self._minimal_intervention(
                transitions, current, target_state
            )
            result["dynamics"] = self._estimate_transition_dynamics(
                transitions, current, target_state
            )
            result["control"] = self._optimize_transition(
                transitions, current, target_state
            )

        return result

    # --- v0.7: Analyze Many ---
    def analyze_many(self, trajectories, target_state=None):
        results = []

        for i, trajectory in enumerate(trajectories):
            result = self.analyze(
                trajectory,
                target_state=target_state
            )

            result["id"] = i
            results.append(result)

        return results

    # --- v0.7: Compare Two Trajectories ---
    def compare(self, trajectory_a, trajectory_b):
        result_a = self.analyze(trajectory_a)
        result_b = self.analyze(trajectory_b)

        sig_a = result_a["signature"]
        sig_b = result_b["signature"]

        stability_a = np.mean(list(sig_a["escape_difficulty"].values()))
        stability_b = np.mean(list(sig_b["escape_difficulty"].values()))

        entropy_a = np.mean(list(sig_a["transition_entropy"].values()))
        entropy_b = np.mean(list(sig_b["transition_entropy"].values()))

        stability_delta = abs(stability_a - stability_b)
        entropy_delta = abs(entropy_a - entropy_b)

        similarity = 1.0 / (1.0 + stability_delta + entropy_delta)

        return {
            "similarity": float(similarity),
            "stability_delta": float(stability_delta),
            "entropy_delta": float(entropy_delta),
            "a": {
                "current_state": result_a["current_state"],
                "best_state": result_a["best_state"],
                "signature": sig_a
            },
            "b": {
                "current_state": result_b["current_state"],
                "best_state": result_b["best_state"],
                "signature": sig_b
            }
        }


# --- Example ---
if __name__ == "__main__":
    traj1 = np.sin(np.linspace(0, 20, 200))
    traj2 = np.cos(np.linspace(0, 20, 200))
    traj3 = np.sin(np.linspace(0, 20, 200)) + 0.2 * np.random.randn(200)

    nx = NEXAH(n_clusters=3, window=10)

    res = nx.analyze(traj1, target_state=0)

    print("=== Single Analysis ===")
    print("Current:", res["current_state"])
    print("Best:", res["best_state"])
    print("Signature:", res["signature"])
    print("Dynamics:", res.get("dynamics"))
    print("Control:", res.get("control"))
    print()

    print("=== Batch Analysis ===")
    batch = nx.analyze_many([traj1, traj2, traj3], target_state=0)
    for item in batch:
        print(
            "ID:", item["id"],
            "Current:", item["current_state"],
            "Best:", item["best_state"],
            "Dominant:", item["signature"]["dominant_state"]
        )
    print()

    print("=== Compare ===")
    comp = nx.compare(traj1, traj2)
    print("Similarity:", comp["similarity"])
    print("Stability delta:", comp["stability_delta"])
    print("Entropy delta:", comp["entropy_delta"])
