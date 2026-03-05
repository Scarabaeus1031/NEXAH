# ==========================================================
# NEXAH CASCADE VISUALIZER
# Visualize cascading failures across coupled systems
# ==========================================================

import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import argparse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")

os.makedirs(VISUALS_DIR, exist_ok=True)


# ----------------------------------------------------------
# COUPLING RULES
# ----------------------------------------------------------

COUPLINGS = {

    ("climate_model", "S3_failure"): ("energy_grid", "S5_freq_drop"),

    ("energy_grid", "S11_blackout"): ("supply_chain", "S3_breakdown")

}


# ----------------------------------------------------------
# LOAD SYSTEM
# ----------------------------------------------------------

def load_system(name):

    path = os.path.join(SYSTEMS_DIR, f"{name}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"System not found: {name}")

    with open(path) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD CASCADE GRAPH
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
# INITIAL STATES
# ----------------------------------------------------------

def initialize_states(system_names):

    states = {}
    systems = {}

    for name in system_names:

        system = load_system(name)

        systems[name] = system

        transitions = system.get("transitions", {})

        if transitions:
            states[name] = list(transitions.keys())[0]
        else:
            states[name] = system["states"][0]

    return systems, states


# ----------------------------------------------------------
# SIMULATE CASCADE
# ----------------------------------------------------------

def simulate(system_names, steps=10):

    systems, states = initialize_states(system_names)

    G = build_graph(system_names)

    pos = nx.spring_layout(G, seed=42)

    frames = []

    for step in range(steps):

        new_states = {}

        # normal transitions
        for name in system_names:

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


        # -----------------------------
        # DRAW GRAPH FRAME
        # -----------------------------

        plt.figure(figsize=(8,6))

        colors = []

        for node in G.nodes():

            if "failure" in states[node] or "breakdown" in states[node]:
                colors.append("red")

            elif "stress" in states[node]:
                colors.append("orange")

            else:
                colors.append("green")


        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=2500,
            arrows=True
        )

        plt.title(f"NEXAH Cascade Simulation — step {step}")

        frame_path = os.path.join(VISUALS_DIR, f"cascade_frame{step}.png")

        plt.savefig(frame_path)

        frames.append(imageio.imread(frame_path))

        plt.close()


    gif_path = os.path.join(VISUALS_DIR, "nexah_cascade.gif")

    imageio.mimsave(gif_path, frames, duration=1)

    print("\nCascade animation saved:", gif_path)


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

if name == "main":

    parser = argparse.ArgumentParser(
        description="NEXAH Cascade Visualizer"
    )

    parser.add_argument(
        "--systems",
        nargs="+",
        help="Systems to visualize"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=10
    )

    args = parser.parse_args()

    if args.systems:

        simulate(args.systems, args.steps)

    else:

        print("\nUsage:")
        print("python nexah_cascade_visualizer.py --systems energy_grid climate_model supply_chain")
