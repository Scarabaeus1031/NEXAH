"""
NEXAH Symmetry Graph – 3 Cycle Kuramoto Vortices
------------------------------------------------

Graph structure:

center node
17 spokes

Cycle layers:
C5  (pentagon)
C6  (hexagon A)
C6  (hexagon B)

Partition:
5 + 6 + 6 = 17

This script:
• builds the graph
• simulates Kuramoto dynamics
• analyzes cycle windings
• plots final phase state with detected vortices
"""

import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from core.symmetry_graph_vortex_detector import wrap_phase, phase_winding


# -------------------------
# Build Graph
# -------------------------

def build_graph():
    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    # center connections
    for s in spokes:
        G.add_edge(center, s)

    # C5 pentagon
    pentagon = spokes[0:5]
    for i in range(5):
        G.add_edge(pentagon[i], pentagon[(i + 1) % 5])

    # C6 hexagon A
    hexagon1 = spokes[5:11]
    for i in range(6):
        G.add_edge(hexagon1[i], hexagon1[(i + 1) % 6])

    # C6 hexagon B
    hexagon2 = spokes[11:17]
    for i in range(6):
        G.add_edge(hexagon2[i], hexagon2[(i + 1) % 6])

    return G


# -------------------------
# Layout
# -------------------------

def layout_graph(G):

    pos = {}

    center = "center"
    pos[center] = (0, 0)

    radius = 3

    spokes = [n for n in G.nodes() if n != center]

    for i, node in enumerate(spokes):

        angle = 2 * math.pi * i / len(spokes)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        pos[node] = (x, y)

    return pos


# -------------------------
# Kuramoto Simulation
# -------------------------

def kuramoto_simulation(G, steps=500, dt=0.05, K=1.0):

    nodes = list(G.nodes())
    n = len(nodes)

    index = {node: i for i, node in enumerate(nodes)}

    theta = np.random.rand(n) * 2 * np.pi
    omega = np.zeros(n)

    for step in range(steps):

        dtheta = np.zeros(n)

        for i, node_i in enumerate(nodes):

            coupling = 0

            for node_j in G.neighbors(node_i):

                j = index[node_j]

                coupling += np.sin(theta[j] - theta[i])

            dtheta[i] = omega[i] + K * coupling

        theta += dt * dtheta
        theta = np.mod(theta, 2 * np.pi)

    return nodes, theta


# -------------------------
# Cycle Analysis
# -------------------------

def analyze_cycles(G, nodes, theta):

    theta_map = {node: theta[i] for i, node in enumerate(nodes)}

    cycles = nx.cycle_basis(G)

    results = []

    for cycle in cycles:

        phases = np.array([theta_map[n] for n in cycle])

        w = phase_winding(phases, list(range(len(cycle))))

        results.append((cycle, w))

    return results


# -------------------------
# Plot
# -------------------------

def draw_graph(G, nodes, theta, results):

    pos = layout_graph(G)

    theta_map = {node: theta[i] for i, node in enumerate(nodes)}

    node_colors = [theta_map[n] for n in G.nodes()]

    plt.figure(figsize=(8, 8))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=500,
        node_color=node_colors,
        cmap=plt.cm.hsv
    )

    nx.draw_networkx_edges(G, pos, width=1.8)
    nx.draw_networkx_labels(G, pos, font_size=9)

    for cycle, w in results:

        if abs(w) > 0.5:

            xs = [pos[n][0] for n in cycle]
            ys = [pos[n][1] for n in cycle]

            cx = np.mean(xs)
            cy = np.mean(ys)

            if w > 0:
                color = "red"
                label = "V"
            else:
                color = "blue"
                label = "A"

            plt.scatter(cx, cy, s=400, color=color, edgecolors="black", zorder=5)
            plt.text(cx, cy, label, color="white", ha="center", va="center")

    plt.title("NEXAH Kuramoto – Cycle Vortex Analysis")

    plt.axis("off")

    plt.tight_layout()

    plt.savefig("kuramoto_vortex_result.png", dpi=300)

    plt.show()


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    G = build_graph()

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    nodes, theta = kuramoto_simulation(G)

    results = analyze_cycles(G, nodes, theta)

    print("\nCycle analysis:")

    for cycle, w in results:
        print("cycle:", cycle, "winding:", round(w, 3))

    draw_graph(G, nodes, theta, results)
