# ==========================================================
# NEXAH EARTH INFRASTRUCTURE SIMULATOR
# Cascades on a real world map
# ==========================================================

import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "global_systems",
    "infrastructure_geo.json"
)

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

def load_data():

    with open(DATA_FILE) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(data):

    G = nx.DiGraph()

    for node, pos in data["nodes"].items():
        G.add_node(node, pos=pos)

    for src, tgt in data["edges"]:
        G.add_edge(src, tgt)

    return G


# ----------------------------------------------------------
# CASCADE
# ----------------------------------------------------------

def simulate(G, start):

    failed = set([start])
    history = []

    while True:

        history.append(failed.copy())

        new_fail = set()

        for n in failed:

            for m in G.successors(n):

                if m not in failed:
                    new_fail.add(m)

        if not new_fail:
            break

        failed.update(new_fail)

    return history


# ----------------------------------------------------------
# DRAW MAP
# ----------------------------------------------------------

def draw_map(G, failed):

    pos = nx.get_node_attributes(G, "pos")

    fig = plt.figure(figsize=(12,6))

    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_global()

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, alpha=0.3)
    ax.add_feature(cfeature.OCEAN)

    # draw edges
    for src, tgt in G.edges():

        x1, y1 = pos[src]
        x2, y2 = pos[tgt]

        ax.plot(
            [x1, x2],
            [y1, y2],
            transform=ccrs.PlateCarree(),
            color="black"
        )

    # draw nodes
    for node, (x, y) in pos.items():

        if node in failed:
            color = "red"
        else:
            color = "skyblue"

        ax.scatter(
            x,
            y,
            color=color,
            s=200,
            transform=ccrs.PlateCarree()
        )

        ax.text(
            x+2,
            y+2,
            node,
            transform=ccrs.PlateCarree()
        )

    plt.title("NEXAH Global Infrastructure Cascade")

    plt.show()


# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------

data = load_data()

G = build_graph(data)

history = simulate(G, "satellites")

for step, failed in enumerate(history):

    print("\nSTEP", step)
    print("FAILED:", failed)

    draw_map(G, failed)
