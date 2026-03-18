"""
NEXAH Symmetry Graph Resilience Test
------------------------------------

Compares structural resilience of symmetry graphs under random edge failures.

Measures:
how many edge removals until the graph fragments.
"""

import random
import statistics
import networkx as nx

from .symmetry_graph_3cycle import build_graph


# -------------------------
# Optional: Cross-linked graph
# -------------------------

def build_crosslinked_graph():

    G = build_graph()

    # extra cross links between rings
    extra_edges = [
        ("s0", "s6"),
        ("s3", "s9"),
        ("s8", "s14"),
        ("s2", "s11")
    ]

    for e in extra_edges:
        if not G.has_edge(*e):
            G.add_edge(*e)

    return G


# -------------------------
# Single drift run
# -------------------------

def run_single_drift(G):

    G = G.copy()

    steps = 0

    while nx.is_connected(G):

        edges = list(G.edges())

        if not edges:
            break

        edge = random.choice(edges)

        G.remove_edge(*edge)

        steps += 1

    return steps


# -------------------------
# Experiment
# -------------------------

def run_experiment(graph_builder, trials=100):

    results = []

    for _ in range(trials):

        G = graph_builder()

        steps = run_single_drift(G)

        results.append(steps)

    return results


# -------------------------
# Report
# -------------------------

def report(name, data):

    print("\n---", name, "---")

    print("runs:", len(data))
    print("min:", min(data))
    print("max:", max(data))
    print("mean:", statistics.mean(data))
    print("median:", statistics.median(data))


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    print("\nRunning symmetry graph resilience experiment...")

    base_results = run_experiment(build_graph)

    cross_results = run_experiment(build_crosslinked_graph)

    report("Original Graph", base_results)

    report("Crosslinked Graph", cross_results)
