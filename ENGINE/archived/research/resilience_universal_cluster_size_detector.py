"""
NEXAH Universal Cluster Size Detector

Searches for the optimal cluster size that maximizes
resilience in dense micro-networks.

Hypothesis:
small dense clusters maximize resilience.

Scan:
nodes = 3 – 30
degree ≈ nodes − 1
"""

import networkx as nx
import statistics

from tools.resilience_analyzer_v2 import analyze_resilience


NODE_MIN = 3
NODE_MAX = 30

SAMPLES_PER_NODE = 20


def generate_dense_cluster(nodes):

    # target degree ≈ nodes - 1
    degree = nodes - 1

    edges = int(nodes * degree)

    edges = min(edges, nodes * nodes - 1)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def evaluate_cluster(nodes):

    scores = []

    for _ in range(SAMPLES_PER_NODE):

        G = generate_dense_cluster(nodes)

        report = analyze_resilience(G)

        scores.append(report["resilience_score"])

    return statistics.mean(scores)


def run_scan():

    print("\nNEXAH Universal Cluster Size Detector")
    print("-------------------------------------")

    best = None

    results = []

    for nodes in range(NODE_MIN, NODE_MAX + 1):

        avg_res = evaluate_cluster(nodes)

        results.append((nodes, avg_res))

        print(
            f"nodes={nodes} | avg_resilience={round(avg_res,3)}"
        )

        if best is None or avg_res > best["resilience"]:

            best = {
                "nodes": nodes,
                "resilience": avg_res
            }

    print("\nBest cluster size discovered")
    print("----------------------------")

    print(
        f"nodes={best['nodes']} "
        f"| resilience={round(best['resilience'],3)}"
    )

    print("\nTop cluster sizes")

    results_sorted = sorted(
        results,
        key=lambda x: x[1],
        reverse=True
    )[:5]

    for r in results_sorted:

        print(
            f"nodes={r[0]} "
            f"| resilience={round(r[1],3)}"
        )


if __name__ == "__main__":

    run_scan()
