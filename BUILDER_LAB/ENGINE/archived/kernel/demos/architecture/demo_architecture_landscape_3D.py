"""
NEXAH Architecture Landscape 3D
===============================

Visualizes the architecture stability field as a 3D landscape.

Axes:
    x = edge probability (network density)
    y = number of nodes
    z = mean spectral stability (λ₂ / λmax)

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_landscape_3D
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# compute stability landscape
# ---------------------------------------------------------

def compute_stability_field():

    node_values = np.arange(4, 15)
    prob_values = np.linspace(0.05, 0.9, 20)

    stability = np.zeros((len(node_values), len(prob_values)))

    for i, n in enumerate(node_values):
        for j, p in enumerate(prob_values):

            scores = []

            for _ in range(30):

                G = nx.erdos_renyi_graph(int(n), float(p))

                if G.number_of_edges() == 0:
                    continue

                score = spectral_stability_score(G)
                scores.append(score)

            if scores:
                stability[i, j] = np.mean(scores)

    return node_values, prob_values, stability


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_3D_landscape(node_values, prob_values, stability):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "architecture_landscape_3D.png"
    )

    P, N = np.meshgrid(prob_values, node_values)

    fig = plt.figure(figsize=(11,8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(
        P,
        N,
        stability,
        cmap="viridis",
        linewidth=0,
        antialiased=True
    )

    ax.set_xlabel("Edge Probability (Network Density)")
    ax.set_ylabel("Number of Nodes")
    ax.set_zlabel("Mean Stability (λ₂ / λmax)")

    ax.set_title("Architecture Stability Landscape (3D)")

    fig.colorbar(surf, shrink=0.5, aspect=10)

    plt.tight_layout()

    plt.savefig(output_file, dpi=170)

    print("\nSaved visualization to:")
    print(output_file)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nComputing 3D architecture landscape...\n")

    node_values, prob_values, stability = compute_stability_field()

    plot_3D_landscape(node_values, prob_values, stability)


if __name__ == "__main__":
    run_demo()
