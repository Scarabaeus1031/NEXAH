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

        # normalize
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
            score = changes / max(1, len(segment)-1)
            scores.append(score)
        return scores

    # --- Navigation 1: Probabilistic (escape) ---
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

    # --- Navigation 2: Graph shortest path (BFS) ---
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

        return None  # no path found

    # --- Main API ---
    def analyze(self, trajectory, target_state=None):
        trajectory = np.array(trajectory)

        # 1. Representation
        states = self._embed(trajectory)

        # 2. Structure
        kmeans = KMeans(n_clusters=self.n_clusters, n_init=10)
        labels = kmeans.fit_predict(states)

        # 3. Transitions
        transitions = self._compute_transitions(labels)

        # 4. Current / next
        current = labels[-1]
        next_state = (
            max(transitions[current], key=transitions[current].get)
            if current in transitions else None
        )

        # 5. Stability
        stable_states = self._detect_stable_states(transitions)

        # 6. Regime shifts
        regime_shifts = self._detect_regime_shifts(labels)

        # 7. Instability
        instability = self._instability_score(labels)

        # 8. Navigation
        path_prob = None
        path_bfs = None

        if target_state is not None:
            path_prob = self._navigate_probabilistic(
                transitions, current, target_state
            )
            path_bfs = self._find_path_bfs(
                transitions, current, target_state
            )

        return {
            "states": states,
            "labels": labels,
            "transitions": transitions,
            "current_state": int(current),
            "next_state": None if next_state is None else int(next_state),
            "stable_states": stable_states,
            "regime_shifts": regime_shifts,
            "instability": instability,
            "path_probabilistic": path_prob,
            "path_bfs": path_bfs
        }


# --- Example ---
if __name__ == "__main__":
    traj = np.sin(np.linspace(0, 20, 200))

    nx = NEXAH(n_clusters=3, window=10)
    result = nx.analyze(traj, target_state=0)

    print("Current:", result["current_state"])
    print("Next:", result["next_state"])
    print("Stable:", result["stable_states"])
    print("Shifts:", result["regime_shifts"][:10], "...")
    print()

    print("Probabilistic path:", result["path_probabilistic"])
    print("Shortest path (BFS):", result["path_bfs"])
    print()

    print("Transitions:")
    for k, v in result["transitions"].items():
        print(f"{k} -> {v}")
