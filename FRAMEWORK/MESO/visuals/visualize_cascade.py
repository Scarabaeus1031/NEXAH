import networkx as nx
import matplotlib.pyplot as plt

from FRAMEWORK.MESO.cascade_dynamics import simulate_cascade


def visualize_cascade(regime_map, start_state):
    """
    Visualize a cascade path in the regime graph.

    The cascade path is highlighted in red.
    """

    graph = regime_map["graph"]

    cascade = simulate_cascade(regime_map, start_state)

    cascade_path = cascade["cascade_path"]

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []
    edge_colors = []

    # Node coloring
    for node in graph.nodes():
        if node in cascade_path:
            node_colors.append("red")
        else:
            node_colors.append("lightgray")

    # Edge coloring
    cascade_edges = list(zip(cascade_path[:-1], cascade_path[1:]))

    for edge in graph.edges():
        if edge in cascade_edges:
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=2500,
        arrows=True,
        font_size=10
    )

    plt.title(f"NEXAH Cascade Path from '{start_state}'")

    plt.show()
