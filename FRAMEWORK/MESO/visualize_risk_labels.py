import networkx as nx
import matplotlib.pyplot as plt


def visualize_risk_labels(regime_map, risk_geometry):
    """
    Visualize regime graph with risk-distance labels.

    Nodes will appear as:
    state_name (distance_to_collapse)
    """

    graph = regime_map["graph"]
    risk_distance = risk_geometry["risk_distance"]

    pos = nx.spring_layout(graph, seed=42)

    labels = {}

    for node in graph.nodes():

        distance = risk_distance.get(node, "?")

        labels[node] = f"{node} ({distance})"

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
        labels=labels,
        node_color=node_colors,
        node_size=2500,
        font_size=10,
        arrows=True
    )

    plt.title("NEXAH Risk Distance Map")

    plt.show()
