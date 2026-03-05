# ==========================================================
# NEXAH PLANETARY CONTROL ROOM (v2)
# Real world map + probabilistic cascades
# ==========================================================

import os
import sys
import random
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from nexah_planetary_engine import load_network, build_graph

DATA_FILE = os.path.join(BASE_DIR, "data", "planetary_network.json")

st.set_page_config(page_title="NEXAH Planetary Control Room", layout="wide")

st.title("🌍 NEXAH Planetary Control Room")

# ----------------------------------------------------------
# LOAD NETWORK
# ----------------------------------------------------------

layers, nodes, edges = load_network(DATA_FILE)
G = build_graph(nodes, edges)

# ----------------------------------------------------------
# LAYER COLORS
# ----------------------------------------------------------

LAYER_COLORS = {
    "space": "purple",
    "digital": "blue",
    "energy": "gold",
    "logistics": "orange",
    "food": "green",
    "water": "cyan",
    "finance": "red"
}

# ----------------------------------------------------------
# CASCADE ENGINE V2
# ----------------------------------------------------------

def simulate_cascade(G, start, steps=10, prob=0.6, recovery=0.1):

    failed = {start}
    history = [set(failed)]

    for step in range(steps):

        new_failed = set(failed)

        for node in list(failed):

            for dep in G.successors(node):

                if dep not in failed:

                    if random.random() < prob:
                        new_failed.add(dep)

        # recovery chance
        for node in list(new_failed):

            if node != start and random.random() < recovery:
                new_failed.remove(node)

        failed = new_failed
        history.append(set(failed))

    return history

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

st.sidebar.header("Simulation Controls")

start_node = st.sidebar.selectbox(
    "Initial Failure",
    list(G.nodes())
)

steps = st.sidebar.slider(
    "Simulation Steps",
    1,
    20,
    10
)

prob = st.sidebar.slider(
    "Cascade Probability",
    0.0,
    1.0,
    0.6
)

recovery = st.sidebar.slider(
    "Recovery Probability",
    0.0,
    0.5,
    0.1
)

run = st.sidebar.button("Run Simulation")

# ----------------------------------------------------------
# MAP DRAW
# ----------------------------------------------------------

def draw_map(G, failed):

    fig = plt.figure(figsize=(14,7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_global()

    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, alpha=0.3)
    ax.add_feature(cfeature.OCEAN)

    pos = nx.get_node_attributes(G, "meta")

    # edges
    for src, tgt in G.edges():

        lat1 = pos[src].get("lat",0)
        lon1 = pos[src].get("lon",0)

        lat2 = pos[tgt].get("lat",0)
        lon2 = pos[tgt].get("lon",0)

        ax.plot(
            [lon1, lon2],
            [lat1, lat2],
            color="black",
            linewidth=1,
            transform=ccrs.PlateCarree()
        )

    # nodes
    for node in G.nodes():

        meta = pos[node]
        lat = meta.get("lat",0)
        lon = meta.get("lon",0)

        layer = G.nodes[node]["layer"]

        color = LAYER_COLORS.get(layer,"gray")

        if node in failed:
            color = "red"

        ax.scatter(
            lon,
            lat,
            color=color,
            s=120,
            transform=ccrs.PlateCarree()
        )

        ax.text(
            lon+1,
            lat+1,
            node,
            fontsize=8,
            transform=ccrs.PlateCarree()
        )

    return fig

# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

if run:

    history = simulate_cascade(G, start_node, steps, prob, recovery)

    step = st.slider(
        "Simulation Step",
        0,
        len(history)-1,
        0
    )

    failed = history[step]

    st.write("Failed systems:", list(failed))

    fig = draw_map(G, failed)

    st.pyplot(fig)

else:

    st.info("Select a starting failure and run the simulation.")
