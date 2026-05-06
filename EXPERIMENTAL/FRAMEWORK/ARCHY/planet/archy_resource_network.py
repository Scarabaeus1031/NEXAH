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
# NETWORK
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
            food=np.random.uniform(0.8,1.2),
            water=np.random.uniform(0.8,1.2),
            energy=np.random.uniform(0.8,1.2)
        )

    city_list = list(G.nodes)

    for i in range(len(city_list)):

        a = city_list[i]

        lat1 = G.nodes[a]["lat"]
        lon1 = G.nodes[a]["lon"]

        for j in range(i+1,len(city_list)):

            b = city_list[j]

            lat2 = G.nodes[b]["lat"]
            lon2 = G.nodes[b]["lon"]

            d = haversine(lat1,lon1,lat2,lon2)

            if d < max_distance:
                G.add_edge(a,b)

    return G


# ---------------------------------------------------
# RESOURCE DEMAND
# ---------------------------------------------------

def resource_demand(pop):

    food = pop * 0.12
    water = pop * 0.10
    energy = pop * 0.11

    return food, water, energy


# ---------------------------------------------------
# RESOURCE UPDATE
# ---------------------------------------------------

def evolve_resources(value):

    growth = 0.01
    decay = 0.008

    noise = np.random.normal(0,0.01)

    return max(0.2, value*(1+growth-decay+noise))


# ---------------------------------------------------
# RESOURCE STRESS
# ---------------------------------------------------

def resource_impact(demand, supply):

    ratio = demand / supply

    if ratio > 1.4:
        return -0.03

    if ratio > 1.2:
        return -0.015

    if ratio < 0.8:
        return 0.004

    return 0


# ---------------------------------------------------
# DRAW
# ---------------------------------------------------

def draw_map(ax,G,year):

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

        data = G.nodes[city]

        lats.append(data["lat"])
        lons.append(data["lon"])
        sizes.append(data["population"]*2)
        stability.append(data["stability"])

    sc=ax.scatter(
        lons,
        lats,
        c=stability,
        s=sizes,
        cmap="viridis",
        transform=ccrs.PlateCarree(),
        vmin=0.25,
        vmax=0.40
    )

    ax.set_title(f"ARCHY Resource Network — {year}")

    return sc


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run_simulation():

    cities = generate_global_city_dataset()

    G = build_network(cities)

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    year = 2025

    def update(frame):

        nonlocal year

        year += 10

        for city in G.nodes:

            data = G.nodes[city]

            pop = data["population"]

            food_d, water_d, energy_d = resource_demand(pop)

            data["food"] = evolve_resources(data["food"])
            data["water"] = evolve_resources(data["water"])
            data["energy"] = evolve_resources(data["energy"])

            impact = (
                resource_impact(food_d,data["food"]) +
                resource_impact(water_d,data["water"]) +
                resource_impact(energy_d,data["energy"])
            )

            data["stability"] += impact + np.random.normal(0,0.002)

            data["stability"] = max(0.25,min(0.40,data["stability"]))

        unstable = [c for c in G.nodes if G.nodes[c]["stability"]<0.29]

        print("Year:",year)

        if unstable:
            print("Unstable cities:",len(unstable))

        return draw_map(ax,G,year)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=30,
        interval=1200
    )

    draw_map(ax,G,year)

    plt.show()


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

if __name__ == "__main__":

    run_simulation()
