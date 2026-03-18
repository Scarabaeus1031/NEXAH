"""
Architecture Mutation Engine

Generates new architecture variants by applying structural mutations.

Used for evolutionary exploration of architecture space.
"""

import random


class ArchitectureMutationEngine:

    def __init__(self, mutation_rate=0.1):

        self.mutation_rate = mutation_rate

    # --------------------------------------------------

    def mutate_architecture(self, architecture):

        nodes = list(architecture.nodes)
        edges = list(architecture.edges)

        mutation_type = random.choice([
            "add_node",
            "remove_node",
            "add_edge",
            "remove_edge"
        ])

        if mutation_type == "add_node":

            new_node = f"N{len(nodes)+1}"
            nodes.append(new_node)

        elif mutation_type == "remove_node" and nodes:

            node = random.choice(nodes)
            nodes.remove(node)

            edges = [
                e for e in edges
                if node not in e
            ]

        elif mutation_type == "add_edge" and len(nodes) >= 2:

            a, b = random.sample(nodes, 2)
            edges.append((a, b))

        elif mutation_type == "remove_edge" and edges:

            edge = random.choice(edges)
            edges.remove(edge)

        architecture.nodes = nodes
        architecture.edges = edges

        return architecture

    # --------------------------------------------------

    def evolve_population(self, architectures, generations=10):

        population = architectures

        for _ in range(generations):

            new_population = []

            for arch in population:

                mutated = self.mutate_architecture(arch)

                new_population.append(mutated)

            population = new_population

        return population
