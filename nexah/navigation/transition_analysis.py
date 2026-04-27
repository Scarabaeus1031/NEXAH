# ============================================================
# 🧭 NEXAH — Transition Analysis
# ============================================================
#
# Purpose:
# Analyze structure of transitions in state graph
#
# ============================================================

import numpy as np


# ------------------------------------------------------------
# SYMMETRY ANALYSIS
# ------------------------------------------------------------

def compute_symmetry(graph):
    """
    Measure symmetry of transitions:
    P(i→j) vs P(j→i)
    """

    symmetry = []

    for i, targets in graph.items():
        for j, data in targets.items():

            if j not in graph:
                continue

            if i not in graph[j]:
                continue

            pij = data["probability"]
            pji = graph[j][i]["probability"]

            symmetry.append({
                "i": i,
                "j": j,
                "P(i→j)": pij,
                "P(j→i)": pji,
                "difference": abs(pij - pji)
            })

    return symmetry


# ------------------------------------------------------------
# DRIFT ANALYSIS
# ------------------------------------------------------------

def compute_drift(basins):
    """
    Average movement direction in state space
    """

    diffs = []

    for t in range(len(basins) - 1):
        diffs.append(basins[t + 1] - basins[t])

    diffs = np.array(diffs)

    return {
        "mean_drift": float(np.mean(diffs)),
        "std_drift": float(np.std(diffs)),
        "positive_moves": int(np.sum(diffs > 0)),
        "negative_moves": int(np.sum(diffs < 0)),
    }


# ------------------------------------------------------------
# TRANSITION DISTANCE
# ------------------------------------------------------------

def compute_transition_distances(graph):
    """
    Measure how far transitions jump (|i - j|)
    """

    distances = []

    for i, targets in graph.items():
        for j, data in targets.items():

            distances.append({
                "from": i,
                "to": j,
                "distance": abs(i - j),
                "probability": data["probability"]
            })

    return distances


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

def analyze_transitions(basins, graph):
    """
    Full analysis
    """

    symmetry = compute_symmetry(graph)
    drift = compute_drift(basins)
    distances = compute_transition_distances(graph)

    return {
        "symmetry": symmetry,
        "drift": drift,
        "distances": distances
    }
