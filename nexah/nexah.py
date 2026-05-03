import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict

class NEXAH:

    def __init__(self, n_clusters=4, window=5):
        self.n_clusters = n_clusters
        self.window = window

    # --- Representation Layer ---
    def _embed(self, trajectory):
        X = []
        for i in range(len(trajectory) - self.window):
            X.append(trajectory[i:i+self.window])
        return np.array(X)

    # --- Structure Layer ---
    def _compute_transitions(self, labels):
        T = defaultdict(lambda: defaultdict(int))

        for i in range(len(labels) - 1):
            a, b = labels[i], labels[i+1]
            T[a][b] += 1

        # normalize
        P = {}
        for a in T:
            total = sum(T[a].values())
            P[a] = {b: T[a][b] / total for b in T[a]}
        return P

    # --- Stability ---
    def _detect_stable_states(self, transitions, threshold=0.9):
        stable = []
        for s in transitions:
            if s in transitions[s] and transitions[s][s] > threshold:
                stable.append(s)
        return stable

    # --- Regime Shifts ---
    def _detect_regime_shifts(self, labels):
        shifts = []
        for i in range(1, len(labels)):
            if labels[i] != labels[i-1]:
                shifts.append(i)
        return shifts

    # --- Instability Score ---
    def _instability_score(self, labels, window=5):
        scores = []
        for i in range(len(labels)):
            start = max(0, i - window)
            segment = labels[start:i+1]

            changes = 0
            for j in range(1, len(segment)):
                if segment[j] != segment[j-1]:
                    changes += 1

            score = changes / max(1, len(segment)-1)
            scores.append(score)

        return scores

    # --- Navigation: greedy next-step path ---
    def _navigate_to_target(self, transitions, start, target, max_steps=10):
        path = [start]
        current = start

        for _ in range(max_steps):
            if current == target:
                break

            if current not in transitions:
                break

            # greedy: pick most likely next
            next_state = max(transitions[current], key=transitions[current].get)
            path.append(next_state)

            if next_state == current:
                break  # stuck in stable state

            current = next_state

        return path

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
        if current in transitions:
            next_state = max(transitions[current], key=transitions[current].get)
        else:
            next_state = None

        # 5. Stability
        stable_states = self._detect_stable_states(transitions)

        # 6. Regime shifts
        regime_shifts = self._detect_regime_shifts(labels)

        # 7. Instability
        instability = self._instability_score(labels)

        # 8. Navigation (optional)
        path = None
        if target_state is not None:
            path = self._navigate_to_target(transitions, current, target_state)

        return {
            "states": states,
            "labels": labels,
            "transitions": transitions,
            "current_state": int(current),
            "next_state": None if next_state is None else int(next_state),
            "stable_states": stable_states,
            "regime_shifts": regime_shifts,
            "instability": instability,
            "path_to_target": path
        }


# --- Example usage ---
if __name__ == "__main__":
    traj = np.sin(np.linspace(0, 20, 200))

    nx = NEXAH(n_clusters=3, window=10)

    # z.B. Zielzustand 0
    result = nx.analyze(traj, target_state=0)

    print("Current state:", result["current_state"])
    print("Next state:", result["next_state"])
    print("Stable states:", result["stable_states"])
    print("Regime shifts:", result["regime_shifts"][:10], "...")

    print("Path to target:", result["path_to_target"])

    print("Transitions:")
    for k, v in result["transitions"].items():
        print(f"{k} -> {v}")
