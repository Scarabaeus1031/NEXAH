import numpy as np


def build_transition_counts(trajectories, grid_shape):
    """
    Build transition counts between grid cells.

    Returns:
        dict: {(x1,y1): {(x2,y2): count}}
    """
    counts = {}

    h, w = grid_shape

    for traj in trajectories:
        for i in range(len(traj) - 1):
            x1, y1 = map(int, traj[i])
            x2, y2 = map(int, traj[i + 1])

            if not (0 <= x1 < w and 0 <= y1 < h and 0 <= x2 < w and 0 <= y2 < h):
                continue

            key1 = (x1, y1)
            key2 = (x2, y2)

            if key1 not in counts:
                counts[key1] = {}

            if key2 not in counts[key1]:
                counts[key1][key2] = 0

            counts[key1][key2] += 1

    return counts


def normalize_transition_matrix(counts):
    """
    Normalize transition counts to probabilities.

    Returns:
        probs: dict {(x1,y1): {(x2,y2): prob}}
    """
    probs = {}

    for state, transitions in counts.items():
        total = sum(transitions.values())

        if total == 0:
            continue

        probs[state] = {}

        for next_state, c in transitions.items():
            probs[state][next_state] = c / total

    return probs


def compute_transition_entropy(probs, grid_shape):
    """
    Compute local entropy of transition probabilities at each cell.

    Returns:
        entropy: 2D array normalized to [0,1] if possible
    """
    h, w = grid_shape
    entropy = np.zeros((h, w), dtype=float)

    for (x, y), transitions in probs.items():
        H = 0.0

        for p in transitions.values():
            if p > 0:
                H -= p * np.log(p)

        if 0 <= x < w and 0 <= y < h:
            entropy[y, x] = H

    if entropy.max() > 0:
        entropy /= entropy.max()

    return entropy
