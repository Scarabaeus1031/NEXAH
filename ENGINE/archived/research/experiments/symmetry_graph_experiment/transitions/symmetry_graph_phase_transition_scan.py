"""
NEXAH Symmetry Graph – Phase Transition Scan
--------------------------------------------

Scans coupling strength K and measures which dynamical
domain the symmetry graph ends up in.

Domains:

GLOBAL_LOCK
BIPOLAR
MULTI_CLUSTER
FRAGMENTED_PHASE

Outputs:
- console statistics
- phase transition plot
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx


# --------------------------------------------------
# Graph construction
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

def run_kuramoto(G, K, steps=2000, dt=0.05):

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

    return clusters


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
# Scan experiment
# --------------------------------------------------

def run_transition_scan(K_values, runs_per_K=20):

    G = build_symmetry_graph()

    domain_types = ["GLOBAL_LOCK","BIPOLAR","MULTI_CLUSTER","FRAGMENTED_PHASE"]

    results = {d:[] for d in domain_types}

    for K in K_values:

        counts = {d:0 for d in domain_types}

        for r in range(runs_per_K):

            theta, nodes = run_kuramoto(G, K)

            clusters = detect_clusters(theta, nodes)

            domain = classify_domain(clusters)

            counts[domain] += 1

        for d in domain_types:
            results[d].append(counts[d] / runs_per_K)

    return results


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_transition(K_values, results):

    plt.figure(figsize=(8,5))

    for domain,vals in results.items():
        plt.plot(K_values, vals, label=domain)

    plt.xlabel("Coupling K")
    plt.ylabel("Probability")
    plt.title("Symmetry Graph Phase Transition")
    plt.legend()

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nRunning Phase Transition Scan...\n")

    K_values = np.linspace(0.02, 0.35, 15)

    results = run_transition_scan(K_values)

    plot_transition(K_values, results)
