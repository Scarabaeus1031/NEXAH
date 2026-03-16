"""
NEXAH Architecture Stability Phase Diagram
==========================================

Computes a phase diagram of architecture stability.

x-axis  : edge probability (network density)
y-axis  : number of nodes
color   : mean spectral stability (λ₂ / λmax)

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_phase_diagram
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# phase sampling
# ---------------------------------------------------------

def compute_phase_diagram():

    node_range = range(4, 15)
    prob_range = np.linspace(0.05, 0.9, 20)

    phase = np.zeros((len(node_range), len(prob_range)))

    for i, n in enumerate(node_range):

        for j, p in enumerate(prob_range):

            scores = []

            for _ in range(40):

                G = nx.erdos_renyi_graph(n, p)

                if G.number_of_edges() == 0:
                    continue

                score = spectral_stability_score(G)
                scores.append(score)

            if len(scores) > 0:
                phase[i, j] = np.mean(scores)

    return node_range, prob_range, phase


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_phase_diagram(nodes, probs, phase):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(
        output_dir,
        "architecture_stability_phase_diagram.png"
    )

    plt.figure(figsize=(8,6))

    plt.imshow(
        phase,
        origin="lower",
        aspect="auto",
        extent=[min(probs), max(probs), min(nodes), max(nodes)]
    )

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")

    plt.title("Architecture Stability Phase Diagram (λ₂ / λmax)")

    cbar = plt.colorbar()
    cbar.set_label("Mean Spectral Stability")

    plt.tight_layout()

    plt.savefig(path, dpi=160)

    print("\nSaved visualization to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nComputing architecture stability phase diagram...\n")

    nodes, probs, phase = compute_phase_diagram()

    plot_phase_diagram(nodes, probs, phase)


if __name__ == "__main__":
    run_demo()
