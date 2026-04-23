"""
NEXAH Architecture Optimizer Demo
=================================

Demonstrates navigation in architecture space.

Starting from a random architecture, the system applies structural
mutations and accepts only those that improve the spectral stability
metric:

    λ₂ / λmax

This approximates a gradient navigation toward stable architectures.

Run:

python -m ENGINE.nexah_kernel.demos.demo_architecture_optimizer
"""

import os
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score


# ---------------------------------------------------------
# mutation operators
# ---------------------------------------------------------

def mutate_graph(G):

    G_new = G.copy()

    nodes = list(G_new.nodes)

    if random.random() < 0.5 and G_new.number_of_edges() > 0:
        # remove random edge
        edge = random.choice(list(G_new.edges))
        G_new.remove_edge(*edge)

    else:
        # add random edge
        u, v = random.sample(nodes, 2)
        if not G_new.has_edge(u, v):
            G_new.add_edge(u, v)

    return G_new


# ---------------------------------------------------------
# optimizer
# ---------------------------------------------------------

def optimize_architecture(G, steps=200):

    scores = []

    current_score = spectral_stability_score(G)

    for _ in range(steps):

        G_candidate = mutate_graph(G)

        score = spectral_stability_score(G_candidate)

        if score > current_score:
            G = G_candidate
            current_score = score

        scores.append(current_score)

    return G, scores


# ---------------------------------------------------------
# visualization
# ---------------------------------------------------------

def plot_progress(scores):

    output_dir = "ENGINE/nexah_kernel/demos/visuals"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(
        output_dir,
        "architecture_optimizer_progress.png"
    )

    plt.figure(figsize=(8,4))

    plt.plot(scores)

    plt.title("Architecture Stability Optimization")
    plt.xlabel("Mutation Step")
    plt.ylabel("λ₂ / λmax")

    plt.tight_layout()

    plt.savefig(path, dpi=160)

    print("\nSaved visualization to:")
    print(path)

    plt.show()


# ---------------------------------------------------------
# run demo
# ---------------------------------------------------------

def run_demo():

    print("\nStarting architecture optimization...\n")

    G = nx.erdos_renyi_graph(6, 0.3)

    start_score = spectral_stability_score(G)

    print("Initial stability:", start_score)

    G_opt, scores = optimize_architecture(G)

    final_score = spectral_stability_score(G_opt)

    print("Final stability:", final_score)

    plot_progress(scores)


if __name__ == "__main__":
    run_demo()
