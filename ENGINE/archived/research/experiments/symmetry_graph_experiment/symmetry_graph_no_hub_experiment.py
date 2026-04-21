"""
NEXAH Symmetry Graph – No Hub Experiment
----------------------------------------

Removes the center node (Q°) and tests how the
C5 + C6 + C6 structure behaves without a hub.

Goal:
Determine whether stability comes from
the hub or the cycles themselves.
"""

import networkx as nx
import random

from .symmetry_graph_3cycle import build_graph


# --------------------------
# remove hub
# --------------------------

def build_no_hub_graph():

    G = build_graph()

    if "center" in G:
        G.remove_node("center")

    return G


# --------------------------
# regime detection
# --------------------------

def detect_regime(G):

    components = nx.number_connected_components(G)

    if components > 1:
        return "FRAGMENT"

    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()

    if avg_degree < 2:
        return "STRESS"

    return "STABLE"


# --------------------------
# drift simulation
# --------------------------

def run_simulation():

    G = build_no_hub_graph()

    edges = list(G.edges())
    random.shuffle(edges)

    for step, edge in enumerate(edges):

        G.remove_edge(*edge)

        regime = detect_regime(G)

        if regime == "FRAGMENT":

            return step + 1

    return len(edges)


# --------------------------
# experiment
# --------------------------

def run_experiment(runs=200):

    results = []

    for _ in range(runs):

        collapse = run_simulation()
        results.append(collapse)

    return results


# --------------------------
# run
# --------------------------

if __name__ == "__main__":

    print("\nRunning No-Hub Symmetry Experiment...\n")

    data = run_experiment(300)

    print("Runs:", len(data))
    print("Min collapse:", min(data))
    print("Max collapse:", max(data))
    print("Mean collapse:", sum(data)/len(data))
