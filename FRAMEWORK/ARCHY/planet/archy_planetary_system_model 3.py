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
                G.add_edge(a,b)

    return G


# ---------------------------------------------------
# POPULATION
# ---------------------------------------------------

def evolve_population(pop, stability):

    growth = 0.01
    stress = (0.34 - stability)*0.03

    noise = np.random.normal(0,0.003)

    return max(0.2, pop*(1+growth-stress+noise))


# ---------------------------------------------------
# RESOURCES
# ---------------------------------------------------

def resource_demand(pop):

    food = pop*0.12
    water = pop*0.10
    energy = pop*0.11

    return food,water,energy


def evolve_resource(v):

    return max(0.2, v*(1+np.random.normal(0.002,0.01)))


def resource_impact(demand,supply):

    ratio = demand/supply

    if ratio>1.4:
        return -0.03

    if ratio>1.2:
        return -0.015

    if ratio<0.8:
        return 0.004

    return 0


# ---------------------------------------------------
# MIGRATION
# ---------------------------------------------------

def migration(G):

    flows={}

    for city in G.nodes:

        stability = G.nodes[city]["stability"]

        if stability<0.29:

            neighbors=list(G.neighbors(city))

            if not neighbors:
                continue

            migrants = G.nodes[city]["population"]*0.02

            flows[city]=-migrants

            per = migrants/len(neighbors)

            for n in neighbors:
                flows[n]=flows.get(n,0)+per

    return flows


# ---------------------------------------------------
# CONFLICT RISK
# ---------------------------------------------------

def conflict_risk(G):

    conflicts=[]

    for a,b in G.edges:

        s1=G.nodes[a]["stability"]
        s2=G.nodes[b]["stability"]

        if s1<0.28 and s2<0.28:

            if np.random.random()<0.05:

                conflicts.append((a,b))

    return conflicts


# ---------------------------------------------------
# DRAW
# ---------------------------------------------------

def draw(ax,G,year,conflicts):

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

        d=G.nodes[city]

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

    for a,b in conflicts:

        ax.plot(
            [G.nodes[a]["lon"],G.nodes[b]["lon"]],
            [G.nodes[a]["lat"],G.nodes[b]["lat"]],
            color="red",
            linewidth=1,
            transform=ccrs.PlateCarree()
        )

    ax.set_title(f"ARCHY Planetary System Model — {year}")


# ---------------------------------------------------
# SIMULATION
# ---------------------------------------------------

def run():

    cities = generate_global_city_dataset()

    G = build_network(cities)

    fig = plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    year=2025

    def update(frame):

        nonlocal year

        year+=10

        for city in G.nodes:

            d=G.nodes[city]

            pop=evolve_population(d["population"],d["stability"])

            food_d,water_d,energy_d = resource_demand(pop)

            d["food"]=evolve_resource(d["food"])
            d["water"]=evolve_resource(d["water"])
            d["energy"]=evolve_resource(d["energy"])

            impact=(
                resource_impact(food_d,d["food"])+
                resource_impact(water_d,d["water"])+
                resource_impact(energy_d,d["energy"])
            )

            d["stability"]+=impact+np.random.normal(0,0.002)

            d["stability"]=max(0.25,min(0.40,d["stability"]))

            d["population"]=pop

        flows=migration(G)

        for c,v in flows.items():

            G.nodes[c]["population"]+=v

        conflicts = conflict_risk(G)

        print("Year:",year,"Conflicts:",len(conflicts))

        draw(ax,G,year,conflicts)

    anim=animation.FuncAnimation(
        fig,
        update,
        frames=30,
        interval=1200
    )

    draw(ax,G,year,[])

    plt.show()


if __name__=="__main__":

    run()
