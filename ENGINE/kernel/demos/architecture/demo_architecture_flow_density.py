"""
NEXAH Architecture Flow Density
===============================

Visualizes how many gradient-flow paths pass through each cell
of the architecture stability landscape.

Interpretation:

    bright regions = many architectures flow through this zone
    dark regions   = little structural traffic

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_flow_density
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
    prob_values = np.linspace(0.05, 0.9, 17)

    stability = np.zeros((len(node_values), len(prob_values)))

    for i, n in enumerate(node_values):
        for j, p in enumerate(prob_values):

            scores = []

            for _ in range(25):

                G = nx.erdos_renyi_graph(int(n), float(p))

                if G.number_of_edges() == 0:
                    continue

                s = spectral_stability_score(G)
                scores.append(s)

            if scores:
                stability[i, j] = np.mean(scores)

    return node_values, prob_values, stability


# ---------------------------------------------------------
# neighbor helper
# ---------------------------------------------------------

def neighbors(i, j, rows, cols):

    neigh = []

    for di, dj in [
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(-1,1),(1,-1),(1,1)
    ]:

        ni = i + di
        nj = j + dj

        if 0 <= ni < rows and 0 <= nj < cols:
            neigh.append((ni,nj))

    return neigh


# ---------------------------------------------------------
# gradient descent / ascent path
# ---------------------------------------------------------

def gradient_destination(stability, start):

    rows, cols = stability.shape
    current = start

    while True:

        neigh = neighbors(current[0], current[1], rows, cols)

        best = current
        best_val = stability[current]

        for n in neigh:

            if stability[n] > best_val:
                best = n
                best_val = stability[n]

        if best == current:
            return current

        current = best


# ---------------------------------------------------------
# compute flow density
# ---------------------------------------------------------

def compute_flow_density(stability):

    rows, cols = stability.shape

    flow = np.zeros_like(stability)

    for i in range(rows):
        for j in range(cols):

            current = (i,j)

            visited = []

            while True:

                visited.append(current)

                neigh = neighbors(current[0],current[1],rows,cols)

                best = current
                best_val = stability[current]

                for n in neigh:

                    if stability[n] > best_val:
                        best = n
                        best_val = stability[n]

                if best == current:
                    break

                current = best

            for v in visited:
                flow[v] += 1

    return flow


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_flow_density(node_values, prob_values, stability, flow):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    outfile = os.path.join(
        output_dir,
        "architecture_flow_density.png"
    )

    plt.figure(figsize=(10,7))

    extent = [
        prob_values.min(),
        prob_values.max(),
        node_values.min(),
        node_values.max()
    ]

    plt.imshow(
        flow,
        origin="lower",
        extent=extent,
        aspect="auto",
        cmap="inferno"
    )

    plt.title("Architecture Flow Density")

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")

    cbar = plt.colorbar()
    cbar.set_label("Number of gradient flows passing")

    plt.tight_layout()

    plt.savefig(outfile, dpi=180)

    print("\nSaved flow density map:")
    print(outfile)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run():

    print("\nComputing stability landscape...\n")

    node_values, prob_values, stability = compute_stability_field()

    print("Computing flow density...\n")

    flow = compute_flow_density(stability)

    plot_flow_density(
        node_values,
        prob_values,
        stability,
        flow
    )


if __name__ == "__main__":
    run()
