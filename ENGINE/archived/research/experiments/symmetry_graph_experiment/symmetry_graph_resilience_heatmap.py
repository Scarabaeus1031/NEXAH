"""
NEXAH Symmetry Graph Resilience Heatmap
---------------------------------------

Calculates edge criticality by removing each edge and measuring
impact on graph connectivity.

Edges with high impact are colored red.
"""

import networkx as nx
import matplotlib.pyplot as plt

from .symmetry_graph_3cycle import build_graph


# -------------------------
# Criticality metric
# -------------------------

def edge_criticality(G):

    base_components = nx.number_connected_components(G)

    scores = {}

    for edge in G.edges():

        H = G.copy()
        H.remove_edge(*edge)

        new_components = nx.number_connected_components(H)

        # score = increase in components
        score = new_components - base_components

        scores[edge] = score

    return scores


# -------------------------
# Visualization
# -------------------------

def visualize_heatmap(G, scores):

    pos = nx.spring_layout(G, seed=42)

    edge_colors = []

    for edge in G.edges():

        score = scores.get(edge, 0)

        if score > 0:
            edge_colors.append("red")
        else:
            edge_colors.append("lightgray")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        edge_color=edge_colors,
        node_size=600,
        font_size=8
    )

    plt.title("Symmetry Graph Edge Criticality Heatmap")
    plt.show()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_graph()

    scores = edge_criticality(G)

    print("\nEdge Criticality Scores:")

    for edge, score in scores.items():
        print(edge, score)

    visualize_heatmap(G, scores)
