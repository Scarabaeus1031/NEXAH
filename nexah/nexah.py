import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict, deque
import random


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

            score = changes / max(1, len(segment)-1)
            scores.append(score)

        return scores

    # --- Escape Difficulty ---
    def _escape_difficulty(self, transitions):
        difficulty = {}

        for s in transitions:
            stay_prob = transitions[s].get(s, 0.0)
            difficulty[s] = stay_prob

        return difficulty

    # --- State Scores ---
    def _score_states(self, transitions):
        scores = {}

        for s in transitions:
            stay_prob = transitions[s].get(s, 0.0)
            outgoing = 1.0 - stay_prob

            # simple v0 score:
            # high stability is good,
            # but too much lock-in slightly reduces flexibility
            scores[s] = stay_prob - 0.25 * outgoing

        return scores

    # --- Best State ---
    def _best_state(self, state_scores):
        if not state_scores:
            return None
        return max(state_scores, key=state_scores.get)

    # --- Minimal Intervention ---
    def _minimal_intervention(self, transitions, start, target):
        if start == target:
            return {
                "needed": False,
                "reason": "already_at_target",
                "cost": 0.0
            }

        if start not in transitions:
            return {
                "needed": True,
                "reason": "no_outgoing_transitions",
                "cost": None
            }

        prob = transitions[start].get(target, 0.0)

        if prob > 0:
            return {
                "needed": True,
                "reason": "direct_transition_exists",
                "transition_probability": prob,
                "cost": 1.0 - prob
            }

        return {
            "needed": True,
            "reason": "no_direct_transition",
            "transition_probability": 0.0,
            "cost": 1.0
        }

    # --- Navigation 1: Probabilistic ---
    def _navigate_probabilistic(self, transitions, start, target, max_steps=20):
        path = [start]
        current = start

        for _ in range(max_steps):
            if current == target:
                break

            if current not in transitions:
                break

            next_states = list(transitions[current].keys())
            probs = list(transitions[current].values())

            next_state = random.choices(next_states, weights=probs)[0]

            path.append(next_state)
            current = next_state

        return path

    # --- Navigation 2: BFS ---
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

            if node in transitions:
                for neighbor in transitions[node]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return None

    # --- Main API ---
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

        stable_states = self._detect_stable_states(transitions)
        regime_shifts = self._detect_regime_shifts(labels)
        instability = self._instability_score(labels)

        escape_difficulty = self._escape_difficulty(transitions)
        state_scores = self._score_states(transitions)
        best_state = self._best_state(state_scores)

        path_prob = None
        path_bfs = None
        minimal_intervention = None

        if target_state is not None:
            path_prob = self._navigate_probabilistic(
                transitions, current, target_state
            )
            path_bfs = self._find_path_bfs(
                transitions, current, target_state
            )
            minimal_intervention = self._minimal_intervention(
                transitions, current, target_state
            )

        return {
            "states": states,
            "labels": labels,
            "transitions": transitions,
            "current_state": current,
            "next_state": None if next_state is None else int(next_state),
            "stable_states": stable_states,
            "regime_shifts": regime_shifts,
            "instability": instability,
            "escape_difficulty": escape_difficulty,
            "state_scores": state_scores,
            "best_state": None if best_state is None else int(best_state),
            "path_probabilistic": path_prob,
            "path_bfs": path_bfs,
            "minimal_intervention": minimal_intervention
        }


# --- Example ---
if __name__ == "__main__":
    traj = np.sin(np.linspace(0, 20, 200))

    nx = NEXAH(n_clusters=3, window=10)
    result = nx.analyze(traj, target_state=0)

    print("Current:", result["current_state"])
    print("Next:", result["next_state"])
    print("Best state:", result["best_state"])
    print("Stable:", result["stable_states"])
    print("Shifts:", result["regime_shifts"][:10], "...")
    print()

    print("Escape difficulty:")
    for k, v in result["escape_difficulty"].items():
        print(f"{k}: {v:.3f}")

    print()
    print("State scores:")
    for k, v in result["state_scores"].items():
        print(f"{k}: {v:.3f}")

    print()
    print("Probabilistic path:", result["path_probabilistic"])
    print("Shortest path (BFS):", result["path_bfs"])
    print("Minimal intervention:", result["minimal_intervention"])

    print()
    print("Transitions:")
    for k, v in result["transitions"].items():
        print(f"{k} -> {v}")
