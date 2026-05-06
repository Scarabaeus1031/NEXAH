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
        math.sin(dphi/2)**2 +
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


# ---------------------------------------------------
# BUILD GLOBAL NETWORK
# ---------------------------------------------------

def build_network(cities, max_distance=2000):

    G = nx.Graph()

    for c in cities:

        G.add_node(
            c["name"],
            lat=c["lat"],
            lon=c["lon"],
            population=c["population"],
            gdp=c["gdp"],
            energy=c["energy"],
            climate=c["climate"],
            stability=0.33
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
# POPULATION
# ---------------------------------------------------

def evolve_population(pop, stability):

    growth = 0.012
    stress = (0.34 - stability) * 0.03

    noise = np.random.normal(0, 0.002)

    new_pop = pop * (1 + growth - stress + noise)

    return max(0.2, new_pop)


# ---------------------------------------------------
# ENERGY
# ---------------------------------------------------

def energy_demand(pop):

    return pop * 0.13


def evolve_energy(cap):

    invest = 0.01
    decay = 0.004

    noise = np.random.normal(0, 0.003)

    return cap * (1 + invest - decay + noise)


def energy_impact(demand, capacity):

    ratio = demand / capacity

    if ratio > 1.3:
        return -0.02

    if ratio > 1.1:
        return -0.01

    if ratio < 0.8:
        return 0.003

    return 0


# ---------------------------------------------------
# ECONOMY
# ---------------------------------------------------

def evolve_gdp(gdp, stability):

    growth = 0.01
    stability_bonus = (stability - 0.30) * 0.05

    noise = np.random.normal(0, 0.005)

    return max(0.2, gdp * (1 + growth + stability_bonus + noise))


def trade_feedback(G, city):

    neighbors = list(G.neighbors(city))

    if not neighbors:
        return 0

    partner_gdp = [G.nodes[n]["gdp"] for n in neighbors]

    avg = np.mean(partner_gdp)

    own = G.nodes[city]["gdp"]

    if own < 0.7 * avg:
        return -0.01

    if own > 1.2 * avg:
        return 0.003

    return 0


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = generate_global_city_dataset()

    G = build_network(cities)

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    year = 2025

    def draw():

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
            vmax=0.40
        )

        ax.set_title(f"ARCHY Civilization Simulator v2 — {year}")

        return sc


    def update(frame):

        nonlocal year

        year += 10

        for city in G.nodes:

            data = G.nodes[city]

            pop = evolve_population(data["population"], data["stability"])

            capacity = evolve_energy(data["energy"])
            demand = energy_demand(pop)

            energy_effect = energy_impact(demand, capacity)

            gdp = evolve_gdp(data["gdp"], data["stability"])

            trade_effect = trade_feedback(G, city)

            data["population"] = pop
            data["energy"] = capacity
            data["gdp"] = gdp

            data["stability"] += energy_effect + trade_effect

            data["stability"] = max(0.25, min(0.40, data["stability"]))

        print("Year:", year)

        unstable = [c for c in G.nodes if G.nodes[c]["stability"] < 0.29]

        if unstable:

            print("Unstable cities:", len(unstable))

        return draw()


    anim = animation.FuncAnimation(
        fig,
        update,
        frames=30,
        interval=1200
    )

    draw()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_simulation()
