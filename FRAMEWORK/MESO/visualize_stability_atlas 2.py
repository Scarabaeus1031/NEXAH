import networkx as nx
import matplotlib.pyplot as plt


def visualize_stability_atlas(regime_map, atlas):
    """
    Visualize the stability atlas of the system.

    Color scheme:
    green  → safe states
    orange → collapse basin
    red    → collapse states
    gray   → unknown
    """

    graph = regime_map["graph"]

    safe_states = set(atlas.get("safe_states", []))
    collapse_basin = set(atlas.get("collapse_basin", []))
    collapse_states = set(atlas.get("collapse_states", []))

    risk_distance = atlas.get("risk_distance", {})

    pos = nx.spring_layout(graph, seed=42)

    node_colors = []
    labels = {}

    for node in graph.nodes():

        if node in collapse_states:
            node_colors.append("red")

        elif node in collapse_basin:
            node_colors.append("orange")

        elif node in safe_states:
            node_colors.append("green")

        else:
            node_colors.append("gray")

        distance = risk_distance.get(node, "?")
        labels[node] = f"{node} ({distance})"

    nx.draw(
        graph,
        pos,
        labels=labels,
        node_color=node_colors,
        node_size=2500,
        arrows=True,
        font_size=10
    )

    plt.title("NEXAH Stability Atlas")

    plt.show()
