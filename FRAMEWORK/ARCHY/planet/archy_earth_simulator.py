from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability
from FRAMEWORK.ARCHY.planet.archy_geographic_network import build_geographic_network


# ---------------------------------------------------
# GLOBAL PARAMETERS
# ---------------------------------------------------

threshold = 0.27
shock = 0.003


# ---------------------------------------------------
# STABILITY EVOLUTION
# ---------------------------------------------------

def evolve_stability(stability, climate, year):

    noise = np.random.normal(0, shock)

    if climate == "urban_heat":
        trend = -0.001

    elif climate == "coastal":
        trend = -0.0005

    elif climate == "tropical":
        trend = -0.0015

    else:
        trend = 0

    warming = (year - 2025) * 0.0005

    new_value = stability + trend - warming + noise

    return max(0.25, min(0.45, new_value))


# ---------------------------------------------------
# NETWORK COUPLING
# ---------------------------------------------------

def apply_network_effect(G):

    for node in G.nodes:

        neighbors = list(G.neighbors(node))

        if not neighbors:
            continue

        neighbor_stability = [
            G.nodes[n]["stability"] for n in neighbors
        ]

        avg = np.mean(neighbor_stability)

        own = G.nodes[node]["stability"]

        G.nodes[node]["stability"] = 0.7 * own + 0.3 * avg


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = simulate_city_stability()

    G = build_geographic_network(cities)

    for name, lat, lon, stability, climate in cities:

        G.nodes[name]["lat"] = lat
        G.nodes[name]["lon"] = lon
        G.nodes[name]["climate"] = climate
        G.nodes[name]["stability"] = stability

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    year = 2025

    lats = [G.nodes[n]["lat"] for n in G.nodes]
    lons = [G.nodes[n]["lon"] for n in G.nodes]

    stability = [G.nodes[n]["stability"] for n in G.nodes]

    sc = ax.scatter(
        lons,
        lats,
        c=stability,
        cmap="viridis",
        s=200,
        transform=ccrs.PlateCarree(),
        vmin=0.25,
        vmax=0.40
    )

    plt.colorbar(sc, label="City Stability")

    for node in G.nodes:

        ax.text(
            G.nodes[node]["lon"] + 1,
            G.nodes[node]["lat"] + 1,
            node,
            fontsize=8
        )

    def update(frame):

        nonlocal year

        year += 10

        for node in G.nodes:

            s = G.nodes[node]["stability"]
            climate = G.nodes[node]["climate"]

            G.nodes[node]["stability"] = evolve_stability(
                s,
                climate,
                year
            )

        apply_network_effect(G)

        new_stability = [G.nodes[n]["stability"] for n in G.nodes]

        sc.set_array(np.array(new_stability))

        ax.set_title(f"ARCHY Earth Simulator — {year}")

        print("Year:", year)

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=10,
        interval=1500
    )

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_simulation()
