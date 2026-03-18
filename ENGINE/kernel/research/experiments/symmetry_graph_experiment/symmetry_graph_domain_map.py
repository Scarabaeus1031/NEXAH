"""
NEXAH Symmetry Graph – Domain Map
---------------------------------

Runs many Kuramoto simulations on the symmetry graph and builds a
statistical map of emergent dynamical domains.

It summarizes how often the system ends in:

- GLOBAL_LOCK
- BIPOLAR
- MULTI_CLUSTER
- FRAGMENTED_PHASE

This is a statistical regime/domain map built from repeated runs.

Outputs:
- console summary
- bar chart of domain frequencies
- histogram of cluster counts
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx
import random


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
        G.add_edge(C5[i], C5[(i+1) % 5])

    # C6A ring
    C6A = [f"C6A_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6A[i], C6A[(i+1) % 6])

    # C6B ring
    C6B = [f"C6B_{i}" for i in range(6)]
    for i in range(6):
        G.add_edge(C6B[i], C6B[(i+1) % 6])

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

    theta = np.random.uniform(0, 2*np.pi, N)
    omega = np.random.normal(1.0, 0.08, N)

    adjacency = nx.to_numpy_array(G, nodelist=nodes)

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

    return theta, nodes


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

    named_clusters = [[nodes[i] for i in cluster] for cluster in clusters]

    return clusters, named_clusters


# --------------------------------------------------
# Domain classification
# --------------------------------------------------

def classify_domain(clusters):

    n = len(clusters)

    if n == 1:
        return "GLOBAL_LOCK"

    if n == 2:
        return "BIPOLAR"

    if 3 <= n <= 4:
        return "MULTI_CLUSTER"

    return "FRAGMENTED_PHASE"


# --------------------------------------------------
# Domain statistics experiment
# --------------------------------------------------

def run_domain_experiment(runs=100):

    G = build_symmetry_graph()

    domain_counts = {
        "GLOBAL_LOCK":0,
        "BIPOLAR":0,
        "MULTI_CLUSTER":0,
        "FRAGMENTED_PHASE":0
    }

    cluster_counts = []

    for r in range(runs):

        theta, nodes = run_kuramoto(G)

        clusters, named = detect_clusters(theta, nodes)

        domain = classify_domain(clusters)

        domain_counts[domain] += 1

        cluster_counts.append(len(clusters))

    return domain_counts, cluster_counts


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def plot_results(domain_counts, cluster_counts):

    plt.figure(figsize=(12,5))

    # domain frequency
    plt.subplot(1,2,1)

    names = list(domain_counts.keys())
    values = list(domain_counts.values())

    plt.bar(names, values)
    plt.title("Domain Frequency")
    plt.xticks(rotation=20)

    # cluster histogram
    plt.subplot(1,2,2)

    plt.hist(cluster_counts, bins=range(1,10), align="left")
    plt.xlabel("Number of clusters")
    plt.ylabel("Frequency")
    plt.title("Cluster Count Distribution")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nRunning Symmetry Graph Domain Map Experiment...\n")

    domain_counts, cluster_counts = run_domain_experiment(runs=100)

    print("Domain statistics:\n")

    for k,v in domain_counts.items():
        print(k,":",v)

    plot_results(domain_counts, cluster_counts)
