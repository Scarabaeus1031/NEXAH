"""
NEXAH Symmetry Graph Kernel Test
--------------------------------

Runs structural analysis on the C5 + C6 + C6 symmetry graph.

Goal:
Investigate regime structure and navigation potential
within the NEXAH kernel framework.
"""

import networkx as nx
from .symmetry_graph_3cycle import build_graph


# -------------------------
# Structural Analysis
# -------------------------

def analyze_structure(G):

    print("\n--- STRUCTURAL ANALYSIS ---")

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    print("\nDegree Distribution:")
    degrees = dict(G.degree())
    print(degrees)

    print("\nAverage Degree:", sum(degrees.values()) / len(degrees))

    print("\nClustering Coefficient:")
    print(nx.average_clustering(G))

    print("\nGraph Density:")
    print(nx.density(G))

    print("\nConnected Components:")
    print(nx.number_connected_components(G))


# -------------------------
# Cycle Analysis
# -------------------------

def analyze_cycles(G):

    print("\n--- CYCLE ANALYSIS ---")

    cycles = nx.cycle_basis(G)

    for c in cycles:
        print("Cycle:", c, "Length:", len(c))


# -------------------------
# Navigation Test
# -------------------------

def navigation_test(G):

    print("\n--- NAVIGATION TEST ---")

    start = "s0"
    target = "s13"

    path = nx.shortest_path(G, start, target)

    print(f"Shortest path {start} → {target}:")
    print(path)
    print("Length:", len(path))


# -------------------------
# Centrality Analysis
# -------------------------

def centrality_analysis(G):

    print("\n--- CENTRALITY ---")

    centrality = nx.betweenness_centrality(G)

    sorted_nodes = sorted(
        centrality.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for node, score in sorted_nodes[:5]:
        print(node, score)


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_graph()

    analyze_structure(G)

    analyze_cycles(G)

    navigation_test(G)

    centrality_analysis(G)
