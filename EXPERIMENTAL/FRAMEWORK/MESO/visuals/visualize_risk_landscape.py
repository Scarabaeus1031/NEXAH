import networkx as nx
import matplotlib.pyplot as plt


def visualize_risk_landscape(regime_map, risk_geometry):

    graph = regime_map["graph"]
    gradient = risk_geometry["risk_gradient"]

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []

    for node in graph.nodes():

        score = gradient.get(node, 0)

        if score > 0.75:
            node_colors.append("green")
        elif score > 0.5:
            node_colors.append("yellow")
        elif score > 0.25:
            node_colors.append("orange")
        else:
            node_colors.append("red")

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=10,
        arrows=True
    )

    plt.title("NEXAH Risk Landscape")

    plt.show()
