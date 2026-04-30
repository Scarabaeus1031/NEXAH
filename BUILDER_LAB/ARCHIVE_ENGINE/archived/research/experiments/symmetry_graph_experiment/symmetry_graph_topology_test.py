"""
Symmetry Graph Topology Test
----------------------------

Compares synchronization stability of three graph topologies
with identical node count (17 nodes):

1. Random graph
2. Ring graph
3. Symmetry graph (C5 + C6 + C6)

Metric:
Synchronization time (R > 0.95)

Runs multiple simulations and reports statistics.
"""

import numpy as np
import networkx as nx

# -----------------------------
# Kuramoto parameters
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

    N = len(G.nodes)
    theta = np.random.uniform(0, 2*np.pi, N)

    nodes = list(G.nodes)

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
# Graph A — Random
# -----------------------------

def random_graph():

    G = nx.gnm_random_graph(17, 30)

    mapping = {i: f"n{i}" for i in range(17)}
    return nx.relabel_nodes(G, mapping)


# -----------------------------
# Graph B — Ring
# -----------------------------

def ring_graph():

    G = nx.cycle_graph(17)

    mapping = {i: f"n{i}" for i in range(17)}
    return nx.relabel_nodes(G, mapping)


# -----------------------------
# Graph C — Symmetry (5+6+6)
# -----------------------------

def symmetry_graph():

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = [f"s{i}" for i in range(17)]

    for s in spokes:
        G.add_edge(center, s)

    # pentagon
    pent = spokes[0:5]
    for i in range(5):
        G.add_edge(pent[i], pent[(i+1)%5])

    # hexagon 1
    hex1 = spokes[5:11]
    for i in range(6):
        G.add_edge(hex1[i], hex1[(i+1)%6])

    # hexagon 2
    hex2 = spokes[11:17]
    for i in range(6):
        G.add_edge(hex2[i], hex2[(i+1)%6])

    return G


# -----------------------------
# Run experiment
# -----------------------------

def run_experiment(name, graph_fn):

    times = []

    for i in range(RUNS):

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

    print("Running topology comparison...")
    print("Runs per topology:", RUNS)

    run_experiment("Random Graph", random_graph)
    run_experiment("Ring Graph", ring_graph)
    run_experiment("Symmetry Graph (5+6+6)", symmetry_graph)

    print()
    print("Experiment complete.")
