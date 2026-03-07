"""
NEXAH MESO Layer

visualize_energy_landscape.py

Visualize the system energy landscape.
"""

import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.MESO.system_energy_landscape import compute_system_energy_landscape


def visualize_energy_landscape(regime_map, risk):
    """
    Visualize energy levels of system states.
    """

    graph = regime_map["graph"]

    energy_data = compute_system_energy_landscape(regime_map, risk)

    energy_landscape = energy_data["energy_landscape"]

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        energy = energy_landscape[node]["energy"]

        if energy >= 0.66:
            node_colors.append("red")

        elif energy >= 0.33:
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

    plt.title("System Energy Landscape")

    plt.show()
