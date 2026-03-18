"""
NEXAH Resilience Graph Evolution Engine

Evolves network architectures by mutating graph topology
and selecting architectures with higher resilience.

Pipeline:

generate graphs
→ mutate topology
→ evaluate resilience
→ keep best graphs
→ repeat

Goal:
discover resilient network structures automatically.
"""

import random
import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


POPULATION = 12
GENERATIONS = 8
MUTATIONS = 4


def generate_graph():

    nodes = random.randint(4, 10)
    degree = random.uniform(2.5, 4.5)

    edges = int(nodes * degree)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def mutate_graph(G):

    H = G.copy()

    mutation_type = random.choice(["add_edge", "remove_edge", "rewire"])

    nodes = list(H.nodes())

    if mutation_type == "add_edge":

        u = random.choice(nodes)
        v = random.choice(nodes)

        if u != v:
            H.add_edge(u, v)

    elif mutation_type == "remove_edge":

        edges = list(H.edges())

        if edges:
            H.remove_edge(*random.choice(edges))

    elif mutation_type == "rewire":

        edges = list(H.edges())

        if edges:
            H.remove_edge(*random.choice(edges))

            u = random.choice(nodes)
            v = random.choice(nodes)

            if u != v:
                H.add_edge(u, v)

    return H


def evaluate_graph(G):

    report = analyze_resilience(G)

    return report["resilience_score"]


def evolve_population():

    population = [generate_graph() for _ in range(POPULATION)]

    best_graph = None
    best_score = -1

    for gen in range(GENERATIONS):

        print(f"\nGeneration {gen+1}")
        print("------------------")

        scored = []

        for G in population:

            score = evaluate_graph(G)

            scored.append((score, G))

            nodes = G.number_of_nodes()
            edges = G.number_of_edges()
            degree = edges / nodes if nodes else 0

            print(
                f"nodes={nodes} edges={edges} "
                f"degree={round(degree,2)} "
                f"resilience={round(score,3)}"
            )

        scored.sort(reverse=True, key=lambda x: x[0])

        best_score_gen, best_graph_gen = scored[0]

        if best_score_gen > best_score:
            best_score = best_score_gen
            best_graph = best_graph_gen

        print("\nBest this generation")
        print("--------------------")

        nodes = best_graph_gen.number_of_nodes()
        edges = best_graph_gen.number_of_edges()
        degree = edges / nodes if nodes else 0

        print(
            f"nodes={nodes} edges={edges} "
            f"degree={round(degree,2)} "
            f"resilience={round(best_score_gen,3)}"
        )

        # selection
        survivors = [g for _, g in scored[: POPULATION // 3]]

        # reproduction + mutation
        new_population = survivors.copy()

        while len(new_population) < POPULATION:

            parent = random.choice(survivors)
            child = parent.copy()

            for _ in range(MUTATIONS):
                child = mutate_graph(child)

            new_population.append(child)

        population = new_population

    return best_graph, best_score


def run():

    print("\nNEXAH Graph Evolution Engine")
    print("----------------------------")

    best_graph, best_score = evolve_population()

    nodes = best_graph.number_of_nodes()
    edges = best_graph.number_of_edges()
    degree = edges / nodes if nodes else 0

    print("\nBest Architecture Discovered")
    print("-----------------------------")

    print(
        f"nodes={nodes} edges={edges} "
        f"degree={round(degree,2)} "
        f"resilience={round(best_score,3)}"
    )


if __name__ == "__main__":

    run()
