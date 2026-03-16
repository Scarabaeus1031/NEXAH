from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability
from FRAMEWORK.ARCHY.planet.archy_population_model import CITY_POPULATION
from FRAMEWORK.ARCHY.planet.archy_energy_model import CITY_ENERGY_CAPACITY
from FRAMEWORK.ARCHY.planet.archy_trade_network import TRADE_CONNECTIONS, CITY_GDP


# ---------------------------------------------------
# BUILD CIVILIZATION NETWORK
# ---------------------------------------------------

def build_civilization(cities):

    G = nx.Graph()

    for name, lat, lon, stability, climate in cities:

        G.add_node(
            name,
            lat=lat,
            lon=lon,
            climate=climate,
            stability=stability,
            population=CITY_POPULATION.get(name, 1),
            energy=CITY_ENERGY_CAPACITY.get(name, 1),
            gdp=CITY_GDP.get(name, 1),
        )

    for a, b in TRADE_CONNECTIONS:

        if a in G.nodes and b in G.nodes:
            G.add_edge(a, b)

    return G


# ---------------------------------------------------
# POPULATION DYNAMICS
# ---------------------------------------------------

def evolve_population(pop, stability):

    growth = 0.01
    stress = (0.35 - stability) * 0.03

    noise = np.random.normal(0, 0.002)

    new_pop = pop * (1 + growth - stress + noise)

    return max(0.2, new_pop)


# ---------------------------------------------------
# ENERGY MODEL
# ---------------------------------------------------

def energy_demand(pop):

    return pop * 0.12


def evolve_energy(capacity):

    investment = 0.01
    decay = 0.004

    noise = np.random.normal(0, 0.003)

    return capacity * (1 + investment - decay + noise)


def energy_impact(demand, capacity):

    ratio = demand / capacity

    if ratio > 1.2:
        return -0.02

    if ratio > 1.0:
        return -0.01

    if ratio < 0.8:
        return 0.003

    return 0


# ---------------------------------------------------
# ECONOMIC MODEL
# ---------------------------------------------------

def evolve_gdp(gdp, stability):

    growth = 0.01
    stability_bonus = (stability - 0.30) * 0.05

    noise = np.random.normal(0, 0.005)

    new_gdp = gdp * (1 + growth + stability_bonus + noise)

    return max(0.2, new_gdp)


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
# CIVILIZATION SIMULATION
# ---------------------------------------------------

def run_civilization():

    cities = simulate_city_stability()

    G = build_civilization(cities)

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

            sizes.append(data["population"] * 15)
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

        for city in G.nodes:

            ax.text(
                G.nodes[city]["lon"] + 1,
                G.nodes[city]["lat"] + 1,
                city,
                fontsize=8
            )

        ax.set_title(f"ARCHY Civilization Simulator — {year}")

        return sc


    def update(frame):

        nonlocal year

        year += 10

        for city in G.nodes:

            data = G.nodes[city]

            # population
            pop = evolve_population(data["population"], data["stability"])

            # energy
            capacity = evolve_energy(data["energy"])
            demand = energy_demand(pop)

            energy_effect = energy_impact(demand, capacity)

            # economy
            gdp = evolve_gdp(data["gdp"], data["stability"])

            trade_effect = trade_feedback(G, city)

            # update state
            data["population"] = pop
            data["energy"] = capacity
            data["gdp"] = gdp

            data["stability"] += energy_effect + trade_effect
            data["stability"] = max(0.25, min(0.40, data["stability"]))

        print("Year:", year)

        weak = [c for c in G.nodes if G.nodes[c]["stability"] < 0.29]

        if weak:
            print("Unstable cities:", weak)

        return draw()


    anim = animation.FuncAnimation(
        fig,
        update,
        frames=25,
        interval=1200
    )

    draw()

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_civilization()
