"""
NEXAH Resilience Universal Architecture Generator

Constructs graph architectures predicted to have high resilience
based on the discovered spectral law and architecture DNA.

Target design principles discovered earlier:

nodes ≈ 4–6
high clustering
dense connectivity
λ₂ / λmax ≈ 1

The generator builds candidate graphs and evaluates their spectral
properties to see whether they fall into the resilience peak region.
"""

import networkx as nx
import numpy as np


TARGET_NODES = 5
TARGET_EDGES = 19


def spectral_ratio(G):

    UG = G.to_undirected()

    L = nx.laplacian_matrix(UG).toarray()

    eigvals = np.linalg.eigvals(L)
    eigvals = np.real(eigvals)
    eigvals.sort()

    if len(eigvals) < 2:
        return None

    lambda2 = eigvals[1]
    lambdamax = eigvals[-1]

    if lambdamax == 0:
        return None

    return lambda2 / lambdamax


def clustering(G):

    try:
        return nx.average_clustering(G)
    except Exception:
        return 0


def generate_candidate():

    G = nx.gnm_random_graph(TARGET_NODES, TARGET_EDGES)

    return G


def evaluate_graph(G):

    ratio = spectral_ratio(G)

    if ratio is None:
        return None

    cluster = clustering(G)

    score = 0.7 * ratio + 0.3 * cluster

    return score, ratio, cluster


def run():

    print("\nNEXAH Universal Architecture Generator")
    print("--------------------------------------")

    best_graph = None
    best_score = 0

    for i in range(200):

        G = generate_candidate()

        result = evaluate_graph(G)

        if result is None:
            continue

        score, ratio, cluster = result

        if score > best_score:

            best_score = score
            best_graph = G

            print("\nNew best architecture")
            print("---------------------")
            print("score =", round(score, 4))
            print("λ₂ / λmax =", round(ratio, 4))
            print("clustering =", round(cluster, 4))
            print("nodes =", G.number_of_nodes())
            print("edges =", G.number_of_edges())

    print("\nFinal best architecture")
    print("-----------------------")

    if best_graph:

        print("nodes =", best_graph.number_of_nodes())
        print("edges =", best_graph.number_of_edges())
        print("density =", nx.density(best_graph))
        print("clustering =", nx.average_clustering(best_graph))

    else:

        print("No architecture found.")


if __name__ == "__main__":
    run()
