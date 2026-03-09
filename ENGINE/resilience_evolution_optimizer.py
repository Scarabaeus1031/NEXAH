"""
NEXAH Resilience Evolution Optimizer

Uses evolutionary search to discover architectures
with increasing resilience.
"""

import random
import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


POPULATION_SIZE = 8
GENERATIONS = 6
MUTATION_RATE = 0.3


def random_graph():

    # smaller graphs -> avoids networkx slowdowns
    n = random.randint(5, 15)

    topology = random.choice([
        "erdos",
        "scale_free",
        "small_world"
    ])

    if topology == "erdos":

        p = random.uniform(0.1, 0.4)
        G = nx.erdos_renyi_graph(n, p, directed=True)

    elif topology == "scale_free":

        m = random.randint(1, 4)
        G = nx.barabasi_albert_graph(n, m).to_directed()

    else:

        k = random.randint(2, 6)
        p = random.uniform(0.1, 0.3)
        G = nx.watts_strogatz_graph(n, k, p).to_directed()

    return G


def mutate_graph(G):

    G = G.copy()

    nodes = list(G.nodes())

    # add edge
    if random.random() < 0.5 and len(nodes) > 2:

        u = random.choice(nodes)
        v = random.choice(nodes)

        if u != v:
            G.add_edge(u, v)

    # remove edge
    if random.random() < 0.5 and G.number_of_edges() > 1:

        edge = random.choice(list(G.edges()))
        G.remove_edge(*edge)

    return G


def evaluate_population(population):

    scored = []

    for G in population:

        report = analyze_resilience(G)

        scored.append({
            "graph": G,
            "score": report["resilience_score"]
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored


def next_generation(scored_population):

    survivors = scored_population[: len(scored_population)//2]

    new_population = [s["graph"] for s in survivors]

    while len(new_population) < POPULATION_SIZE:

        parent = random.choice(survivors)["graph"]

        child = parent.copy()

        if random.random() < MUTATION_RATE:
            child = mutate_graph(child)

        new_population.append(child)

    return new_population


def run_evolution():

    print("\nNEXAH Evolution Optimizer")
    print("------------------------")

    population = [random_graph() for _ in range(POPULATION_SIZE)]

    best_overall = None

    for generation in range(GENERATIONS):

        scored = evaluate_population(population)

        best = scored[0]

        print(
            f"\nGeneration {generation+1}"
            f" | best resilience: {round(best['score'], 3)}"
            f" | nodes: {best['graph'].number_of_nodes()}"
            f" | edges: {best['graph'].number_of_edges()}"
        )

        if best_overall is None or best["score"] > best_overall["score"]:
            best_overall = best

        population = next_generation(scored)

    print("\nBest architecture discovered")
    print("Resilience:", round(best_overall["score"], 3))
    print("Nodes:", best_overall["graph"].number_of_nodes())
    print("Edges:", best_overall["graph"].number_of_edges())


if __name__ == "__main__":

    run_evolution()
