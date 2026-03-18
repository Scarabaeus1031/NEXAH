"""
NEXAH Architecture Attractor Map
================================

Simulates architecture evolution in the stability landscape.

Each starting point follows the stability gradient until it
reaches a stable basin (local attractor).

Output:

• stability landscape
• regime boundaries
• attractor basins
• architecture trajectories

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_attractor_map
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
# compute gradient field
# ---------------------------------------------------------

def compute_gradient(stability):

    gy, gx = np.gradient(stability)

    return gx, gy


# ---------------------------------------------------------
# gradient ascent trajectory
# ---------------------------------------------------------

def simulate_trajectory(start_i, start_j, gx, gy, steps=30):

    path = []

    i = start_i
    j = start_j

    for _ in range(steps):

        path.append((i, j))

        di = gy[i, j]
        dj = gx[i, j]

        i_new = int(np.clip(i + np.sign(di), 0, gx.shape[0]-1))
        j_new = int(np.clip(j + np.sign(dj), 0, gx.shape[1]-1))

        if i_new == i and j_new == j:
            break

        i, j = i_new, j_new

    path.append((i, j))

    return path


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_attractors(nodes, probs, stability, gx, gy):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "architecture_attractor_map.png"
    )

    plt.figure(figsize=(10,7))

    extent = [
        probs.min(),
        probs.max(),
        nodes.min(),
        nodes.max()
    ]

    plt.imshow(
        stability,
        origin="lower",
        aspect="auto",
        extent=extent
    )

    # simulate trajectories
    for i in range(0, len(nodes), 2):
        for j in range(0, len(probs), 2):

            path = simulate_trajectory(i, j, gx, gy)

            xs = [probs[p[1]] for p in path]
            ys = [nodes[p[0]] for p in path]

            plt.plot(xs, ys, color="white", alpha=0.6)

    plt.xlabel("Edge Probability")
    plt.ylabel("Number of Nodes")

    plt.title("Architecture Attractor Map")

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

    print("\nComputing architecture attractor map...\n")

    nodes, probs, stability = compute_stability_field()

    gx, gy = compute_gradient(stability)

    plot_attractors(nodes, probs, stability, gx, gy)


if __name__ == "__main__":
    run_demo()
