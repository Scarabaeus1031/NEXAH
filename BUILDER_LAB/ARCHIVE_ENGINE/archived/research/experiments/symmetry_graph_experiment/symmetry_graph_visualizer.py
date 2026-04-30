"""
NEXAH Symmetry Graph Visualizer
--------------------------------

Visualizes the 17-29-5 symmetry graph used in the
NEXAH symmetry experiments.

Structure:
- center node
- 17 spokes
- pentagon ring
- hexagon ring
"""

import networkx as nx
import matplotlib.pyplot as plt


# -------------------------
# Build Graph
# -------------------------

def build_symmetry_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    for s in spokes:
        G.add_edge(center, s)

    pentagon = spokes[:5]

    for i in range(5):
        G.add_edge(pentagon[i], pentagon[(i + 1) % 5])

    hexagon = spokes[5:11]

    for i in range(6):
        G.add_edge(hexagon[i], hexagon[(i + 1) % 6])

    return G


# -------------------------
# Visualization
# -------------------------

def draw_graph(G):

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8,8))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=400
    )

    nx.draw_networkx_edges(
        G,
        pos,
        width=1.5
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9
    )

    plt.title("NEXAH Symmetry Graph (17-Pentagon-Hexagon)")

    plt.axis("off")

    plt.tight_layout()

    plt.savefig("symmetry_graph.png", dpi=300)

    plt.show()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_symmetry_graph()

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    draw_graph(G)
