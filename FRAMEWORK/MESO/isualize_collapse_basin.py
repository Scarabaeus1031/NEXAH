import networkx as nx
import matplotlib.pyplot as plt


def visualize_collapse_basin(regime_map, basin):

    graph = regime_map["graph"]

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    collapse_states = regime_map.get("collapse_states", set())

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        elif node in basin:
            node_colors.append("orange")

        else:
            node_colors.append("green")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        arrows=True
    )

    plt.title("NEXAH Collapse Basin")

    plt.show()
