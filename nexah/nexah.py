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

        # normalize to probabilities
        P = {}
        for a in T:
            total = sum(T[a].values())
            P[a] = {b: T[a][b] / total for b in T[a]}
        return P

    # --- Stability Detection ---
    def _detect_stable_states(self, transitions, threshold=0.9):
        stable = []
        for state in transitions:
            if state in transitions[state]:
                if transitions[state][state] > threshold:
                    stable.append(state)
        return stable

    # --- Regime Shift Detection ---
    def _detect_regime_shifts(self, labels):
        shifts = []
        for i in range(1, len(labels)):
            if labels[i] != labels[i-1]:
                shifts.append(i)
        return shifts

    # --- Main API ---
    def analyze(self, trajectory):
        trajectory = np.array(trajectory)

        # 1. Representation
        states = self._embed(trajectory)

        # 2. Structure (Clustering)
        kmeans = KMeans(n_clusters=self.n_clusters, n_init=10)
        labels = kmeans.fit_predict(states)

        # 3. Transitions
        transitions = self._compute_transitions(labels)

        # 4. Navigation (simple next-step)
        current = labels[-1]
        if current in transitions:
            next_state = max(transitions[current], key=transitions[current].get)
        else:
            next_state = None

        # 5. Stability
        stable_states = self._detect_stable_states(transitions)

        # 6. Regime shifts
        regime_shifts = self._detect_regime_shifts(labels)

        return {
            "states": states,
            "labels": labels,
            "transitions": transitions,
            "current_state": int(current),
            "next_state": None if next_state is None else int(next_state),
            "stable_states": stable_states,
            "regime_shifts": regime_shifts
        }


# --- Example usage ---
if __name__ == "__main__":
    traj = np.sin(np.linspace(0, 20, 200))

    nx = NEXAH(n_clusters=3, window=10)
    result = nx.analyze(traj)

    print("Current state:", result["current_state"])
    print("Next state:", result["next_state"])
    print("Stable states:", result["stable_states"])
    print("Regime shifts (indices):", result["regime_shifts"])
    print("Transitions:", result["transitions"])
