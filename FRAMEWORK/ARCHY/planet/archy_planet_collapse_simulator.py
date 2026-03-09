from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability
from FRAMEWORK.ARCHY.planet.archy_climate_model import climate_stress


# ---------------------------------------------------
# GLOBAL INFRASTRUCTURE CONNECTIONS
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
# BUILD NETWORK
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
# CITY EVOLUTION
# ---------------------------------------------------

def evolve_city(stability, climate, lat, year):

    noise = np.random.normal(0, 0.002)

    stress = climate_stress(lat, year)

    if climate == "urban_heat":
        trend = 0.002 - stress

    elif climate == "coastal":
        trend = 0.001 - stress

    elif climate == "tropical":
        trend = -0.001 - stress

    else:
        trend = -stress

    new_value = stability + trend + noise

    return max(0.25, min(0.45, new_value))


# ---------------------------------------------------
# CASCADE PROPAGATION
# ---------------------------------------------------

def propagate_cascade(G, threshold=0.29, shock=0.01):

    collapsed = []

    for node in list(G.nodes):

        if G.nodes[node]["stability"] < threshold:

            collapsed.append(node)

            for neighbor in G.neighbors(node):

                G.nodes[neighbor]["stability"] -= shock

    return collapsed


# ---------------------------------------------------
# RUN SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = simulate_city_stability()

    G = build_network(cities)

    names = list(G.nodes)

    lats = [G.nodes[n]["lat"] for n in names]
    lons = [G.nodes[n]["lon"] for n in names]
    climates = [G.nodes[n]["climate"] for n in names]
    stability = [G.nodes[n]["stability"] for n in names]

    fig = plt.figure(figsize=(12,6))

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    sc = ax.scatter(
        lons,
        lats,
        c=stability,
        cmap="viridis",
        s=200,
        transform=ccrs.PlateCarree(),
        vmin=0.26,
        vmax=0.40
    )

    for name, lat, lon in zip(names, lats, lons):

        ax.text(
            lon + 1,
            lat + 1,
            name,
            fontsize=8
        )

    plt.colorbar(sc, label="City Stability")

    year = 2025

    def update(frame):

        nonlocal stability, year

        year += 10

        # evolve cities

        stability = [

            evolve_city(
                stability[i],
                climates[i],
                lats[i],
                year
            )

            for i in range(len(stability))

        ]

        # update graph values

        for i, name in enumerate(names):

            G.nodes[name]["stability"] = stability[i]

        # cascade propagation

        collapsed = propagate_cascade(G)

        stability = [G.nodes[n]["stability"] for n in names]

        sc.set_array(np.array(stability))

        ax.set_title(f"ARCHY Planet Collapse Simulation — {year}")

        print("Year:", year)

        if collapsed:
            print("Cascade:", collapsed)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=12,
        interval=1500
    )

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_simulation()
