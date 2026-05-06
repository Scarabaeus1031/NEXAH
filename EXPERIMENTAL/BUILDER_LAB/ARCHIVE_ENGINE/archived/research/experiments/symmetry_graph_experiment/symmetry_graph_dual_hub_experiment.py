"""
NEXAH Symmetry Graph – Dual Hub Experiment
------------------------------------------

Tests resilience of a dual-hub version of the symmetry graph.

Structure:
center_A
center_B
connected to C5 + C6 + C6 modules
"""

import networkx as nx
import random

from .symmetry_graph_3cycle import build_graph


# -------------------------
# build dual hub graph
# -------------------------

def build_dual_hub_graph():

    G = build_graph()

    # rename original center
    nx.relabel_nodes(G, {"center": "center_A"}, copy=False)

    # add second hub
    G.add_node("center_B")

    # connect B to all outer nodes
    for i in range(17):
        node = f"s{i}"
        if node in G:
            G.add_edge("center_B", node)

    # connect hubs together
    G.add_edge("center_A", "center_B")

    return G


# -------------------------
# regime detection
# -------------------------

def detect_regime(G):

    if nx.number_connected_components(G) > 1:
        return "FRAGMENT"

    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()

    if avg_degree < 2.5:
        return "STRESS"

    return "STABLE"


# -------------------------
# drift simulation
# -------------------------

def run_simulation():

    G = build_dual_hub_graph()

    edges = list(G.edges())
    random.shuffle(edges)

    for step, edge in enumerate(edges):

        G.remove_edge(*edge)

        regime = detect_regime(G)

        if regime == "FRAGMENT":
            return step + 1

    return len(edges)


# -------------------------
# experiment
# -------------------------

def run_experiment(runs=300):

    results = []

    for _ in range(runs):

        collapse = run_simulation()
        results.append(collapse)

    return results


# -------------------------
# run
# -------------------------

if __name__ == "__main__":

    print("\nRunning Dual Hub Experiment...\n")

    data = run_experiment(300)

    print("Runs:", len(data))
    print("Min collapse:", min(data))
    print("Max collapse:", max(data))
    print("Mean collapse:", sum(data)/len(data))
