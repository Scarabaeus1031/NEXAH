"""
NEXAH Symmetry Graph – Cluster Map
----------------------------------

Runs the Kuramoto simulation on the symmetry graph
and automatically detects phase clusters.

Clusters are determined via simple phase-distance grouping.

Outputs:

- order parameter plot
- colored cluster map on phase circle
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

    # connect rings
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

def run_kuramoto(G, K=0.12, steps=2500, dt=0.05):

    nodes = list(G.nodes())
    N = len(nodes)

    index = {n: i for i, n in enumerate(nodes)}

    theta = np.random.uniform(0, 2*np.pi, N)

    omega = np.random.normal(1.0, 0.08, N)

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

        r = np.abs(np.sum(np.exp(1j*theta))) / N
        order_series.append(r)

    return theta, order_series, nodes


# --------------------------------------------------
# Cluster detection
# --------------------------------------------------

def detect_clusters(theta, nodes, threshold=0.25):

    clusters = []
    used = set()

    for i in range(len(theta)):

        if i in used:
            continue

        cluster = [i]

        for j in range(len(theta)):

            if i == j:
                continue

            d = abs(np.angle(np.exp(1j*(theta[i]-theta[j]))))

            if d < threshold:
                cluster.append(j)

        for c in cluster:
            used.add(c)

        clusters.append(cluster)

    # convert index to node names
    named_clusters = []

    for cluster in clusters:
        named_clusters.append([nodes[i] for i in cluster])

    return clusters, named_clusters


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def plot_cluster_map(theta, nodes, clusters, order_series):

    plt.figure(figsize=(12,5))

    # order parameter
    plt.subplot(1,2,1)

    plt.plot(order_series)
    plt.title("Global Synchronization R(t)")
    plt.xlabel("time step")
    plt.ylabel("R")

    # cluster circle
    plt.subplot(1,2,2)

    colors = plt.cm.tab10(np.linspace(0,1,len(clusters)))

    for c,cluster in enumerate(clusters):

        for i in cluster:

            x = np.cos(theta[i])
            y = np.sin(theta[i])

            plt.scatter(x, y, color=colors[c], s=80)

            plt.text(x*1.07, y*1.07, nodes[i], fontsize=8)

    circle = plt.Circle((0,0),1, fill=False)
    plt.gca().add_patch(circle)

    plt.axis("equal")

    plt.title("Phase Cluster Map")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nRunning Symmetry Graph Cluster Detection...\n")

    G = build_symmetry_graph()

    print("Nodes:", len(G.nodes()))
    print("Edges:", len(G.edges()))

    theta, order_series, nodes = run_kuramoto(G)

    clusters, named_clusters = detect_clusters(theta, nodes)

    print("\nDetected clusters:\n")

    for c in named_clusters:
        print(c)

    plot_cluster_map(theta, nodes, clusters, order_series)
