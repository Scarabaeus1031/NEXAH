"""
NEXAH Resilience Spectral Analyzer

Analyzes spectral properties of network architectures and compares
them with measured resilience.

Spectral quantities analyzed:

- adjacency spectral radius
- algebraic connectivity (Laplacian λ2)
- largest Laplacian eigenvalue
- spectral gap proxy

These values often correlate with stability and robustness
in complex networks.
"""

import os
import json
import statistics
import networkx as nx
import numpy as np

RESULT_DIR = "results"


def load_graphs():

    graphs = []

    if not os.path.exists(RESULT_DIR):
        return graphs

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        try:

            with open(path) as file:
                r = json.load(file)

            if "nodes" not in r:
                continue

            nodes = r["nodes"]
            edges = r["edges"]
            resilience = r["resilience_score"]

            G = nx.gnm_random_graph(nodes, edges, directed=True)

            graphs.append((G, resilience))

        except Exception:
            continue

    return graphs


def spectral_features(G):

    UG = G.to_undirected()

    A = nx.to_numpy_array(UG)
    eigvals_A = np.linalg.eigvals(A)

    spectral_radius = max(abs(eigvals_A))

    L = nx.laplacian_matrix(UG).toarray()
    eigvals_L = np.linalg.eigvals(L)
    eigvals_L = np.sort(eigvals_L)

    algebraic_connectivity = eigvals_L[1] if len(eigvals_L) > 1 else 0
    largest_laplacian = eigvals_L[-1]

    spectral_gap = largest_laplacian - algebraic_connectivity

    return {
        "spectral_radius": float(spectral_radius),
        "algebraic_connectivity": float(algebraic_connectivity),
        "largest_laplacian": float(largest_laplacian),
        "spectral_gap": float(spectral_gap)
    }


def run():

    print("\nNEXAH Resilience Spectral Analyzer")
    print("----------------------------------")

    graphs = load_graphs()

    if len(graphs) < 3:
        print("Not enough graphs.")
        return

    high = []
    low = []

    for G, res in graphs:

        spec = spectral_features(G)

        if res > 0.8:
            high.append(spec)
        else:
            low.append(spec)

    def summarize(group):

        if not group:
            return None

        return {
            "spectral_radius": statistics.mean([g["spectral_radius"] for g in group]),
            "algebraic_connectivity": statistics.mean([g["algebraic_connectivity"] for g in group]),
            "largest_laplacian": statistics.mean([g["largest_laplacian"] for g in group]),
            "spectral_gap": statistics.mean([g["spectral_gap"] for g in group]),
        }

    high_stats = summarize(high)
    low_stats = summarize(low)

    print("\nHigh Resilience Spectral Signature")
    print("----------------------------------")

    if high_stats:
        for k, v in high_stats.items():
            print(f"{k:20s} ≈ {round(v,3)}")

    print("\nLow Resilience Spectral Signature")
    print("---------------------------------")

    if low_stats:
        for k, v in low_stats.items():
            print(f"{k:20s} ≈ {round(v,3)}")


if __name__ == "__main__":
    run()
