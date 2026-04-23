"""
NEXAH Symmetry Graph Drift Simulation
-------------------------------------

Simulates structural drift on the symmetry graph (C5 + C6 + C6).

Process:
Graph → random edge failure → cycle analysis → regime detection
"""

import random
import networkx as nx

from .symmetry_graph_3cycle import build_graph


# -------------------------
# Regime Detection
# -------------------------

def detect_regime(G):

    if not nx.is_connected(G):
        return "FRAGMENT"

    cycles = nx.cycle_basis(G)

    lengths = [len(c) for c in cycles]

    if any(l >= 6 for l in lengths):
        return "STABLE"

    if any(l >= 3 for l in lengths):
        return "STRESS"

    return "COLLAPSE"


# -------------------------
# Drift Step
# -------------------------

def drift_step(G):

    edges = list(G.edges())

    if not edges:
        return

    edge = random.choice(edges)

    G.remove_edge(*edge)

    return edge


# -------------------------
# Simulation
# -------------------------

def run_simulation(steps=20):

    G = build_graph()

    print("\nInitial Graph")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    for t in range(steps):

        removed = drift_step(G)

        regime = detect_regime(G)

        print("\nStep:", t+1)
        print("Removed edge:", removed)
        print("Edges remaining:", G.number_of_edges())
        print("Regime:", regime)

        if regime == "FRAGMENT":
            print("Graph fragmented → simulation stop")
            break


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    run_simulation(steps=30)
