"""
NEXAH Resilience Spectral Landscape

Builds a 3D stability landscape using spectral connectivity
and graph structure.

Axes:
X = nodes
Y = spectral connectivity ratio (λ2 / λmax)
Z = resilience

Color = clustering coefficient

This reveals where resilient architectures live in
spectral–structural space.
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

    print("\nNEXAH Resilience Spectral Landscape")
    print("-----------------------------------")

    graphs = load_graphs()

    if len(graphs) < 5:
        print("Not enough data.")
        return

    xs = []
    ys = []
    zs = []
    cs = []

    for G, resilience in graphs:

        ratio = spectral_ratio(G)

        if ratio is None:
            continue

        clustering = nx.average_clustering(G)

        xs.append(G.number_of_nodes())
        ys.append(ratio)
        zs.append(resilience)
        cs.append(clustering)

    xs = np.array(xs)
    ys = np.array(ys)
    zs = np.array(zs)
    cs = np.array(cs)

    fig = plt.figure(figsize=(9,7))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(
        xs,
        ys,
        zs,
        c=cs,
        cmap="plasma",
        s=80,
        alpha=0.9
    )

    ax.set_xlabel("Nodes")
    ax.set_ylabel("λ₂ / λ_max")
    ax.set_zlabel("Resilience")

    ax.set_title("NEXAH Spectral Stability Landscape")

    cbar = fig.colorbar(scatter)
    cbar.set_label("Clustering")

    plt.show()


if __name__ == "__main__":
    run()
