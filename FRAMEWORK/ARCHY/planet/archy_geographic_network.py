from __future__ import annotations

import math
import matplotlib.pyplot as plt
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability


# ---------------------------------------------------
# GEOGRAPHIC DISTANCE
# ---------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi/2)**2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(dlambda/2)**2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


# ---------------------------------------------------
# BUILD NETWORK FROM DISTANCE
# ---------------------------------------------------

def build_geographic_network(cities, max_distance=3000):

    G = nx.Graph()

    for name, lat, lon, stability, climate in cities:

        G.add_node(
            name,
            lat=lat,
            lon=lon,
            stability=stability
        )

    city_list = list(G.nodes)

    for i in range(len(city_list)):

        a = city_list[i]

        lat1 = G.nodes[a]["lat"]
        lon1 = G.nodes[a]["lon"]

        for j in range(i+1, len(city_list)):

            b = city_list[j]

            lat2 = G.nodes[b]["lat"]
            lon2 = G.nodes[b]["lon"]

            d = haversine(lat1, lon1, lat2, lon2)

            if d < max_distance:

                G.add_edge(a, b)

    return G


# ---------------------------------------------------
# VISUALIZE NETWORK
# ---------------------------------------------------

def plot_network(G):

    pos = {}

    for node in G.nodes:

        lat = G.nodes[node]["lat"]
        lon = G.nodes[node]["lon"]

        pos[node] = (lon, lat)

    stability = [G.nodes[n]["stability"] for n in G.nodes]

    plt.figure(figsize=(10,6))

    nx.draw(
        G,
        pos,
        node_color=stability,
        cmap="viridis",
        node_size=400,
        with_labels=True
    )

    plt.title("ARCHY Geographic City Network")

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    cities = simulate_city_stability()

    G = build_geographic_network(cities)

    print("Cities:", len(G.nodes))
    print("Connections:", len(G.edges))

    plot_network(G)
