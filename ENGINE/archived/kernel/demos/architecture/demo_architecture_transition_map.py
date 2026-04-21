"""
NEXAH Architecture Transition Map
=================================

Visualizes transition zones in architecture space.

Color shows the magnitude of stability change:

    Δ stability = | stability(p+Δp) − stability(p) |

High values indicate regime boundaries and structural transitions.

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_transition_map
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

            if len(scores) > 0:
                stability[i, j] = np.mean(scores)

    return node_range, prob_range, stability


# ---------------------------------------------------------
# compute transition map
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

def plot_transition_map(nodes, probs, transition):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(
        output_dir,
        "architecture_transition_map.png"
    )

    plt.figure(figsize=(8,6))

    plt.imshow(
        transition,
        origin="lower",
        aspect="auto",
        extent=[min(probs), max(probs), min(nodes), max(nodes)]
    )

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")

    plt.title("Architecture Transition Map")

    cbar = plt.colorbar()
    cbar.set_label("| Δ stability |")

    plt.tight_layout()

    plt.savefig(path, dpi=160)

    print("\nSaved visualization to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nComputing architecture transition map...\n")

    nodes, probs, stability = compute_stability_field()

    transition = compute_transition_map(stability)

    plot_transition_map(nodes, probs, transition)


if __name__ == "__main__":
    run_demo()
