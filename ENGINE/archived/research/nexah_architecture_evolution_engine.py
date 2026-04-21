"""
NEXAH Architecture Evolution Engine

Uses evolutionary search to discover resilient architectures.

Algorithm:

initialize population
→ evaluate resilience
→ select best
→ mutate architectures
→ repeat
"""

import random
import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


POPULATION_SIZE = 12
GENERATIONS = 8
SURVIVORS = 4


def random_graph():

    nodes = random.randint(3, 10)

    degree = random.uniform(2.0, 5.0)

    edges = int(nodes * degree)

    edges = min(edges, nodes * nodes - 1)

    return nx.gnm_random_graph(nodes, edges, directed=True)


def mutate_graph(G):

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    # small random variation
    nodes = max(3, nodes + random.choice([-1, 0, 1]))

    edges = max(1, edges + random.choice([-2, -1, 0, 1, 2]))

    edges = min(edges, nodes * nodes - 1)

    return nx.gnm_random_graph(nodes, edges, directed=True)


def evaluate_population(population):

    results = []

    for G in population:

        report = analyze_resilience(G)

        nodes = report["nodes"]
        edges = report["edges"]
        res = report["resilience_score"]

        degree = edges / nodes if nodes else 0

        results.append({
            "graph": G,
            "nodes": nodes,
            "edges": edges,
            "degree": degree,
            "resilience": res
        })

    return results


def evolve():

    print("\nNEXAH Architecture Evolution Engine")
    print("-----------------------------------")

    population = [random_graph() for _ in range(POPULATION_SIZE)]

    best_global = None

    for gen in range(GENERATIONS):

        print(f"\nGeneration {gen+1}")
        print("------------------")

        results = evaluate_population(population)

        results.sort(key=lambda r: r["resilience"], reverse=True)

        best = results[0]

        print(
            f"Best | nodes={best['nodes']} "
            f"edges={best['edges']} "
            f"degree={round(best['degree'],2)} "
            f"resilience={round(best['resilience'],3)}"
        )

        if best_global is None or best["resilience"] > best_global["resilience"]:
            best_global = best

        # select survivors
        survivors = results[:SURVIVORS]

        # build next generation
        new_population = []

        for s in survivors:

            new_population.append(s["graph"])

            for _ in range(2):

                new_population.append(mutate_graph(s["graph"]))

        population = new_population[:POPULATION_SIZE]

    print("\nBest Architecture Discovered")
    print("-----------------------------")

    print(
        f"nodes={best_global['nodes']} "
        f"edges={best_global['edges']} "
        f"degree={round(best_global['degree'],2)} "
        f"resilience={round(best_global['resilience'],3)}"
    )


if __name__ == "__main__":

    evolve()
