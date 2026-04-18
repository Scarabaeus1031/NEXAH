# ==========================================================
# NEXAH VISUALIZER
# Generate graph + animated walk from a NEXAH system JSON
# ==========================================================

import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import imageio.v2 as imageio


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMS_DIR = os.path.join(BASE_DIR, "systems")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")

os.makedirs(VISUALS_DIR, exist_ok=True)


# ----------------------------------------------------------
# COLOR BY REGIME
# ----------------------------------------------------------

def regime_color(regime):

    if regime == "STABLE":
        return "green"

    if regime == "STRESS":
        return "orange"

    if regime == "FAILURE":
        return "red"

    if regime == "COLLAPSE":
        return "black"

    return "gray"


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
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(system):

    states = system["states"]
    transitions = system["transitions"]

    G = nx.DiGraph()

    for s in states:
        G.add_node(s)

    for s, t in transitions.items():
        G.add_edge(s, t)

    return G


# ----------------------------------------------------------
# DRAW GRAPH PNG
# ----------------------------------------------------------

def draw_graph(system_name, G, system):

    regimes = system["regimes"]

    colors = []

    for node in G.nodes():
        r = regimes.get(node, "UNKNOWN")
        colors.append(regime_color(r))

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 6))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=1500,
        arrows=True
    )

    plt.title(f"NEXAH System Graph — {system_name}")

    path = os.path.join(VISUALS_DIR, f"{system_name}_graph.png")

    plt.savefig(path)
    plt.close()

    print("Graph saved:", path)

    return pos


# ----------------------------------------------------------
# CREATE ANIMATION
# ----------------------------------------------------------

def animate_walk(system_name, G, system, pos):

    transitions = system["transitions"]
    regimes = system["regimes"]

    frames = []

    state = list(transitions.keys())[0]

    for step in range(10):

        plt.figure(figsize=(12,6))

        colors = []

        for node in G.nodes():

            if node == state:
                colors.append("cyan")
            else:
                colors.append(regime_color(regimes.get(node, "UNKNOWN")))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=colors,
            node_size=1500,
            arrows=True
        )

        plt.title(f"NEXAH Walk — step {step} — state {state}")

        frame_path = os.path.join(VISUALS_DIR, f"frame_{step}.png")

        plt.savefig(frame_path)
        plt.close()

        frames.append(imageio.imread(frame_path))

        state = transitions.get(state, state)

    gif_path = os.path.join(VISUALS_DIR, f"{system_name}_walk.gif")

    imageio.mimsave(gif_path, frames, duration=1)

    print("Animation saved:", gif_path)


# ----------------------------------------------------------
# VISUALIZE SYSTEM
# ----------------------------------------------------------

def visualize(system_name):

    system = load_system(system_name)

    G = build_graph(system)

    pos = draw_graph(system_name, G, system)

    animate_walk(system_name, G, system, pos)


# ----------------------------------------------------------
# CLI ENTRY
# ----------------------------------------------------------

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="NEXAH System Visualizer"
    )

    parser.add_argument(
        "system",
        help="System name (JSON in systems folder)"
    )

    args = parser.parse_args()

    visualize(args.system)
