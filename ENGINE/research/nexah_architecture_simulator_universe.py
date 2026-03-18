"""
NEXAH Architecture Simulator Universe

Simulates thousands of architectures across the architecture space
to map the global resilience landscape.

Axes explored:

nodes
degree
edges
"""

import random
import statistics
import math

import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


SIMULATIONS = 600


def random_architecture():

    nodes = random.randint(3, 15)

    degree = random.uniform(1.5, 5.0)

    edges = int(nodes * degree)

    max_edges = nodes * nodes - 1

    edges = min(edges, max_edges)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def run_simulation():

    results = []

    print("\nNEXAH Architecture Universe Simulator")
    print("-------------------------------------")

    for i in range(SIMULATIONS):

        G = random_architecture()

        report = analyze_resilience(G)

        nodes = report["nodes"]
        edges = report["edges"]
        res = report["resilience_score"]

        degree = edges / nodes if nodes else 0

        results.append({
            "nodes": nodes,
            "edges": edges,
            "degree": degree,
            "resilience": res
        })

        if i % 50 == 0:

            print(
                f"Sim {i} | "
                f"nodes={nodes} "
                f"degree={round(degree,2)} "
                f"resilience={round(res,3)}"
            )

    return results


def analyze_universe(results):

    ranked = sorted(results, key=lambda x: x["resilience"], reverse=True)

    top = ranked[:50]

    nodes = [r["nodes"] for r in top]
    degree = [r["degree"] for r in top]
    edges = [r["edges"] for r in top]
    res = [r["resilience"] for r in top]

    print("\nUniverse Statistics")
    print("-------------------")

    print("best resilience:", round(max(res),3))
    print("mean resilience:", round(statistics.mean(res),3))

    print("\nStability Region")

    print("nodes ≈", round(statistics.mean(nodes),2))
    print("degree ≈", round(statistics.mean(degree),2))
    print("edges ≈", round(statistics.mean(edges),2))

    print("\nTop Architectures")

    for r in ranked[:10]:

        print(
            f"nodes={r['nodes']} "
            f"edges={r['edges']} "
            f"degree={round(r['degree'],2)} "
            f"resilience={round(r['resilience'],3)}"
        )


def run():

    results = run_simulation()

    analyze_universe(results)


if __name__ == "__main__":

    run()
