"""
NEXAH Architecture Morse Complex
================================

Approximates a Morse-style topological analysis of the architecture
stability landscape.

Detected structures:

• local maxima      → attractor nodes
• local minima      → low-stability basins
• saddle candidates → transition gates

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_morse_complex
"""

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# stability field
# ---------------------------------------------------------

def compute_stability_field():

    node_values = np.arange(4, 15)
    prob_values = np.linspace(0.05, 0.9, 18)

    stability = np.zeros((len(node_values), len(prob_values)))

    for i, n in enumerate(node_values):
        for j, p in enumerate(prob_values):

            scores = []

            for _ in range(15):

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

    nbs = []

    for di in [-1,0,1]:
        for dj in [-1,0,1]:

            if di == 0 and dj == 0:
                continue

            ni = i + di
            nj = j + dj

            if 0 <= ni < rows and 0 <= nj < cols:
                nbs.append((ni,nj))

    return nbs


# ---------------------------------------------------------
# Morse classification
# ---------------------------------------------------------

def classify_points(field):

    rows, cols = field.shape

    maxima = []
    minima = []
    saddles = []

    for i in range(rows):
        for j in range(cols):

            value = field[i,j]

            nb_vals = []

            for ni,nj in neighbors(i,j,rows,cols):
                nb_vals.append(field[ni,nj])

            if all(value >= v for v in nb_vals):
                maxima.append((i,j))

            elif all(value <= v for v in nb_vals):
                minima.append((i,j))

            else:

                higher = sum(value < v for v in nb_vals)
                lower = sum(value > v for v in nb_vals)

                if higher > 0 and lower > 0:
                    saddles.append((i,j))

    return maxima, minima, saddles


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_morse(node_vals, prob_vals, field, maxima, minima, saddles):

    P, N = np.meshgrid(prob_vals, node_vals)

    plt.figure(figsize=(10,6))

    plt.imshow(
        field,
        origin="lower",
        aspect="auto",
        extent=[prob_vals.min(), prob_vals.max(), node_vals.min(), node_vals.max()],
        cmap="viridis"
    )

    for i,j in maxima:
        plt.scatter(prob_vals[j], node_vals[i], color="red", s=80)

    for i,j in minima:
        plt.scatter(prob_vals[j], node_vals[i], color="blue", s=40)

    for i,j in saddles:
        plt.scatter(prob_vals[j], node_vals[i], color="orange", s=40)

    plt.colorbar(label="Mean Spectral Stability (λ₂ / λmax)")

    plt.xlabel("Edge Probability (Network Density)")
    plt.ylabel("Number of Nodes")

    plt.title("Architecture Morse Complex")

    os.makedirs(
        "ENGINE/nexah_kernel/demos/visuals",
        exist_ok=True
    )

    path = "ENGINE/nexah_kernel/demos/visuals/architecture_morse_complex.png"

    plt.savefig(path, dpi=200)

    print("\nSaved visualization to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# main
# ---------------------------------------------------------

def main():

    print("\nComputing stability field...\n")

    node_vals, prob_vals, field = compute_stability_field()

    print("Detecting Morse structures...\n")

    maxima, minima, saddles = classify_points(field)

    print("Maxima:", len(maxima))
    print("Minima:", len(minima))
    print("Saddles:", len(saddles))

    plot_morse(node_vals, prob_vals, field, maxima, minima, saddles)


if __name__ == "__main__":
    main()
