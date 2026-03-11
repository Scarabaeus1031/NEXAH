"""
NEXAH Symmetry Graph – 3 Cycle Experiment
-----------------------------------------

Graph structure:

center node
17 spokes

Cycle layers:
C5  (pentagon)
C6  (hexagon A)
C6  (hexagon B)

Partition:
5 + 6 + 6 = 17
"""

import networkx as nx
import matplotlib.pyplot as plt
import math


# -------------------------
# Build Graph
# -------------------------

def build_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    # center connections
    for s in spokes:
        G.add_edge(center, s)

    # C5 pentagon
    pentagon = spokes[0:5]

    for i in range(5):
        G.add_edge(pentagon[i], pentagon[(i+1) % 5])

    # C6 hexagon A
    hexagon1 = spokes[5:11]

    for i in range(6):
        G.add_edge(hexagon1[i], hexagon1[(i+1) % 6])

    # C6 hexagon B
    hexagon2 = spokes[11:17]

    for i in range(6):
        G.add_edge(hexagon2[i], hexagon2[(i+1) % 6])

    return G


# -------------------------
# Geometric Layout
# -------------------------

def layout_graph(G):

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
# Draw Graph
# -------------------------

def draw_graph(G):

    pos = layout_graph(G)

    plt.figure(figsize=(8,8))

    nx.draw_networkx_nodes(G, pos, node_size=500)
    nx.draw_networkx_edges(G, pos, width=1.8)
    nx.draw_networkx_labels(G, pos, font_size=9)

    plt.title("NEXAH Symmetry Graph (C5 + C6 + C6)")

    plt.axis("off")
    plt.tight_layout()

    plt.savefig("symmetry_graph_3cycle.png", dpi=300)

    plt.show()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_graph()

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    draw_graph(G)
