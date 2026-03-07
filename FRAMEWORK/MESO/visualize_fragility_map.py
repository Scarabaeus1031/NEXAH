"""
NEXAH MESO Layer

visualize_fragility_map.py

Visualize system fragility in the regime graph.
"""

import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.MESO.system_fragility_map import compute_system_fragility_map


def visualize_fragility_map(regime_map, risk):
    """
    Visualize fragility levels for each system state.
    """

    graph = regime_map["graph"]

    fragility_data = compute_system_fragility_map(regime_map, risk)

    fragility_map = fragility_data["fragility_map"]

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        fragility = fragility_map[node]

        if fragility >= 0.66:
            node_colors.append("red")

        elif fragility >= 0.33:
            node_colors.append("orange")

        else:
            node_colors.append("green")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=10,
        font_weight="bold"
    )

    plt.title("System Fragility Map")

    plt.show()
