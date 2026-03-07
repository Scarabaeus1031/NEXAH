import networkx as nx
import matplotlib.pyplot as plt


def visualize_regime_map(regime_map, save_path=None):

    G = regime_map["graph"]
    collapse_states = regime_map["collapse_states"]
    basins = regime_map["basins"]

    pos = nx.spring_layout(G)

    node_colors = []

    for node in G.nodes():

        if node in collapse_states:
            node_colors.append("red")

        else:
            in_basin = False

            for basin_nodes in basins.values():
                if node in basin_nodes:
                    in_basin = True

            if in_basin:
                node_colors.append("orange")
            else:
                node_colors.append("lightblue")

    plt.figure(figsize=(8,6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=10,
        arrows=True
    )

    plt.title("NEXAH Regime Map")

    if save_path:
        plt.savefig(save_path)

    plt.show()
