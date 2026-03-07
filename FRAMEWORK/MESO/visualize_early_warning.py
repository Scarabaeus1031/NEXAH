import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.MESO.early_warning_signals import detect_early_warning_signals


def visualize_early_warning(regime_map, risk):
    """
    Visualize early warning structure of the system.

    Color scheme:
    green   = stable
    yellow  = early warning
    orange  = tipping point
    red     = collapse
    """

    graph = regime_map["graph"]

    data = detect_early_warning_signals(regime_map, risk)

    early_warning = set(data["early_warning_states"])
    tipping_points = set(data["tipping_points"])
    collapse_states = set(data["collapse_states"])

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        elif node in tipping_points:
            node_colors.append("orange")

        elif node in early_warning:
            node_colors.append("yellow")

        else:
            node_colors.append("green")

    labels = {node: node for node in graph.nodes()}

    nx.draw(
        graph,
        pos,
        labels=labels,
        node_color=node_colors,
        node_size=2500,
        arrows=True,
        font_size=10
    )

    plt.title("NEXAH Early Warning Structure")

    plt.show()
