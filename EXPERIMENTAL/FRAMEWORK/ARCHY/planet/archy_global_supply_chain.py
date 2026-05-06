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
# DISTANCE
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
# BUILD SUPPLY NETWORK
# ---------------------------------------------------

def build_supply_network(cities, max_distance=3500):

    G = nx.DiGraph()

    for c in cities:

        G.add_node(
            c["name"],
            lat=c["lat"],
            lon=c["lon"],
            population=c["population"],
            stability=0.33,
            industry=np.random.uniform(0.8,1.2),
            food=np.random.uniform(0.8,1.2),
            energy=np.random.uniform(0.8,1.2)
        )

    nodes = list(G.nodes)

    for i in range(len(nodes)):

        a = nodes[i]

        for j in range(i+1,len(nodes)):

            b = nodes[j]

            d = haversine(
                G.nodes[a]["lat"],
                G.nodes[a]["lon"],
                G.nodes[b]["lat"],
                G.nodes[b]["lon"]
            )

            if d < max_distance:

                flow = np.random.uniform(0.2,1.0)

                G.add_edge(a,b,flow=flow)
                G.add_edge(b,a,flow=flow)

    return G


# ---------------------------------------------------
# SUPPLY SHOCK
# ---------------------------------------------------

def supply_shock(G):

    for city in G.nodes:

        stability = G.nodes[city]["stability"]

        if stability < 0.28:

            for neighbor in G.successors(city):

                if "flow" in G[city][neighbor]:

                    G[city][neighbor]["flow"] *= 0.7


# ---------------------------------------------------
# ECONOMIC IMPACT
# ---------------------------------------------------

def supply_impact(G):

    for city in G.nodes:

        incoming = 0

        for neighbor in G.predecessors(city):

            incoming += G[neighbor][city]["flow"]

        demand = G.nodes[city]["population"] * 0.5

        ratio = incoming / (demand + 0.1)

        if ratio < 0.7:
            G.nodes[city]["stability"] -= 0.02

        elif ratio < 1.0:
            G.nodes[city]["stability"] -= 0.01

        elif ratio > 1.3:
            G.nodes[city]["stability"] += 0.003

        G.nodes[city]["stability"] = max(0.25,min(0.40,G.nodes[city]["stability"]))


# ---------------------------------------------------
# POPULATION
# ---------------------------------------------------

def evolve_population(pop, stability):

    growth = 0.01
    stress = (0.34 - stability)*0.03

    noise = np.random.normal(0,0.003)

    return max(0.2, pop*(1+growth-stress+noise))


# ---------------------------------------------------
# DRAW
# ---------------------------------------------------

def draw(ax,G,year):

    ax.clear()

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    lats=[]
    lons=[]
    sizes=[]
    stability=[]

    for city in G.nodes:

        d = G.nodes[city]

        lats.append(d["lat"])
        lons.append(d["lon"])
        sizes.append(d["population"]*2)
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

    # draw major supply routes
    for a,b,data in G.edges(data=True):

        if data["flow"] > 0.8:

            ax.plot(
                [G.nodes[a]["lon"],G.nodes[b]["lon"]],
                [G.nodes[a]["lat"],G.nodes[b]["lat"]],
                color="orange",
                linewidth=0.5,
                alpha=0.4,
                transform=ccrs.PlateCarree()
            )

    ax.set_title(f"ARCHY Global Supply Chain — {year}")


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_supply_network(cities)

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    year = 2025

    def update(frame):

        nonlocal year

        year += 10

        for city in G.nodes:

            pop = G.nodes[city]["population"]
            stab = G.nodes[city]["stability"]

            G.nodes[city]["population"] = evolve_population(pop,stab)

        supply_shock(G)

        supply_impact(G)

        unstable = [c for c in G.nodes if G.nodes[c]["stability"] < 0.29]

        print("Year:",year,"Unstable:",len(unstable))

        draw(ax,G,year)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=30,
        interval=1200
    )

    draw(ax,G,year)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run()
