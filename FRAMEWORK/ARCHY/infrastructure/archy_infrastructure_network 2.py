from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from FRAMEWORK.ARCHY.urban.archy_city_fields import simulate_city


def build_grid_network(size):

    G = nx.grid_2d_graph(size, size)

    for node in G.nodes():
        G.nodes[node]["load"] = np.random.uniform(0.3, 1.0)

    return G


def apply_city_stability(G, stability_grid):

    for (x, y) in G.nodes():

        stability = stability_grid[x, y]

        G.nodes[(x, y)]["capacity"] = stability


def cascade_failure(G, threshold=0.2):

    failed = []

    for node in G.nodes():

        capacity = G.nodes[node]["capacity"]
        load = G.nodes[node]["load"]

        if capacity < threshold or load > capacity:

            failed.append(node)

    for node in failed:

        G.remove_node(node)

    return G, failed


def simulate_network(size=30):

    city, field, modified = simulate_city(size=size)

    G = build_grid_network(size)

    apply_city_stability(G, modified)

    G_after, failed = cascade_failure(G)

    return modified, G_after, failed


def plot_network(city_grid, G):

    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.title("Urban Stability Field")
    plt.imshow(city_grid, cmap="viridis")

    plt.subplot(1,2,2)
    plt.title("Infrastructure Network")

    pos = {(x,y):(y,-x) for (x,y) in G.nodes()}

    nx.draw(G, pos=pos, node_size=10)

    plt.show()


if __name__ == "__main__":

    grid, G, failed = simulate_network(25)

    plot_network(grid, G)

    print("Failed nodes:", len(failed))
