# ==========================================================
# NEXAH DASHBOARD
# Interactive interface for NEXAH simulations
# ==========================================================

import streamlit as st
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")

st.set_page_config(page_title="NEXAH Dashboard", layout="wide")

st.title("NEXAH System Dashboard")

# ----------------------------------------------------------
# LOAD SYSTEMS
# ----------------------------------------------------------

def list_systems():

    systems = []

    for f in os.listdir(SYSTEMS_DIR):
        if f.endswith(".json"):
            systems.append(f.replace(".json", ""))

    return systems


def load_system(name):

    path = os.path.join(SYSTEMS_DIR, f"{name}.json")

    with open(path) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(system):

    G = nx.DiGraph()

    states = system.get("states", [])
    transitions = system.get("transitions", {})

    for s in states:
        G.add_node(s)

    for src, tgt in transitions.items():
        G.add_edge(src, tgt)

    return G


# ----------------------------------------------------------
# DRAW GRAPH
# ----------------------------------------------------------

def draw_graph(G):

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="lightblue",
        arrows=True,
        ax=ax
    )

    st.pyplot(fig)


# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

systems = list_systems()

selected_system = st.sidebar.selectbox(
    "Select system",
    systems
)

steps = st.sidebar.slider(
    "Simulation steps",
    1,
    20,
    10
)

run_button = st.sidebar.button("Run Simulation")

# ----------------------------------------------------------
# SHOW SYSTEM STRUCTURE
# ----------------------------------------------------------

system = load_system(selected_system)

st.subheader("System Structure")

G = build_graph(system)

draw_graph(G)

# ----------------------------------------------------------
# SIMULATION
# ----------------------------------------------------------

if run_button:

    st.subheader("Simulation Walk")

    transitions = system.get("transitions", {})
    regimes = system.get("regimes", {})

    state = list(transitions.keys())[0]

    history = []

    for step in range(steps):

        regime = regimes.get(state, "UNKNOWN")

        history.append((step, state, regime))

        state = transitions.get(state, state)

    for step, state, regime in history:

        st.write(f"Step {step} — State: **{state}** ({regime})")
