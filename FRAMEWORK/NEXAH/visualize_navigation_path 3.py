import networkx as nx
import matplotlib.pyplot as plt


def visualize_navigation_path(regime_map, path):
    """
    Visualize the regime graph and highlight
    the navigation trajectory.
    """

    graph = regime_map["graph"]

    pos = nx.spring_layout(graph, seed=42)

    # base node colors
    node_colors = []

    collapse_states = regime_map.get("collapse_states", set())

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")
        else:
            node_colors.append("orange")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        arrows=True
    )

    # highlight path edges
    path_edges = []

    for i in range(len(path) - 1):
        path_edges.append((path[i], path[i + 1]))

    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=path_edges,
        width=4,
        edge_color="blue"
    )

    plt.title("NEXAH Navigation Path")

    plt.show()
