from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_planet_simulator import generate_planet
from FRAMEWORK.ARCHY.planet.archy_global_network import build_city_network


def propagate_failure(G, threshold=0.26):

    new_failed = []

    for node in list(G.nodes()):

        stability = G.nodes[node]["stability"]

        neighbors = list(G.neighbors(node))

        if not neighbors:
            continue

        neighbor_stability = sum(
            G.nodes[n]["stability"] for n in neighbors
        ) / len(neighbors)

        effective = (stability + neighbor_stability) / 2

        if effective < threshold:
            new_failed.append(node)

    for node in new_failed:
        if node in G:
            G.remove_node(node)

    return new_failed


def animate_cascade(G, steps=10):

    pos = {node: G.nodes[node]["pos"] for node in G.nodes()}

    fig, ax = plt.subplots(figsize=(7,7))

    def update(frame):

        ax.clear()

        failed = propagate_failure(G)

        nodes = list(G.nodes())

        stability = [G.nodes[n]["stability"] for n in nodes]

        nx.draw(
            G,
            pos,
            node_color=stability,
            cmap="viridis",
            node_size=200,
            ax=ax,
            with_labels=False
        )

        ax.set_title(f"Infrastructure Cascade — step {frame}")

        if not failed:
            anim.event_source.stop()

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=steps,
        interval=800
    )

    plt.show()


if __name__ == "__main__":

    planet = generate_planet(8)

    G = build_city_network(planet)

    animate_cascade(G)
