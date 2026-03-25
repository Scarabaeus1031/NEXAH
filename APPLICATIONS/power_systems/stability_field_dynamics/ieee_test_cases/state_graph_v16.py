# APPLICATIONS/power_systems/ieee_test_cases/state_graph_v16.py

import numpy as np


def point_to_state(point, states, max_dist=6.0):
    """
    Assign a trajectory point to the nearest detected state center.
    Returns state index or None.
    """
    if len(states) == 0:
        return None

    x, y = point
    best_idx = None
    best_dist = None

    for i, s in enumerate(states):
        cy, cx = s["center"]
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)

        if best_dist is None or d < best_dist:
            best_dist = d
            best_idx = i

    if best_dist is not None and best_dist <= max_dist:
        return best_idx

    return None


def build_state_graph(trajectories, states, max_dist=6.0):
    """
    Build a directed weighted graph between states from trajectories.

    Returns
    -------
    node_counts : dict
        visits per state
    edge_counts : dict
        transitions between states
    """
    node_counts = {i: 0 for i in range(len(states))}
    edge_counts = {}

    for traj in trajectories:
        assigned = []

        for p in traj:
            sid = point_to_state(p, states, max_dist=max_dist)
            assigned.append(sid)
            if sid is not None:
                node_counts[sid] += 1

        # compress consecutive equal states / Nones
        compressed = []
        prev = object()
        for sid in assigned:
            if sid != prev:
                compressed.append(sid)
                prev = sid

        # transitions only between valid states
        for a, b in zip(compressed[:-1], compressed[1:]):
            if a is None or b is None:
                continue
            edge_counts[(a, b)] = edge_counts.get((a, b), 0) + 1

    return node_counts, edge_counts


def classify_loops_by_state(loops, states, max_dist=6.0):
    """
    Classify loops into:
    - local: mostly around one state
    - bridging: touches multiple states
    - interface: touches none / stays in transition zone
    """
    classified = {
        "local": [],
        "bridging": [],
        "interface": []
    }

    for loop in loops:
        touched = set()

        for p in loop:
            sid = point_to_state(p, states, max_dist=max_dist)
            if sid is not None:
                touched.add(sid)

        if len(touched) == 0:
            classified["interface"].append(loop)
        elif len(touched) == 1:
            classified["local"].append(loop)
        else:
            classified["bridging"].append(loop)

    return classified
