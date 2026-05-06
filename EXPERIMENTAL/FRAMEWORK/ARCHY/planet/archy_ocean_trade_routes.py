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
# CHOKEPOINTS
# ---------------------------------------------------

CHOKEPOINTS = {

    "SUEZ": (30.0, 32.5),
    "PANAMA": (9.0, -79.5),
    "MALACCA": (2.5, 101.0),
    "HORMUZ": (26.5, 56.0),
    "GIBRALTAR": (36.0, -5.5)

}


# ---------------------------------------------------
# NETWORK
# ---------------------------------------------------

def build_ocean_network(cities, max_distance=5000):

    G = nx.DiGraph()

    for c in cities:

        G.add_node(
            c["name"],
            lat=c["lat"],
            lon=c["lon"],
            population=c["population"],
            stability=0.33
        )

    nodes = list(G.nodes)

    for i in range(len(nodes)):

        a = nodes[i]

        for j in range(i+1, len(nodes)):

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
# CHOKEPOINT IMPACT
# ---------------------------------------------------

def chokepoint_disruption(G):

    disruptions = []

    for name,(lat,lon) in CHOKEPOINTS.items():

        if np.random.random() < 0.05:

            disruptions.append(name)

            for a,b,data in G.edges(data=True):

                mid_lat = (G.nodes[a]["lat"] + G.nodes[b]["lat"])/2
                mid_lon = (G.nodes[a]["lon"] + G.nodes[b]["lon"])/2

                d = haversine(lat,lon,mid_lat,mid_lon)

                if d < 1200:

                    data["flow"] *= 0.5

    return disruptions


# ---------------------------------------------------
# SUPPLY IMPACT
# ---------------------------------------------------

def supply_effect(G):

    for city in G.nodes:

        incoming = 0

        for n in G.predecessors(city):

            incoming += G[n][city]["flow"]

        demand = G.nodes[city]["population"] * 0.6

        ratio = incoming/(demand+0.1)

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

def evolve_population(pop,stability):

    growth = 0.01
    stress = (0.34 - stability)*0.03

    noise = np.random.normal(0,0.003)

    return max(0.2,pop*(1+growth-stress+noise))


# ---------------------------------------------------
# DRAW
# ---------------------------------------------------

def draw(ax,G,year,disruptions):

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

    # draw trade routes
    for a,b,data in G.edges(data=True):

        if data["flow"] > 0.8:

            ax.plot(
                [G.nodes[a]["lon"],G.nodes[b]["lon"]],
                [G.nodes[a]["lat"],G.nodes[b]["lat"]],
                color="orange",
                linewidth=0.5,
                alpha=0.3,
                transform=ccrs.PlateCarree()
            )

    # draw chokepoints
    for name,(lat,lon) in CHOKEPOINTS.items():

        color = "red" if name in disruptions else "white"

        ax.scatter(
            lon,
            lat,
            s=60,
            color=color,
            transform=ccrs.PlateCarree()
        )

    ax.set_title(f"ARCHY Ocean Trade Routes — {year}")


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_ocean_network(cities)

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

        disruptions = chokepoint_disruption(G)

        supply_effect(G)

        unstable = [c for c in G.nodes if G.nodes[c]["stability"] < 0.29]

        print("Year:",year,"Unstable:",len(unstable),"Chokepoints:",disruptions)

        draw(ax,G,year,disruptions)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=30,
        interval=1200
    )

    draw(ax,G,year,[])

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run()
