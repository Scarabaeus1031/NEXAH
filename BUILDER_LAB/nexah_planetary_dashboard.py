# ==========================================================
# NEXAH PLANETARY DASHBOARD
# Interactive Global Cascade Simulator
# ==========================================================

import os
import json
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from nexah_planetary_engine import (
    load_network,
    build_graph,
    cascade_simulation
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "planetary_network.json")


# ----------------------------------------------------------
# LOAD NETWORK
# ----------------------------------------------------------

layers, nodes, edges = load_network(DATA_FILE)
G = build_graph(nodes, edges)


# ----------------------------------------------------------
# STREAMLIT CONFIG
# ----------------------------------------------------------

st.set_page_config(
    page_title="NEXAH Planetary Dashboard",
    layout="wide"
)

st.title("🌍 NEXAH Planetary Infrastructure Dashboard")


# ----------------------------------------------------------
# SIDEBAR CONTROLS
# ----------------------------------------------------------

st.sidebar.header("Simulation Controls")

start_node = st.sidebar.selectbox(
    "Initial Failure",
    list(G.nodes())
)

steps = st.sidebar.slider(
    "Simulation Steps",
    min_value=1,
    max_value=10,
    value=6
)

run = st.sidebar.button("Run Cascade Simulation")


# ----------------------------------------------------------
# NETWORK DRAW FUNCTION
# ----------------------------------------------------------

def draw_network(G, failed):

    pos = nx.spring_layout(G, seed=42)

    colors = []

    for node in G.nodes():

        if node in failed:
            colors.append("red")

        else:
            colors.append("skyblue")

    fig, ax = plt.subplots(figsize=(12,6))

    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=colors,
        node_size=2500,
        arrows=True
    )

    return fig


# ----------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------

if run:

    history = cascade_simulation(
        G,
        start_failed={start_node},
        steps=steps
    )

    st.subheader("Cascade Timeline")

    step = st.slider(
        "Select Simulation Step",
        0,
        len(history)-1,
        0
    )

    failed = history[step]

    st.write("Failed Systems:", list(failed))

    fig = draw_network(G, failed)

    st.pyplot(fig)


else:

    st.write("Select a starting failure and run the simulation.") 
