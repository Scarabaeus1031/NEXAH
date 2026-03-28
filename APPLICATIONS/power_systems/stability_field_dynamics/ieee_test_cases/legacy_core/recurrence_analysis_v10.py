import numpy as np


def detect_loops(trajectories, eps=1.5, min_length=10):
    """
    Detect closed loops in trajectories.

    Returns:
        loops: list of trajectory segments forming loops
    """
    loops = []

    for traj in trajectories:
        if len(traj) < min_length:
            continue

        start = traj[0]

        for i in range(min_length, len(traj)):
            if np.linalg.norm(traj[i] - start) < eps:
                loops.append(traj[:i])
                break

    return loops


def compute_recurrence_map(trajectories, grid_shape):
    """
    Count how often trajectories return to previously visited regions.
    """
    h, w = grid_shape
    recurrence = np.zeros((h, w))

    for traj in trajectories:
        visited = set()

        for p in traj:
            x, y = int(p[0]), int(p[1])
            key = (x, y)

            if key in visited:
                recurrence[y, x] += 1
            else:
                visited.add(key)

    if recurrence.max() > 0:
        recurrence /= recurrence.max()

    return recurrence
