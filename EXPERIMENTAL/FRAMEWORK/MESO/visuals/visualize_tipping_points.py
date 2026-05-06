import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.MESO.tipping_points import detect_tipping_points


def visualize_tipping_points(regime_map, risk):
    """
    Visualize tipping points in the regime graph.

    Color scheme:
    red    = collapse states
    orange = tipping points
    green  = normal states
    """

    graph = regime_map["graph"]

    tp_data = detect_tipping_points(regime_map, risk)

    tipping_points = set(tp_data["tipping_points"])
    collapse_states = set(tp_data["collapse_states"])

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        elif node in tipping_points:
            node_colors.append("orange")

        else:
            node_colors.append("green")

    labels = {}

    for node in graph.nodes():
        labels[node] = node

    nx.draw(
        graph,
        pos,
        labels=labels,
        node_color=node_colors,
        node_size=2500,
        arrows=True,
        font_size=10
    )

    plt.title("NEXAH Tipping Points")

    plt.show()
