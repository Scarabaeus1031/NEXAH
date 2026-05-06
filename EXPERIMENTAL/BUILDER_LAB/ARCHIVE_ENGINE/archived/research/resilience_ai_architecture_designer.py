"""
NEXAH AI Architecture Designer

Uses discovered scaling laws to design new
architectures likely to have high resilience.

Target principle discovered:

Resilience ≈ f(1 / degree)

Optimal degree range ≈ 3 – 4
"""

import random
import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


TARGET_DEGREE_MIN = 3.0
TARGET_DEGREE_MAX = 4.0

ARCHITECTURES_TO_TEST = 10


def generate_candidate():

    n = random.randint(5, 40)

    target_degree = random.uniform(TARGET_DEGREE_MIN, TARGET_DEGREE_MAX)

    edges_target = int(n * target_degree)

    G = nx.gnm_random_graph(n, edges_target, directed=True)

    return G


def design_architectures():

    print("\nNEXAH AI Architecture Designer")
    print("------------------------------")

    best = None

    for i in range(ARCHITECTURES_TO_TEST):

        G = generate_candidate()

        report = analyze_resilience(G)

        score = report["resilience_score"]

        nodes = G.number_of_nodes()
        edges = G.number_of_edges()

        degree = edges / nodes

        print(
            f"Test {i+1} | nodes={nodes} "
            f"| edges={edges} "
            f"| degree={round(degree,2)} "
            f"| resilience={round(score,3)}"
        )

        if best is None or score > best["score"]:

            best = {
                "graph": G,
                "score": score,
                "nodes": nodes,
                "edges": edges,
                "degree": degree
            }

    print("\nBest AI-designed architecture")
    print("-----------------------------")

    print(
        f"nodes={best['nodes']} "
        f"| edges={best['edges']} "
        f"| degree={round(best['degree'],2)} "
        f"| resilience={round(best['score'],3)}"
    )


def run():

    design_architectures()


if __name__ == "__main__":

    run()
