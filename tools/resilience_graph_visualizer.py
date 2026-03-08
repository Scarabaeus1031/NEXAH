# tools/resilience_graph_visualizer.py

import json
import networkx as nx
import matplotlib.pyplot as plt


BASE_SYSTEM = "APPLICATIONS/examples/energy_grid_control.json"
NEW_SYSTEM = "APPLICATIONS/examples/energy_grid_evolved.json"


# --------------------------------------------------
# IO
# --------------------------------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# --------------------------------------------------
# graph builder
# --------------------------------------------------

def build_graph(data):

    G = nx.DiGraph()

    nodes = data.get("nodes", [])
    transitions = data.get("transitions", {})
    regimes = data.get("regimes", {})

    for n in nodes:
        regime = regimes.get(n, "UNKNOWN")
        G.add_node(n, regime=regime)

    for source, targets in transitions.items():

        if isinstance(targets, list):

            for t in targets:
                G.add_edge(source, t)

        else:

            G.add_edge(source, targets)

    return G


# --------------------------------------------------
# node coloring
# --------------------------------------------------

def node_colors(G):

    colors = []

    for n in G.nodes():

        regime = G.nodes[n].get("regime", "")

        if regime.upper() == "STABLE":
            colors.append("green")

        elif regime.upper() == "CRITICAL":
            colors.append("orange")

        elif regime.upper() == "COLLAPSE":
            colors.append("red")

        else:
            colors.append("gray")

    return colors


# --------------------------------------------------
# draw graph
# --------------------------------------------------

def draw_graph(G, title):

    pos = nx.spring_layout(G, seed=42)

    colors = node_colors(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=1800,
        font_size=9,
        arrows=True
    )

    plt.title(title)


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    base = load_json(BASE_SYSTEM)
    new = load_json(NEW_SYSTEM)

    G_base = build_graph(base)
    G_new = build_graph(new)

    plt.figure(figsize=(12,6))

    plt.subplot(1,2,1)
    draw_graph(G_base, "Original System")

    plt.subplot(1,2,2)
    draw_graph(G_new, "Evolved System")

    plt.tight_layout()
    plt.show()
