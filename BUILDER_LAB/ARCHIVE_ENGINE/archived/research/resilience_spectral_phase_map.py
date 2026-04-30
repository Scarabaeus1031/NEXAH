"""
NEXAH Resilience Spectral Phase Map

Visualizes the relationship between spectral connectivity
and resilience.

Axes:
X = λ₂ / λ_max  (spectral connectivity ratio)
Y = resilience

This reveals whether resilience follows a continuous
spectral phase law.

The script reconstructs representative graphs from stored
compact experiment results.
"""

import os
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


RESULT_DIR = "results"


def load_graphs():

    graphs = []

    if not os.path.exists(RESULT_DIR):
        return graphs

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        try:

            path = os.path.join(RESULT_DIR, f)

            with open(path) as file:
                r = json.load(file)

            if "nodes" not in r:
                continue

            nodes = r["nodes"]
            edges = r["edges"]
            resilience = r["resilience_score"]

            if nodes < 2:
                continue

            G = nx.gnm_random_graph(nodes, edges)

            graphs.append((G, resilience))

        except Exception:
            continue

    return graphs


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


def run():

    print("\nNEXAH Resilience Spectral Phase Map")
    print("-----------------------------------")

    graphs = load_graphs()

    if len(graphs) < 5:
        print("Not enough data.")
        return

    xs = []
    ys = []

    for G, resilience in graphs:

        ratio = spectral_ratio(G)

        if ratio is None:
            continue

        xs.append(ratio)
        ys.append(resilience)

    xs = np.array(xs)
    ys = np.array(ys)

    plt.figure(figsize=(8,6))
    plt.scatter(xs, ys, alpha=0.8)

    if len(xs) > 2:
        coeff = np.polyfit(xs, ys, 1)
        line = np.poly1d(coeff)

        xline = np.linspace(xs.min(), xs.max(), 100)
        yline = line(xline)

        plt.plot(xline, yline)

    plt.xlabel("λ₂ / λ_max  (spectral connectivity ratio)")
    plt.ylabel("Resilience")

    plt.title("NEXAH Spectral Phase Map")

    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    run()
