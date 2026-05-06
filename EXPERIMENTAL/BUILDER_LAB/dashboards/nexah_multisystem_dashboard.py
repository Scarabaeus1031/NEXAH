# ==========================================================
# NEXAH MULTI-SYSTEM DASHBOARD
# Interactive simulation of coupled systems
# ==========================================================

import streamlit as st
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")

st.set_page_config(page_title="NEXAH Multi-System Dashboard", layout="wide")

st.title("NEXAH Multi-System Simulator")

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
# COUPLING RULES
# ----------------------------------------------------------

COUPLINGS = {

    ("climate_model", "S3_failure"): ("energy_grid", "S5_freq_drop"),

    ("energy_grid", "S11_blackout"): ("supply_chain", "S3_breakdown")

}


# ----------------------------------------------------------
# BUILD COUPLED GRAPH
# ----------------------------------------------------------

def build_graph(system_names):

    G = nx.DiGraph()

    for s in system_names:
        G.add_node(s)

    for (src_sys, _), (tgt_sys, _) in COUPLINGS.items():

        if src_sys in system_names and tgt_sys in system_names:

            G.add_edge(src_sys, tgt_sys)

    return G


# ----------------------------------------------------------
# SIMULATION
# ----------------------------------------------------------

def simulate(system_names, steps):

    systems = {}
    states = {}

    for name in system_names:

        system = load_system(name)

        systems[name] = system

        transitions = system.get("transitions", {})

        states[name] = list(transitions.keys())[0]


    history = []

    for step in range(steps):

        new_states = {}

        for name in states:

            system = systems[name]

            transitions = system.get("transitions", {})

            state = states[name]

            next_state = transitions.get(state, state)

            new_states[name] = next_state


        # apply couplings
        for (src_sys, src_state), (tgt_sys, tgt_state) in COUPLINGS.items():

            if src_sys in states and states[src_sys] == src_state:

                if tgt_sys in new_states:

                    new_states[tgt_sys] = tgt_state


        states = new_states

        history.append(states.copy())

    return history


# ----------------------------------------------------------
# DRAW SYSTEM GRAPH
# ----------------------------------------------------------

def draw_graph(G):

    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(6,4))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        arrows=True,
        ax=ax
    )

    st.pyplot(fig)


# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

systems = list_systems()

selected_systems = st.sidebar.multiselect(
    "Select systems",
    systems,
    default=systems
)

steps = st.sidebar.slider(
    "Simulation steps",
    1,
    20,
    10
)

run = st.sidebar.button("Run Simulation")


# ----------------------------------------------------------
# SHOW SYSTEM NETWORK
# ----------------------------------------------------------

if selected_systems:

    st.subheader("System Coupling Network")

    G = build_graph(selected_systems)

    draw_graph(G)


# ----------------------------------------------------------
# RUN SIMULATION
# ----------------------------------------------------------

if run:

    history = simulate(selected_systems, steps)

    st.subheader("Simulation Timeline")

    for step, states in enumerate(history):

        st.write(f"Step {step}")

        for system, state in states.items():

            st.write(f"{system} → {state}")

        st.write("---")
