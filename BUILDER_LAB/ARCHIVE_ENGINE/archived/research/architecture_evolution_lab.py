"""
NEXAH Architecture Evolution Lab

Evolutionary search for resilient system architectures.
"""

import random

from ENGINE.nexah_engine import NexahEngine
from ENGINE.results_store import store_result


class ArchitectureEvolutionLab:

    def __init__(self, population_size=10, generations=5):

        self.population_size = population_size
        self.generations = generations
        self.engine = NexahEngine()

    def evaluate_population(self):

        population_results = []

        for i in range(self.population_size):

            print(f"  Running architecture {i+1}/{self.population_size}")

            result = self.engine.run()

            resilience_score = None

            if "resilience" in result:
                resilience_score = result["resilience"].get("resilience_score")

            population_results.append(
                {
                    "result": result,
                    "score": resilience_score
                }
            )

        return population_results

    def select_best(self, population_results, top_k=3):

        ranked = sorted(
            population_results,
            key=lambda x: x["score"] if x["score"] is not None else 0,
            reverse=True
        )

        return ranked[:top_k]

    def mutate_architecture(self, architecture):

        # placeholder mutation logic
        # future versions can modify graph topology

        mutated = architecture

        return mutated

    def run(self):

        print("\nStarting Architecture Evolution Lab\n")

        best_global = None

        for generation in range(self.generations):

            print(f"\n=== Generation {generation+1}/{self.generations} ===\n")

            population_results = self.evaluate_population()

            best = self.select_best(population_results)

            best_architecture = best[0]["result"]

            best_score = best[0]["score"]

            print(f"\nBest resilience score: {best_score}\n")

            store_result(best_architecture, generation + 1)

            best_global = best_architecture

        print("\nEvolution process finished\n")

        return best_global


def run_evolution():

    lab = ArchitectureEvolutionLab(
        population_size=10,
        generations=5
    )

    best_system = lab.run()

    return best_system


if __name__ == "__main__":

    run_evolution()
