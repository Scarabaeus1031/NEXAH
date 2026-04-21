"""
NEXAH Micro Architecture Scanner

High-resolution scan of small architectures to detect
maximum resilience regions in micro-network space.

Search space:
nodes = 4–10
degree ≈ 2–5
"""

import networkx as nx
import statistics

from tools.resilience_analyzer_v2 import analyze_resilience


NODE_MIN = 4
NODE_MAX = 10

DEGREE_MIN = 2.0
DEGREE_MAX = 5.0
DEGREE_STEP = 0.25

SAMPLES_PER_POINT = 12


def generate_graph(nodes, degree):

    edges = int(nodes * degree)

    # directed graph edge safety
    edges = min(edges, nodes * nodes - 1)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def evaluate_point(nodes, degree):

    scores = []

    for _ in range(SAMPLES_PER_POINT):

        G = generate_graph(nodes, degree)

        report = analyze_resilience(G)

        scores.append(report["resilience_score"])

    return statistics.mean(scores)


def run_scan():

    print("\nNEXAH Micro Architecture Scanner")
    print("--------------------------------")

    best = None

    nodes_range = range(NODE_MIN, NODE_MAX + 1)

    degree_values = []

    d = DEGREE_MIN
    while d <= DEGREE_MAX:
        degree_values.append(round(d, 2))
        d += DEGREE_STEP

    for nodes in nodes_range:

        for degree in degree_values:

            avg_res = evaluate_point(nodes, degree)

            print(
                f"nodes={nodes} "
                f"| degree={degree} "
                f"| avg_resilience={round(avg_res,3)}"
            )

            if best is None or avg_res > best["resilience"]:

                best = {
                    "nodes": nodes,
                    "degree": degree,
                    "resilience": avg_res
                }

    print("\nBest micro architecture discovered")
    print("----------------------------------")
    print(
        f"nodes={best['nodes']} "
        f"| degree={round(best['degree'],2)} "
        f"| resilience={round(best['resilience'],3)}"
    )


if __name__ == "__main__":

    run_scan()
