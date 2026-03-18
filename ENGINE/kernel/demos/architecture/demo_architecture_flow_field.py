"""
NEXAH Architecture Flow Field
=============================

Visualizes the architecture stability landscape together with
a flow field indicating the direction of increasing stability.

Layers:

1) Stability heatmap (λ₂ / λmax)
2) Regime boundaries
3) Flow vectors (gradient of stability)

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_flow_field
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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

                s = spectral_stability_score(G)
                scores.append(s)

            if scores:
                stability[i, j] = np.mean(scores)

    return node_values, prob_values, stability


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
# compute gradient flow
# ---------------------------------------------------------

def compute_flow(stability, node_values, prob_values):

    d_nodes = node_values[1] - node_values[0]
    d_probs = prob_values[1] - prob_values[0]

    grad_nodes, grad_probs = np.gradient(stability, d_nodes, d_probs)

    U = grad_probs
    V = grad_nodes

    magnitude = np.sqrt(U**2 + V**2)

    U_norm = np.zeros_like(U)
    V_norm = np.zeros_like(V)

    mask = magnitude > 1e-10

    U_norm[mask] = U[mask] / magnitude[mask]
    V_norm[mask] = V[mask] / magnitude[mask]

    return U_norm, V_norm


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_flow(node_values, prob_values, stability, regimes, U, V):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "architecture_flow_field.png"
    )

    plt.figure(figsize=(10,7))

    extent = [
        prob_values.min(),
        prob_values.max(),
        node_values.min(),
        node_values.max()
    ]

    plt.imshow(
        stability,
        origin="lower",
        aspect="auto",
        extent=extent
    )

    plt.contour(
        prob_values,
        node_values,
        regimes,
        levels=[0.5,1.5],
        colors="black",
        linewidths=2
    )

    P, N = np.meshgrid(prob_values, node_values)

    plt.quiver(
        P,
        N,
        U,
        V,
        color="cyan",
        scale=15
    )

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")
    plt.title("Architecture Flow Field")

    cbar = plt.colorbar()
    cbar.set_label("Mean Stability (λ₂ / λmax)")

    plt.tight_layout()

    plt.savefig(output_file, dpi=170)

    print("\nSaved visualization to:")
    print(output_file)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nComputing architecture flow field...\n")

    node_values, prob_values, stability = compute_stability_field()

    regimes = classify_regimes(stability)

    U, V = compute_flow(stability, node_values, prob_values)

    plot_flow(node_values, prob_values, stability, regimes, U, V)


if __name__ == "__main__":
    run_demo()
