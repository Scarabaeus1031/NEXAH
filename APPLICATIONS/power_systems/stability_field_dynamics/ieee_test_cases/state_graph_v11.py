import numpy as np


def assign_state(point, labeled):
    y, x = int(point[1]), int(point[0])
    if 0 <= y < labeled.shape[0] and 0 <= x < labeled.shape[1]:
        return labeled[y, x]
    return 0


def build_state_transition_graph(trajectories, labeled):
    """
    Build transition counts between detected states.
    """
    transitions = {}

    for traj in trajectories:
        prev_state = None

        for p in traj:
            s = assign_state(p, labeled)
            if s == 0:
                continue

            if prev_state is not None and prev_state != s:
                key = (prev_state, s)
                transitions[key] = transitions.get(key, 0) + 1

            prev_state = s

    return transitions
