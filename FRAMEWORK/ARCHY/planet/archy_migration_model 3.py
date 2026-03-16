from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import networkx as nx
import math

from FRAMEWORK.ARCHY.planet.archy_global_city_dataset import generate_global_city_dataset


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
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# ---------------------------------------------------
# BUILD NETWORK
# ---------------------------------------------------

def build_network(cities, max_distance=2500):

    G = nx.Graph()

    for c in cities:

        G.add_node(
            c["name"],
            lat=c["lat"],
            lon=c["lon"],
            population=c["population"],
            stability=0.33,
        )

    city_list = list(G.nodes)

    for i in range(len(city_list)):

        a = city_list[i]

        lat1 = G.nodes[a]["lat"]
        lon1 = G.nodes[a]["lon"]

        for j in range(i + 1, len(city_list)):

            b = city_list[j]

            lat2 = G.nodes[b]["lat"]
            lon2 = G.nodes[b]["lon"]

            d = haversine(lat1, lon1, lat2, lon2)

            if d < max_distance:
                G.add_edge(a, b)

    return G


# ---------------------------------------------------
# MIGRATION LOGIC
# ---------------------------------------------------

def migration_flow(G):

    flows = {}

    for city in G.nodes:

        stability = G.nodes[city]["stability"]
        population = G.nodes[city]["population"]

        if stability < 0.29:

            neighbors = list(G.neighbors(city))

            if not neighbors:
                continue

            migrants = population * 0.02

            migrants_per_neighbor = migrants / len(neighbors)

            flows[city] = -migrants

            for n in neighbors:

                flows[n] = flows.get(n, 0) + migrants_per_neighbor

    return flows


# ---------------------------------------------------
# APPLY MIGRATION
# ---------------------------------------------------

def apply_migration(G, flows):

    for city, delta in flows.items():

        G.nodes[city]["population"] += delta

        if G.nodes[city]["population"] < 0.2:
            G.nodes[city]["population"] = 0.2


# ---------------------------------------------------
# STABILITY UPDATE
# ---------------------------------------------------

def update_stability(G):

    for city in G.nodes:

        pop = G.nodes[city]["population"]

        stress = (pop - 5) * 0.002

        noise = np.random.normal(0, 0.002)

        G.nodes[city]["stability"] += -stress + noise

        G.nodes[city]["stability"] = max(0.25, min(0.40, G.nodes[city]["stability"]))


# ---------------------------------------------------
# DRAW MAP
# ---------------------------------------------------

def draw_map(ax, G, year):

    ax.clear()

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    lats = []
    lons = []
    sizes = []
    stability = []

    for city in G.nodes:

        data = G.nodes[city]

        lats.append(data["lat"])
        lons.append(data["lon"])
        sizes.append(data["population"] * 2)
        stability.append(data["stability"])

    sc = ax.scatter(
        lons,
        lats,
        c=stability,
        s=sizes,
        cmap="viridis",
        transform=ccrs.PlateCarree(),
        vmin=0.25,
        vmax=0.40,
    )

    ax.set_title(f"ARCHY Migration Simulator — {year}")

    return sc


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = generate_global_city_dataset()

    G = build_network(cities)

    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    year = 2025

    def update(frame):

        nonlocal year

        year += 10

        flows = migration_flow(G)

        apply_migration(G, flows)

        update_stability(G)

        unstable = [c for c in G.nodes if G.nodes[c]["stability"] < 0.29]

        print("Year:", year)

        if unstable:
            print("Unstable cities:", len(unstable))

        return draw_map(ax, G, year)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=30,
        interval=1200,
    )

    draw_map(ax, G, year)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_simulation()
