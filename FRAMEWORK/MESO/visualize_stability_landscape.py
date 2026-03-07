import matplotlib.pyplot as plt
import networkx as nx


def visualize_stability_landscape(regime_map, landscape):
    """
    Visualize stability landscape.
    """

    # regime_map enthält bereits den Graphen
    G = regime_map["graph"]

    pos = nx.spring_layout(G, seed=42)

    potentials = [landscape[n]["potential"] for n in G.nodes()]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1800,
        node_color=potentials,
        cmap=plt.cm.viridis
    )

    labels = {
        n: f"{n}\nU={landscape[n]['potential']:.2f}"
        for n in G.nodes()
    }

    nx.draw_networkx_labels(G, pos, labels)

    plt.title("Stability Landscape")
    plt.show()
