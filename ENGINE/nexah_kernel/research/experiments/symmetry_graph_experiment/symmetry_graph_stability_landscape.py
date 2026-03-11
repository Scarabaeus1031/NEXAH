"""
NEXAH Symmetry Graph Stability Landscape
----------------------------------------

Compares collapse distributions for:

1. no hub
2. single hub
3. dual hub

Output:
- console summary
- histogram plot with 3 subplots
"""

import random
import statistics
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
# summary
# -----------------------------

def print_summary(name, data):

    print("\n", name)
    print("Runs:", len(data))
    print("Min collapse:", min(data))
    print("Max collapse:", max(data))
    print("Mean collapse:", statistics.mean(data))


# -----------------------------
# plot landscape
# -----------------------------

def plot_landscape(nohub, single, dual):

    fig, axs = plt.subplots(1,3, figsize=(15,5))

    axs[0].hist(nohub, bins=10)
    axs[0].set_title("No Hub")

    axs[1].hist(single, bins=10)
    axs[1].set_title("Single Hub")

    axs[2].hist(dual, bins=10)
    axs[2].set_title("Dual Hub")

    for ax in axs:
        ax.set_xlabel("Edges removed before collapse")
        ax.set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()


# -----------------------------
# run
# -----------------------------

if __name__ == "__main__":

    print("\nRunning Stability Landscape Experiment...\n")

    nohub_data = run_experiment(build_no_hub_graph)
    single_data = run_experiment(build_graph)
    dual_data = run_experiment(build_dual_hub_graph)

    print_summary("No Hub", nohub_data)
    print_summary("Single Hub", single_data)
    print_summary("Dual Hub", dual_data)

    plot_landscape(nohub_data, single_data, dual_data)
