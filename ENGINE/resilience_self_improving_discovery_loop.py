"""
NEXAH Self Improving Discovery Loop

Autonomous scientific discovery cycle:

generate architectures
→ analyze resilience
→ discover scaling laws
→ design improved architectures
→ repeat
"""

import random
import networkx as nx
import statistics

from tools.resilience_analyzer_v2 import analyze_resilience


GENERATIONS = 5
ARCHITECTURES_PER_GEN = 12

TARGET_DEGREE_MIN = 2.5
TARGET_DEGREE_MAX = 4.5


def generate_architecture():

    n = random.randint(5, 40)

    degree = random.uniform(TARGET_DEGREE_MIN, TARGET_DEGREE_MAX)

    edges = int(n * degree)

    G = nx.gnm_random_graph(n, edges, directed=True)

    return G


def evaluate_population(graphs):

    results = []

    for G in graphs:

        report = analyze_resilience(G)

        score = report["resilience_score"]

        nodes = G.number_of_nodes()
        edges = G.number_of_edges()

        degree = edges / nodes

        results.append({
            "graph": G,
            "nodes": nodes,
            "edges": edges,
            "degree": degree,
            "resilience": score
        })

    return results


def discover_degree_law(results):

    degrees = [r["degree"] for r in results]
    resilience = [r["resilience"] for r in results]

    best = sorted(results, key=lambda r: r["resilience"], reverse=True)[:3]

    best_degree = statistics.mean([r["degree"] for r in best])

    return best_degree


def update_search_window(best_degree):

    width = 1.0

    return best_degree - width/2, best_degree + width/2


def run_loop():

    global TARGET_DEGREE_MIN
    global TARGET_DEGREE_MAX

    print("\nNEXAH Self Improving Discovery Loop")
    print("-----------------------------------")

    for gen in range(GENERATIONS):

        print(f"\nGeneration {gen+1}")
        print("------------------")

        graphs = [generate_architecture() for _ in range(ARCHITECTURES_PER_GEN)]

        results = evaluate_population(graphs)

        best = max(results, key=lambda r: r["resilience"])

        avg_res = statistics.mean([r["resilience"] for r in results])

        print(
            f"Best resilience: {round(best['resilience'],3)} "
            f"| nodes={best['nodes']} "
            f"| edges={best['edges']} "
            f"| degree={round(best['degree'],2)}"
        )

        print("Average resilience:", round(avg_res,3))

        best_degree = discover_degree_law(results)

        TARGET_DEGREE_MIN, TARGET_DEGREE_MAX = update_search_window(best_degree)

        print(
            "Updated search window:",
            round(TARGET_DEGREE_MIN,2),
            "–",
            round(TARGET_DEGREE_MAX,2)
        )


if __name__ == "__main__":

    run_loop()
