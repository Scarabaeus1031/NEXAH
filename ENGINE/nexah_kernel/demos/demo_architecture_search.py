"""
NEXAH Architecture Stability Search
===================================

Explores the architecture space of random graphs and evaluates their
spectral stability using the metric

    λ₂ / λmax

where

λ₂     = algebraic connectivity
λmax   = largest Laplacian eigenvalue

The demo generates many random architectures and visualizes the
distribution of stability scores.

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_search
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# architecture generator
# ---------------------------------------------------------

def generate_random_architecture(n_nodes=5, edge_prob=0.5):
    """
    Generate a random architecture graph.
    """
    return nx.erdos_renyi_graph(n_nodes, edge_prob)


# ---------------------------------------------------------
# architecture search
# ---------------------------------------------------------

def architecture_search(samples=2000):

    scores = []
    degrees = []
    clusterings = []

    for _ in range(samples):

        G = generate_random_architecture()

        if len(G.edges) == 0:
            continue

        score = spectral_stability_score(G)

        scores.append(score)

        degrees.append(np.mean([d for _, d in G.degree()]))
        clusterings.append(nx.average_clustering(G))

    return scores, degrees, clusterings


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_results(scores):

    plt.figure(figsize=(8,5))

    plt.hist(scores, bins=40)

    plt.title("Architecture Stability Distribution (λ₂ / λmax)")
    plt.xlabel("Spectral Stability Score")
    plt.ylabel("Architecture Count")

    plt.tight_layout()

    plt.savefig(
        "ENGINE/nexah_kernel/demos/visuals/architecture_stability_distribution.png",
        dpi=150
    )

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nRunning architecture stability search...\n")

    scores, degrees, clusterings = architecture_search(samples=5000)

    print("Samples analyzed:", len(scores))
    print("Mean stability score:", np.mean(scores))
    print("Max stability score:", np.max(scores))

    plot_results(scores)


if __name__ == "__main__":
    run_demo()
