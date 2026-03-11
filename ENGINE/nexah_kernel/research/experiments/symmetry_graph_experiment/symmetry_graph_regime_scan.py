"""
NEXAH Symmetry Graph Regime Scan
--------------------------------

Scans structural regimes under progressive edge drift.

Goal:
Map the transition from STABLE → STRESS → FRAGMENT
as edges disappear.
"""

import networkx as nx
import random
import matplotlib.pyplot as plt

from .symmetry_graph_3cycle import build_graph


# -----------------------------
# Regime detection
# -----------------------------

def detect_regime(G):

    if nx.number_connected_components(G) > 1:
        return "FRAGMENT"

    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()

    if avg_degree < 2.5:
        return "STRESS"

    return "STABLE"


# -----------------------------
# Single drift simulation
# -----------------------------

def run_drift_simulation():

    G = build_graph()

    regimes = []

    edges = list(G.edges())
    random.shuffle(edges)

    for step, edge in enumerate(edges):

        G.remove_edge(*edge)

        regime = detect_regime(G)

        regimes.append(regime)

        if regime == "FRAGMENT":
            break

    return regimes


# -----------------------------
# Multiple runs
# -----------------------------

def regime_scan(runs=200):

    results = []

    for _ in range(runs):

        regimes = run_drift_simulation()

        fragment_step = None

        for i, r in enumerate(regimes):

            if r == "FRAGMENT":
                fragment_step = i + 1
                break

        if fragment_step is None:
            fragment_step = len(regimes)

        results.append(fragment_step)

    return results


# -----------------------------
# Visualization
# -----------------------------

def plot_regime_histogram(data):

    plt.hist(data, bins=15)

    plt.title("Symmetry Graph Regime Collapse Distribution")
    plt.xlabel("Edges removed before fragmentation")
    plt.ylabel("Frequency")

    plt.show()


# -----------------------------
# Run experiment
# -----------------------------

if __name__ == "__main__":

    print("\nRunning Regime Scan...\n")

    data = regime_scan(runs=300)

    print("Runs:", len(data))
    print("Min collapse:", min(data))
    print("Max collapse:", max(data))
    print("Mean collapse:", sum(data)/len(data))

    plot_regime_histogram(data)
