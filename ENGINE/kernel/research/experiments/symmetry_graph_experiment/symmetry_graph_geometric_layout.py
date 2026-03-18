"""
NEXAH Symmetry Graph (Geometric Layout)
---------------------------------------

Creates a geometrically structured visualization of the
17–Pentagon–Hexagon symmetry graph.

Structure:
- center node
- 17 spokes on a circle
- pentagon ring
- hexagon ring
"""

import networkx as nx
import matplotlib.pyplot as plt
import math


# -------------------------
# Graph Builder
# -------------------------

def build_symmetry_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    # center connections
    for s in spokes:
        G.add_edge(center, s)

    # pentagon
    pentagon = spokes[:5]

    for i in range(5):
        G.add_edge(pentagon[i], pentagon[(i+1) % 5])

    # hexagon
    hexagon = spokes[5:11]

    for i in range(6):
        G.add_edge(hexagon[i], hexagon[(i+1) % 6])

    return G


# -------------------------
# Geometric Layout
# -------------------------

def geometric_layout(G):

    pos = {}

    center = "center"
    pos[center] = (0, 0)

    radius = 3

    spokes = [n for n in G.nodes() if n != center]

    for i, node in enumerate(spokes):

        angle = 2 * math.pi * i / len(spokes)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        pos[node] = (x, y)

    return pos


# -------------------------
# Visualization
# -------------------------

def draw_graph(G):

    pos = geometric_layout(G)

    plt.figure(figsize=(8,8))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=500
    )

    nx.draw_networkx_edges(
        G,
        pos,
        width=1.8
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9
    )

    plt.title("NEXAH Symmetry Graph (Geometric Layout: 17–Pentagon–Hexagon)")

    plt.axis("off")

    plt.tight_layout()

    plt.savefig("symmetry_graph_geometric.png", dpi=300)

    plt.show()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_symmetry_graph()

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    draw_graph(G)
