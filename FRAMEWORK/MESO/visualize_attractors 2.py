import networkx as nx
import matplotlib.pyplot as plt
from FRAMEWORK.MESO.attractor_detection import detect_attractors


def visualize_attractors(regime_map):
    """
    Visualize attractors in the regime graph.

    Color scheme:
    red   = terminal attractor
    blue  = cycle attractor
    green = normal state
    """

    graph = regime_map["graph"]

    attractor_data = detect_attractors(regime_map)

    terminal_states = set(attractor_data["terminal_states"])
    cycles = attractor_data["cycles"]

    cycle_nodes = set()
    for cycle in cycles:
        cycle_nodes.update(cycle)

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        if node in terminal_states:
            node_colors.append("red")

        elif node in cycle_nodes:
            node_colors.append("blue")

        else:
            node_colors.append("green")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        arrows=True,
        font_size=10
    )

    plt.title("NEXAH Attractor Detection")

    plt.show()
