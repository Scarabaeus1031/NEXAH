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
# GLOBAL PARAMETERS
# ---------------------------------------------------

INITIAL_STABILITY = 0.33


# ---------------------------------------------------
# BUILD CITY NETWORK
# ---------------------------------------------------

def build_city_network(cities):

    G = nx.Graph()

    for c in cities:

        G.add_node(
            c["name"],
            lat=c["lat"],
            lon=c["lon"],
            population=c["population"],
            stability=INITIAL_STABILITY
        )

    return G


# ---------------------------------------------------
# GLOBAL DYNAMICS
# ---------------------------------------------------

def evolve_population(pop, stability):

    growth = 0.01
    stress = (0.34 - stability) * 0.03
    noise = np.random.normal(0, 0.003)

    return max(0.2, pop * (1 + growth - stress + noise))


def evolve_stability(stability):

    noise = np.random.normal(0, 0.004)

    stability += noise

    return max(0.25, min(0.40, stability))


# ---------------------------------------------------
# GLOBAL METRICS
# ---------------------------------------------------

def compute_metrics(G):

    stability_values = [G.nodes[n]["stability"] for n in G.nodes]

    unstable = [s for s in stability_values if s < 0.29]

    instability_index = np.mean([0.34 - s for s in stability_values])

    conflict_probability = len(unstable) / len(stability_values)

    migration_pressure = sum([max(0, 0.30 - s) for s in stability_values])

    supply_stress = instability_index * 1.5

    return {
        "unstable": len(unstable),
        "instability_index": instability_index,
        "conflict_probability": conflict_probability,
        "migration_pressure": migration_pressure,
        "supply_stress": supply_stress
    }


# ---------------------------------------------------
# MAP
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

        d = G.nodes[city]

        lats.append(d["lat"])
        lons.append(d["lon"])
        sizes.append(d["population"] * 2)
        stability.append(d["stability"])

    ax.scatter(
        lons,
        lats,
        c=stability,
        s=sizes,
        cmap="viridis",
        transform=ccrs.PlateCarree(),
        vmin=0.25,
        vmax=0.40
    )

    ax.set_title(f"ARCHY Global Stability Map — {year}")


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_city_network(cities)

    fig = plt.figure(figsize=(14,8))

    ax_map = plt.subplot2grid((2,2),(0,0),projection=ccrs.PlateCarree())
    ax_instability = plt.subplot2grid((2,2),(0,1))
    ax_conflicts = plt.subplot2grid((2,2),(1,0))
    ax_supply = plt.subplot2grid((2,2),(1,1))

    year = 2025

    years=[]
    instability_series=[]
    conflict_series=[]
    supply_series=[]

    def update(frame):

        nonlocal year

        year += 10

        for city in G.nodes:

            pop = G.nodes[city]["population"]
            stab = G.nodes[city]["stability"]

            G.nodes[city]["population"] = evolve_population(pop, stab)
            G.nodes[city]["stability"] = evolve_stability(stab)

        metrics = compute_metrics(G)

        years.append(year)
        instability_series.append(metrics["instability_index"])
        conflict_series.append(metrics["conflict_probability"])
        supply_series.append(metrics["supply_stress"])

        print(
            "Year:", year,
            "Unstable:", metrics["unstable"],
            "ConflictProb:", round(metrics["conflict_probability"],3)
        )

        draw_map(ax_map, G, year)

        # instability graph
        ax_instability.clear()
        ax_instability.plot(years, instability_series)
        ax_instability.set_title("Global Instability Index")

        # conflict graph
        ax_conflicts.clear()
        ax_conflicts.plot(years, conflict_series)
        ax_conflicts.set_title("Conflict Probability")

        # supply stress
        ax_supply.clear()
        ax_supply.plot(years, supply_series)
        ax_supply.set_title("Supply Chain Stress")

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=40,
        interval=1000
    )

    draw_map(ax_map, G, year)

    plt.tight_layout()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run()
