"""
NEXAH Architecture Stability Landscape
======================================

Explores architecture space and visualizes the stability landscape.

x-axis  : average degree
y-axis  : clustering coefficient
color   : spectral stability (λ₂ / λmax)

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_stability_landscape
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# architecture generator
# ---------------------------------------------------------

def generate_random_architecture(n_nodes=6, edge_prob=0.4):

    G = nx.erdos_renyi_graph(n_nodes, edge_prob)

    if G.number_of_edges() == 0:
        return None

    return G


# ---------------------------------------------------------
# architecture sampling
# ---------------------------------------------------------

def sample_architecture_space(samples=4000):

    degrees = []
    clusterings = []
    stability = []

    for _ in range(samples):

        G = generate_random_architecture()

        if G is None:
            continue

        score = spectral_stability_score(G)

        deg = np.mean([d for _, d in G.degree()])
        clust = nx.average_clustering(G)

        degrees.append(deg)
        clusterings.append(clust)
        stability.append(score)

    return degrees, clusterings, stability


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_landscape(degrees, clusterings, stability):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        "architecture_stability_landscape.png"
    )

    plt.figure(figsize=(8,6))

    scatter = plt.scatter(
        degrees,
        clusterings,
        c=stability,
        s=10
    )

    plt.xlabel("Average Degree")
    plt.ylabel("Clustering Coefficient")

    plt.title("Architecture Stability Landscape (λ₂ / λmax)")

    cbar = plt.colorbar(scatter)
    cbar.set_label("Spectral Stability Score")

    plt.tight_layout()

    plt.savefig(output_path, dpi=160)

    print("\nSaved visualization to:")
    print(output_path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nSampling architecture space...\n")

    degrees, clusterings, stability = sample_architecture_space()

    print("Samples analyzed:", len(stability))
    print("Mean stability:", np.mean(stability))
    print("Max stability:", np.max(stability))

    plot_landscape(degrees, clusterings, stability)


if __name__ == "__main__":
    run_demo()
