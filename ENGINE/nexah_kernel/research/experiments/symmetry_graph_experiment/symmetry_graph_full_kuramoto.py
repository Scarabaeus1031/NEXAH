"""
NEXAH Symmetry Graph – Full Kuramoto Network
--------------------------------------------

Simulates the full symmetry graph as a Kuramoto oscillator network.

Structure:

    dual hub core
    + C5 ring
    + C6 ring
    + C6 ring

Total ≈ 17 oscillators.

Goal:
observe phase synchronization and cluster formation.

Outputs:
- order parameter over time
- final phase distribution
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import math
import networkx as nx


# --------------------------------------------------
# Build symmetry graph
# --------------------------------------------------

def build_symmetry_graph():

    G = nx.Graph()

    # hubs
    G.add_node("hub_A")
    G.add_node("hub_B")

    G.add_edge("hub_A", "hub_B")

    # C5 ring
    C5 = [f"C5_{i}" for i in range(5)]
    for i in range(5):
        G.add_edge(C5[i], C5[(i + 1) % 5])

    # C6 ring A
    C6A = [f"C6A_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6A[i], C6A[(i + 1) % 6])

    # C6 ring B
    C6B = [f"C6B_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6B[i], C6B[(i + 1) % 6])

    # connect rings to hubs
    for n in C5:
        G.add_edge("hub_A", n)

    for n in C6A:
        G.add_edge("hub_A", n)

    for n in C6B:
        G.add_edge("hub_B", n)

    return G


# --------------------------------------------------
# Kuramoto simulation
# --------------------------------------------------

def run_kuramoto(G, K=0.3, steps=2000, dt=0.05):

    nodes = list(G.nodes())
    N = len(nodes)

    index = {n: i for i, n in enumerate(nodes)}

    theta = np.random.uniform(0, 2*np.pi, N)

    omega = np.random.normal(1.0, 0.05, N)

    adjacency = nx.to_numpy_array(G, nodelist=nodes)

    order_series = []

    for step in range(steps):

        dtheta = np.zeros(N)

        for i in range(N):

            coupling_sum = 0

            for j in range(N):

                if adjacency[i, j] > 0:
                    coupling_sum += math.sin(theta[j] - theta[i])

            dtheta[i] = omega[i] + K * coupling_sum

        theta = theta + dtheta * dt
        theta = np.mod(theta, 2*np.pi)

        # order parameter
        r = np.abs(np.sum(np.exp(1j*theta)))/N
        order_series.append(r)

    return theta, order_series, nodes


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def plot_results(theta, order_series, nodes):

    plt.figure(figsize=(12,5))

    # order parameter
    plt.subplot(1,2,1)
    plt.plot(order_series)
    plt.title("Global Synchronization (Order Parameter)")
    plt.xlabel("time step")
    plt.ylabel("R")

    # phase distribution
    plt.subplot(1,2,2)

    x = np.cos(theta)
    y = np.sin(theta)

    plt.scatter(x, y)

    for i, node in enumerate(nodes):
        plt.text(x[i]*1.05, y[i]*1.05, node, fontsize=8)

    circle = plt.Circle((0,0),1, fill=False)
    plt.gca().add_patch(circle)

    plt.title("Final Phase Distribution")

    plt.axis("equal")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nRunning Full Symmetry Graph Kuramoto Simulation...\n")

    G = build_symmetry_graph()

    print("Nodes:", len(G.nodes()))
    print("Edges:", len(G.edges()))

    theta, order_series, nodes = run_kuramoto(G)

    print("Final synchronization:", order_series[-1])

    plot_results(theta, order_series, nodes)
