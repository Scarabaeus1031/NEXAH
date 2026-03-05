# ==========================================================
# NEXAH INFRASTRUCTURE SIMULATOR
# Real-world infrastructure cascade simulation
# ==========================================================

import os
import json
import networkx as nx
import matplotlib.pyplot as plt
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INFRA_FILE = os.path.join(BASE_DIR, "global_systems", "real_infrastructure.json")


# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

def load_data():

    with open(INFRA_FILE) as f:
        return json.load(f)


# ----------------------------------------------------------
# BUILD GRAPH
# ----------------------------------------------------------

def build_graph(data):

    G = nx.DiGraph()

    for n in data["nodes"]:
        G.add_node(n)

    for src, tgt in data["edges"]:
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

        for node in failed:

            for neighbor in G.successors(node):

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

    plt.figure(figsize=(10,8))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=3000,
        arrows=True
    )

    plt.title("Infrastructure Cascade Simulation")

    plt.show()


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        help="initial infrastructure failure"
    )

    args = parser.parse_args()

    data = load_data()

    G = build_graph(data)

    history = simulate(G, args.start)

    for step, failed in enumerate(history):

        print("\nSTEP", step)
        print("Failed:", failed)

        draw_graph(G, failed)
