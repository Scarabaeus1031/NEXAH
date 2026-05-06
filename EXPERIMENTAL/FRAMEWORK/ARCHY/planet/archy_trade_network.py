from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import networkx as nx

from FRAMEWORK.ARCHY.planet.archy_real_cities import simulate_city_stability
from FRAMEWORK.ARCHY.planet.archy_population_model import CITY_POPULATION


# ---------------------------------------------------
# INITIAL ECONOMIC SIZE (rough relative values)
# ---------------------------------------------------

CITY_GDP = {
    "Frankfurt": 0.8,
    "Berlin": 0.9,
    "London": 3.2,
    "Paris": 2.8,

    "New York": 3.5,
    "Chicago": 1.7,
    "Los Angeles": 2.0,

    "Tokyo": 3.4,
    "Shanghai": 3.0,
    "Delhi": 1.8,

    "São Paulo": 1.7,
    "Buenos Aires": 1.1,

    "Cairo": 1.0,
    "Lagos": 0.8,

    "Sydney": 1.2,
    "Melbourne": 1.0,
}


# ---------------------------------------------------
# TRADE CONNECTIONS
# ---------------------------------------------------

TRADE_CONNECTIONS = [
    ("New York", "London"),
    ("London", "Frankfurt"),
    ("Frankfurt", "Paris"),
    ("Paris", "Berlin"),

    ("Tokyo", "Shanghai"),
    ("Shanghai", "Delhi"),
    ("Los Angeles", "Tokyo"),

    ("São Paulo", "Buenos Aires"),

    ("Cairo", "Lagos"),

    ("London", "New York"),
    ("Paris", "Tokyo"),
    ("Frankfurt", "Chicago"),
    ("Sydney", "Tokyo"),
]


# ---------------------------------------------------
# BUILD TRADE NETWORK
# ---------------------------------------------------

def build_trade_network(cities):

    G = nx.Graph()

    for name, lat, lon, stability, climate in cities:
        G.add_node(
            name,
            lat=lat,
            lon=lon,
            stability=stability,
            climate=climate,
            population=CITY_POPULATION.get(name, 1.0),
            gdp=CITY_GDP.get(name, 1.0),
        )

    for a, b in TRADE_CONNECTIONS:
        if a in G.nodes and b in G.nodes:
            G.add_edge(a, b)

    return G


# ---------------------------------------------------
# ECONOMIC DYNAMICS
# ---------------------------------------------------

def evolve_gdp(gdp, stability, population):

    base_growth = 0.01
    stability_bonus = (stability - 0.30) * 0.05
    population_pressure = min(population / 30.0, 1.0) * 0.01
    noise = np.random.normal(0, 0.005)

    new_gdp = gdp * (1 + base_growth + stability_bonus - population_pressure + noise)

    return max(0.2, new_gdp)


def trade_stress(gdp, neighbors_gdp):

    if not neighbors_gdp:
        return 0.0

    avg_partner_gdp = np.mean(neighbors_gdp)
    ratio = gdp / avg_partner_gdp if avg_partner_gdp > 0 else 1.0

    if ratio < 0.6:
        return -0.010

    if ratio < 0.8:
        return -0.005

    if ratio > 1.2:
        return 0.003

    return 0.0


def instability_trade_shock(stability):

    if stability < 0.28:
        return -0.015

    if stability < 0.30:
        return -0.008

    return 0.0


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_trade_simulation():

    cities = simulate_city_stability()
    G = build_trade_network(cities)

    fig = plt.figure(figsize=(12, 6))
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
            sizes.append(data["gdp"] * 120)
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

        ax.set_title(f"ARCHY Trade Network Simulator — {year}")

        return sc

    def update(frame):

        nonlocal year
        year += 10

        new_gdp = {}

        # 1) GDP evolution
        for city in G.nodes:
            data = G.nodes[city]

            new_gdp[city] = evolve_gdp(
                data["gdp"],
                data["stability"],
                data["population"]
            )

        for city in G.nodes:
            G.nodes[city]["gdp"] = new_gdp[city]

        # 2) Trade feedback into stability
        for city in G.nodes:
            neighbors = list(G.neighbors(city))
            neighbor_gdp = [G.nodes[n]["gdp"] for n in neighbors]

            ts = trade_stress(G.nodes[city]["gdp"], neighbor_gdp)
            shock = instability_trade_shock(G.nodes[city]["stability"])

            G.nodes[city]["stability"] += ts + shock
            G.nodes[city]["stability"] = max(0.25, min(0.40, G.nodes[city]["stability"]))

        print("Year:", year)

        weak = [c for c in G.nodes if G.nodes[c]["stability"] < 0.29]
        if weak:
            print("Trade-stressed cities:", weak)

        return draw()

    animation.FuncAnimation(
        fig,
        update,
        frames=20,
        interval=1200
    )

    draw()
    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_trade_simulation()
