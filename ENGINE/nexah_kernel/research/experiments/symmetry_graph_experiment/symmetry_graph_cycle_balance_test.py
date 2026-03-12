"""
Symmetry Graph Cycle Balance Test
---------------------------------

Tests whether the fast synchronization result is specific to

5 + 6 + 6 = 17

or whether other 3-cycle partitions of 17 nodes also produce
similar Kuramoto synchronization efficiency.

Compared partitions:

5 + 6 + 6
4 + 6 + 7
3 + 7 + 7
5 + 5 + 7
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

        for i, ni in enumerate(nodes):
            for j, nj in enumerate(nodes):

                if G.has_edge(ni, nj):
                    dtheta[i] += np.sin(theta[j] - theta[i])

        theta += dt * K * dtheta

        R = order_parameter(theta)

        if R > SYNC_THRESHOLD:
            return step * dt

    return T_MAX

# -----------------------------
# Build graph from cycle sizes
# -----------------------------

def build_cycle_graph(cycles):

    G = nx.Graph()

    center = "center"
    G.add_node(center)

    spokes = []
    idx = 0

    for size in cycles:

        cycle_nodes = []

        for _ in range(size):

            node = f"s{idx}"
            spokes.append(node)
            cycle_nodes.append(node)

            G.add_edge(center, node)

            idx += 1

        # connect cycle
        for i in range(size):
            G.add_edge(cycle_nodes[i], cycle_nodes[(i+1) % size])

    return G

# -----------------------------
# Experiment
# -----------------------------

def run_partition_test(name, cycles):

    times = []

    for _ in range(RUNS):

        G = build_cycle_graph(cycles)
        t = simulate_kuramoto(G)

        times.append(t)

    mean = np.mean(times)
    std = np.std(times)

    print()
    print(name)
    print("cycles:", cycles)
    print("mean sync time:", round(mean,2))
    print("std:", round(std,2))

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    print("Cycle Balance Synchronization Test")
    print("Runs per topology:", RUNS)

    run_partition_test("Balanced (5+6+6)", [5,6,6])
    run_partition_test("4+6+7", [4,6,7])
    run_partition_test("3+7+7", [3,7,7])
    run_partition_test("5+5+7", [5,5,7])

    print()
    print("Experiment complete.")
