"""
Symmetry Graph vs Star Graph Comparison
--------------------------------------

Compares synchronization speed between

1. Star graph (center + spokes)
2. Symmetry graph (center + C5 + C6 + C6)

Both graphs use 18 nodes.

Metric:
Kuramoto synchronization time (R > 0.95)
"""

import numpy as np
import networkx as nx

# -----------------------------
# Parameters
# -----------------------------

K = 1.5
dt = 0.05
T_MAX = 200
SYNC_THRESHOLD = 0.95
RUNS = 50


# -----------------------------
# Order parameter
# -----------------------------

def order_parameter(theta):
    return np.abs(np.mean(np.exp(1j * theta)))


# -----------------------------
# Kuramoto simulation
# -----------------------------

def simulate_kuramoto(G):

    nodes = list(G.nodes)
    N = len(nodes)

    theta = np.random.uniform(0, 2*np.pi, N)

    for step in range(int(T_MAX/dt)):

        dtheta = np.zeros(N)

        for i, node_i in enumerate(nodes):

            for j, node_j in enumerate(nodes):

                if G.has_edge(node_i, node_j):

                    dtheta[i] += np.sin(theta[j] - theta[i])

        theta += dt * K * dtheta

        R = order_parameter(theta)

        if R > SYNC_THRESHOLD:
            return step * dt

    return T_MAX


# -----------------------------
# Star graph
# -----------------------------

def star_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    for s in spokes:
        G.add_edge(center, s)

    return G


# -----------------------------
# Symmetry graph (5+6+6)
# -----------------------------

def symmetry_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    for s in spokes:
        G.add_edge(center, s)

    # C5
    pent = spokes[0:5]
    for i in range(5):
        G.add_edge(pent[i], pent[(i+1)%5])

    # C6
    hex1 = spokes[5:11]
    for i in range(6):
        G.add_edge(hex1[i], hex1[(i+1)%6])

    # C6
    hex2 = spokes[11:17]
    for i in range(6):
        G.add_edge(hex2[i], hex2[(i+1)%6])

    return G


# -----------------------------
# Run experiment
# -----------------------------

def run_experiment(name, graph_fn):

    times = []

    for _ in range(RUNS):

        G = graph_fn()
        t = simulate_kuramoto(G)

        times.append(t)

    mean = np.mean(times)
    std = np.std(times)

    print()
    print(name)
    print("mean sync time:", round(mean,2))
    print("std:", round(std,2))


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    print("Running star vs symmetry comparison")
    print("Runs per topology:", RUNS)

    run_experiment("Star Graph", star_graph)
    run_experiment("Symmetry Graph (5+6+6)", symmetry_graph)

    print()
    print("Experiment complete.")
