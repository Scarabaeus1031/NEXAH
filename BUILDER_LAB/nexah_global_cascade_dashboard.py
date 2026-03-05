# ==========================================================
# NEXAH GLOBAL CASCADE DASHBOARD
# Interactive visualization of cascading global systems
# ==========================================================

import streamlit as st
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_FILE = os.path.join(BASE_DIR, "global_systems", "global_system_map.json")

st.set_page_config(page_title="NEXAH Global Cascade", layout="wide")

st.title("NEXAH Global Cascade Simulator")

# ----------------------------------------------------------
# LOAD GLOBAL MAP
# ----------------------------------------------------------

def load_map():

    with open(MAP_FILE) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(data):

    G = nx.DiGraph()

    for s in data["systems"]:
        G.add_node(s)

    for src, tgt in data["couplings"]:
        G.add_edge(src, tgt)

    return G


# ----------------------------------------------------------
# CASCADE SIMULATION
# ----------------------------------------------------------

def simulate(G, start):

    failed = set([start])

    history = []

    while True:

        history.append(failed.copy())

        new_failures = set()

        for system in failed:

            for neighbor in G.successors(system):

                if neighbor not in failed:
                    new_failures.add(neighbor)

        if not new_failures:
            break

        failed.update(new_failures)

    return history


# ----------------------------------------------------------
# DRAW GRAPH
# ----------------------------------------------------------

def draw_graph(G, failed):

    pos = nx.spring_layout(G, seed=42)

    colors = []

    for node in G.nodes():

        if node in failed:
            colors.append("red")
        else:
            colors.append("lightblue")

    fig, ax = plt.subplots(figsize=(8,6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=3000,
        arrows=True,
        ax=ax
    )

    st.pyplot(fig)


# ----------------------------------------------------------
# UI
# ----------------------------------------------------------

data = load_map()

systems = data["systems"]

G = build_graph(data)

start_system = st.sidebar.selectbox(
    "Initial Failure",
    systems
)

run = st.sidebar.button("Run Cascade Simulation")


# ----------------------------------------------------------
# SHOW NETWORK
# ----------------------------------------------------------

st.subheader("Global System Network")

draw_graph(G, set())


# ----------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------

if run:

    history = simulate(G, start_system)

    st.subheader("Cascade Simulation")

    for step, failed in enumerate(history):

        st.write(f"Step {step}")

        draw_graph(G, failed)
