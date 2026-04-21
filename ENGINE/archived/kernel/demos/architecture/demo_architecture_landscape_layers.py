"""
NEXAH Architecture Landscape Layers
===================================

Combines multiple landscape layers into one visualization.

Layers:

1) Stability field (λ₂ / λmax)         → heatmap
2) Regime classification                → contour lines
3) Transition ridges |Δ stability|     → white overlays

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_landscape_layers
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# compute stability field
# ---------------------------------------------------------

def compute_stability_field():

    node_range = range(4, 15)
    prob_range = np.linspace(0.05, 0.9, 20)

    stability = np.zeros((len(node_range), len(prob_range)))

    for i, n in enumerate(node_range):

        for j, p in enumerate(prob_range):

            scores = []

            for _ in range(30):

                G = nx.erdos_renyi_graph(n, p)

                if G.number_of_edges() == 0:
                    continue

                score = spectral_stability_score(G)
                scores.append(score)

            if scores:
                stability[i, j] = np.mean(scores)

    return node_range, prob_range, stability


# ---------------------------------------------------------
# regime classification
# ---------------------------------------------------------

def classify_regimes(stability):

    regimes = np.zeros_like(stability)

    regimes[stability < 0.15] = 0
    regimes[(stability >= 0.15) & (stability < 0.45)] = 1
    regimes[stability >= 0.45] = 2

    return regimes


# ---------------------------------------------------------
# transition ridges
# ---------------------------------------------------------

def compute_transition_map(stability):

    transition = np.zeros_like(stability)

    for i in range(stability.shape[0]):

        for j in range(stability.shape[1] - 1):

            transition[i, j] = abs(
                stability[i, j+1] - stability[i, j]
            )

    return transition


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_layers(nodes, probs, stability, regimes, transition):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(
        output_dir,
        "architecture_landscape_layers.png"
    )

    plt.figure(figsize=(9,7))

    extent = [min(probs), max(probs), min(nodes), max(nodes)]

    # base layer: stability heatmap
    plt.imshow(
        stability,
        origin="lower",
        aspect="auto",
        extent=extent
    )

    # regime boundaries
    plt.contour(
        probs,
        nodes,
        regimes,
        levels=[0.5, 1.5],
        colors="black",
        linewidths=2
    )

    # transition ridges
    plt.contour(
        probs,
        nodes,
        transition,
        levels=5,
        colors="white",
        linewidths=1
    )

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")

    plt.title("Architecture Landscape Layers")

    cbar = plt.colorbar()
    cbar.set_label("Mean Stability (λ₂ / λmax)")

    plt.tight_layout()

    plt.savefig(path, dpi=170)

    print("\nSaved visualization to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nComputing architecture landscape layers...\n")

    nodes, probs, stability = compute_stability_field()

    regimes = classify_regimes(stability)

    transition = compute_transition_map(stability)

    plot_layers(nodes, probs, stability, regimes, transition)


if __name__ == "__main__":
    run_demo()
