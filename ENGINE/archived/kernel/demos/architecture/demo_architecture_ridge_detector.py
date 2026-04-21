"""
NEXAH Architecture Ridge Detector
=================================

Detects important structures in the architecture stability landscape.

Detected structures:

• local stability peaks
• ridge points
• saddle candidates

Visualization:

3D landscape with detected features marked.

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_ridge_detector
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# compute stability field
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

                s = spectral_stability_score(G)
                scores.append(s)

            if scores:
                stability[i, j] = np.mean(scores)

    return node_values, prob_values, stability


# ---------------------------------------------------------
# ridge / peak detection
# ---------------------------------------------------------

def detect_features(stability):

    peaks = []
    ridges = []
    saddles = []

    rows, cols = stability.shape

    for i in range(1, rows-1):
        for j in range(1, cols-1):

            value = stability[i, j]

            neighbors = [
                stability[i-1, j],
                stability[i+1, j],
                stability[i, j-1],
                stability[i, j+1],
            ]

            if value > max(neighbors):
                peaks.append((i, j))

            elif value > np.mean(neighbors):
                ridges.append((i, j))

            elif abs(value - np.mean(neighbors)) < 0.01:
                saddles.append((i, j))

    return peaks, ridges, saddles


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_landscape(node_values, prob_values, stability, peaks, ridges, saddles):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "architecture_ridge_detector.png"
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
        antialiased=True,
        alpha=0.9
    )

    # plot peaks
    for i, j in peaks:
        ax.scatter(
            prob_values[j],
            node_values[i],
            stability[i, j],
            color="red",
            s=40
        )

    # plot ridge points
    for i, j in ridges:
        ax.scatter(
            prob_values[j],
            node_values[i],
            stability[i, j],
            color="orange",
            s=20
        )

    # plot saddles
    for i, j in saddles:
        ax.scatter(
            prob_values[j],
            node_values[i],
            stability[i, j],
            color="white",
            s=20
        )

    ax.set_xlabel("Edge Probability (Network Density)")
    ax.set_ylabel("Number of Nodes")
    ax.set_zlabel("Mean Stability (λ₂ / λmax)")

    ax.set_title("Architecture Stability Landscape with Ridge Detection")

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

    print("\nComputing architecture ridge detection...\n")

    node_values, prob_values, stability = compute_stability_field()

    peaks, ridges, saddles = detect_features(stability)

    plot_landscape(
        node_values,
        prob_values,
        stability,
        peaks,
        ridges,
        saddles
    )


if __name__ == "__main__":
    run_demo()
