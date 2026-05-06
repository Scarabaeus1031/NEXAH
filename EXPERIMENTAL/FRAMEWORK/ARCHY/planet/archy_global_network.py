from __future__ import annotations

import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_planet_simulator import generate_planet


def build_city_network(planet):

    size = len(planet)

    G = nx.Graph()

    for x in range(size):
        for y in range(size):

            climate, stability = planet[x][y]

            node_id = f"{x}-{y}"

            G.add_node(
                node_id,
                pos=(x, y),
                stability=stability,
                climate=climate
            )

    # connect neighbors

    for x in range(size):
        for y in range(size):

            node = f"{x}-{y}"

            for dx, dy in [(1,0),(0,1)]:

                nx_ = x + dx
                ny_ = y + dy

                if nx_ < size and ny_ < size:

                    neighbor = f"{nx_}-{ny_}"

                    G.add_edge(node, neighbor)

    return G


def cascade_failure(G, threshold=0.26):

    failed_nodes = []

    for node in list(G.nodes()):

        stability = G.nodes[node]["stability"]

        if stability < threshold:

            failed_nodes.append(node)

            G.remove_node(node)

    return failed_nodes


def plot_network(G):

    pos = {node: G.nodes[node]["pos"] for node in G.nodes()}

    stability = [G.nodes[n]["stability"] for n in G.nodes()]

    plt.figure(figsize=(7,7))

    nx.draw(
        G,
        pos,
        node_color=stability,
        cmap="viridis",
        node_size=200,
        with_labels=False
    )

    plt.title("Global City Infrastructure Network")

    plt.show()


if __name__ == "__main__":

    planet = generate_planet(8)

    G = build_city_network(planet)

    failed = cascade_failure(G)

    print("Cities failed:", len(failed))

    plot_network(G)
