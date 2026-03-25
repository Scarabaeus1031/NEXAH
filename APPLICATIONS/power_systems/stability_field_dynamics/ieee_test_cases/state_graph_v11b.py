import numpy as np


def assign_state(point, labeled):
    y, x = int(point[1]), int(point[0])
    if 0 <= y < labeled.shape[0] and 0 <= x < labeled.shape[1]:
        return labeled[y, x]
    return 0


def build_weighted_transition_graph(trajectories, labeled):
    transitions = {}
    state_counts = {}

    for traj in trajectories:
        prev = None

        for p in traj:
            s = assign_state(p, labeled)
            if s == 0:
                continue

            state_counts[s] = state_counts.get(s, 0) + 1

            if prev is not None and prev != s:
                key = (prev, s)
                transitions[key] = transitions.get(key, 0) + 1

            prev = s

    # normalize → probabilities
    probs = {}
    for (a, b), c in transitions.items():
        total = sum(v for (x, y), v in transitions.items() if x == a)
        probs[(a, b)] = c / total if total > 0 else 0

    return transitions, probs, state_counts


def compute_state_entropy(probs):
    entropy = {}

    for (a, b), p in probs.items():
        if a not in entropy:
            entropy[a] = []

        if p > 0:
            entropy[a].append(-p * np.log(p))

    return {k: sum(v) for k, v in entropy.items()}
