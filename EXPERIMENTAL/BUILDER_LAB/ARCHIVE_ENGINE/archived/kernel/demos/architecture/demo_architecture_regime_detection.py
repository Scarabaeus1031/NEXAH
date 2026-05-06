"""
NEXAH Architecture Regime Detection
===================================

Detects structural regimes in architecture space using the
spectral stability metric:

    λ₂ / λmax

Regimes:

UNSTABLE
METASTABLE
STABLE

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_regime_detection
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# regime classifier
# ---------------------------------------------------------

def classify_regime(score):

    if score < 0.15:
        return 0  # unstable

    elif score < 0.45:
        return 1  # metastable

    else:
        return 2  # stable


# ---------------------------------------------------------
# architecture sampling
# ---------------------------------------------------------

def sample_regimes():

    node_range = range(4, 15)
    prob_range = np.linspace(0.05, 0.9, 20)

    regimes = np.zeros((len(node_range), len(prob_range)))

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

                mean_score = np.mean(scores)
                regimes[i, j] = classify_regime(mean_score)

    return node_range, prob_range, regimes


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_regime_map(nodes, probs, regimes):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(
        output_dir,
        "architecture_regime_map.png"
    )

    plt.figure(figsize=(8,6))

    plt.imshow(
        regimes,
        origin="lower",
        aspect="auto",
        extent=[min(probs), max(probs), min(nodes), max(nodes)],
        cmap="plasma"
    )

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")

    plt.title("Architecture Regime Map")

    cbar = plt.colorbar()
    cbar.set_label("0 = unstable | 1 = metastable | 2 = stable")

    plt.tight_layout()

    plt.savefig(path, dpi=160)

    print("\nSaved visualization to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nDetecting architecture regimes...\n")

    nodes, probs, regimes = sample_regimes()

    plot_regime_map(nodes, probs, regimes)


if __name__ == "__main__":
    run_demo()
