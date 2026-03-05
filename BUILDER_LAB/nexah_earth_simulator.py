# ==========================================================
# NEXAH EARTH INFRASTRUCTURE SIMULATOR
# Visualize cascades on a world map
# ==========================================================

import os
import json
import networkx as nx
import matplotlib.pyplot as plt

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

def draw(G, failed):

    pos = nx.get_node_attributes(G, "pos")

    colors = []

    for n in G.nodes():

        if n in failed:
            colors.append("red")
        else:
            colors.append("skyblue")

    plt.figure(figsize=(12,6))

    nx.draw(
        G,
        pos,
        node_color=colors,
        with_labels=True,
        node_size=2500,
        arrows=True
    )

    plt.title("NEXAH Earth Infrastructure Network")

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

    draw(G, failed)
