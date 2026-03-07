import matplotlib.pyplot as plt
import networkx as nx


def visualize_stability_landscape(regime_map, landscape):
    """
    Visualize system stability landscape.
    """

    pos = nx.spring_layout(regime_map, seed=42)

    potentials = [landscape[n]["potential"] for n in regime_map.nodes()]

    cmap = plt.cm.viridis

    nx.draw(
        regime_map,
        pos,
        with_labels=True,
        node_size=1800,
        node_color=potentials,
        cmap=cmap
    )

    labels = {
        n: f"{n}\nU={landscape[n]['potential']:.2f}"
        for n in regime_map.nodes()
    }

    nx.draw_networkx_labels(regime_map, pos, labels)

    plt.title("Stability Landscape")
    plt.show()
