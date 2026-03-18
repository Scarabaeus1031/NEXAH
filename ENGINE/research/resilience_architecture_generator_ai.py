"""
NEXAH Resilience Architecture Generator AI

Uses ridge detection results to generate new architectures
near the most stable resilience region.
"""

import random
import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


TARGET_NODES = 6
TARGET_DEGREE = 3.6

SAMPLES = 12


def generate_ridge_architecture():

    # small variation around ridge
    nodes = max(3, int(random.gauss(TARGET_NODES, 1)))

    degree = max(1.5, random.gauss(TARGET_DEGREE, 0.6))

    edges = int(nodes * degree)

    # directed graph safety
    edges = min(edges, nodes * nodes - 1)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def run_generator():

    print("\nNEXAH Architecture Generator AI")
    print("--------------------------------")

    best = None

    for i in range(SAMPLES):

        G = generate_ridge_architecture()

        report = analyze_resilience(G)

        nodes = report["nodes"]
        edges = report["edges"]
        res = report["resilience_score"]

        degree = edges / nodes if nodes else 0

        print(
            f"Test {i+1} | "
            f"nodes={nodes} | "
            f"edges={edges} | "
            f"degree={round(degree,2)} | "
            f"resilience={round(res,3)}"
        )

        if best is None or res > best["resilience"]:
            best = {
                "nodes": nodes,
                "edges": edges,
                "degree": degree,
                "resilience": res
            }

    print("\nBest Generated Architecture")
    print("---------------------------")

    print(
        f"nodes={best['nodes']} | "
        f"edges={best['edges']} | "
        f"degree={round(best['degree'],2)} | "
        f"resilience={round(best['resilience'],3)}"
    )


if __name__ == "__main__":

    run_generator()
