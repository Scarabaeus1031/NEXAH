from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability


# ---------------------------------------------------
# GLOBAL INFRASTRUCTURE NETWORK
# ---------------------------------------------------

NETWORK_CONNECTIONS = [

    ("New York", "London"),
    ("London", "Frankfurt"),
    ("Frankfurt", "Paris"),
    ("Paris", "Berlin"),

    ("Tokyo", "Shanghai"),
    ("Shanghai", "Delhi"),

    ("Los Angeles", "Tokyo"),

    ("São Paulo", "Buenos Aires"),

    ("Cairo", "Lagos"),
]


# ---------------------------------------------------
# BUILD NETWORK GRAPH
# ---------------------------------------------------

def build_network(cities):

    G = nx.Graph()

    for name, lat, lon, stability, climate in cities:

        G.add_node(
            name,
            lat=lat,
            lon=lon,
            stability=stability,
            climate=climate
        )

    for a, b in NETWORK_CONNECTIONS:

        if a in G.nodes and b in G.nodes:
            G.add_edge(a, b)

    return G


# ---------------------------------------------------
# CASCADE SIMULATION
# ---------------------------------------------------

def simulate_cascade(G, threshold=0.29, shock=0.01):

    failed = []

    for node in G.nodes:

        stability = G.nodes[node]["stability"]

        if stability < threshold:

            failed.append(node)

            for neighbor in G.neighbors(node):

                G.nodes[neighbor]["stability"] -= shock

    return failed


# ---------------------------------------------------
# VISUALIZATION
# ---------------------------------------------------

def plot_network(G):

    pos = nx.spring_layout(G)

    stability = [G.nodes[n]["stability"] for n in G.nodes]

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=stability,
        cmap="viridis",
        node_size=800
    )

    plt.title("ARCHY Global Infrastructure Network")

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    cities = simulate_city_stability()

    G = build_network(cities)

    failed = simulate_cascade(G)

    print("Cities failed:", len(failed))

    if failed:
        print("Failed cities:", failed)

    plot_network(G)
