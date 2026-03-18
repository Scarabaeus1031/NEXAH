"""
NEXAH Symmetry Graph Entropy Scan
---------------------------------

Compares collapse distributions for:

1. no hub
2. single hub
3. dual hub

and computes:
- mean collapse
- collapse histogram
- Shannon entropy of collapse distribution
"""

import random
import statistics
import math
import matplotlib.pyplot as plt
import networkx as nx

from .symmetry_graph_3cycle import build_graph
from .symmetry_graph_dual_hub_experiment import build_dual_hub_graph


# -----------------------------
# build no-hub graph
# -----------------------------

def build_no_hub_graph():

    G = build_graph()

    if "center" in G:
        G.remove_node("center")

    return G


# -----------------------------
# collapse simulation
# -----------------------------

def collapse_simulation(G):

    G = G.copy()

    edges = list(G.edges())
    random.shuffle(edges)

    for step, edge in enumerate(edges):

        G.remove_edge(*edge)

        if nx.number_connected_components(G) > 1:
            return step + 1

    return len(edges)


# -----------------------------
# run experiment
# -----------------------------

def run_experiment(builder, runs=300):

    results = []

    for _ in range(runs):

        G = builder()
        collapse = collapse_simulation(G)

        results.append(collapse)

    return results


# -----------------------------
# Shannon entropy
# -----------------------------

def shannon_entropy(data):

    counts = {}

    for value in data:
        counts[value] = counts.get(value, 0) + 1

    total = len(data)

    entropy = 0

    for count in counts.values():

        p = count / total
        entropy -= p * math.log2(p)

    return entropy


# -----------------------------
# summary
# -----------------------------

def print_summary(name, data):

    entropy = shannon_entropy(data)

    print("\n", name)
    print("Runs:", len(data))
    print("Min collapse:", min(data))
    print("Max collapse:", max(data))
    print("Mean collapse:", statistics.mean(data))
    print("Shannon entropy:", entropy)


# -----------------------------
# plotting
# -----------------------------

def plot_entropy_landscape(nohub, single, dual):

    fig, axs = plt.subplots(1,3, figsize=(15,5))

    datasets = [
        ("No Hub", nohub),
        ("Single Hub", single),
        ("Dual Hub", dual)
    ]

    for ax, (title, data) in zip(axs, datasets):

        ax.hist(data, bins=12)

        entropy = shannon_entropy(data)

        ax.set_title(f"{title}\nEntropy = {entropy:.2f}")

        ax.set_xlabel("Edges removed before collapse")
        ax.set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()


# -----------------------------
# run
# -----------------------------

if __name__ == "__main__":

    print("\nRunning Entropy Scan...\n")

    nohub_data = run_experiment(build_no_hub_graph)
    single_data = run_experiment(build_graph)
    dual_data = run_experiment(build_dual_hub_graph)

    print_summary("No Hub", nohub_data)
    print_summary("Single Hub", single_data)
    print_summary("Dual Hub", dual_data)

    plot_entropy_landscape(nohub_data, single_data, dual_data)
