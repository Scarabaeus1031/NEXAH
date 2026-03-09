"""
NEXAH Massive Architecture Search

Runs large-scale architecture exploration using the NEXAH engine.
"""

from nexah_engine import NexahEngine
from architecture_mutation_engine import ArchitectureMutationEngine

from tools.system_designer import generate_architecture


class MassiveArchitectureSearch:

    def __init__(self,
                 population_size=50,
                 generations=10):

        self.population_size = population_size
        self.generations = generations

        self.engine = NexahEngine()
        self.mutator = ArchitectureMutationEngine()

    # --------------------------------------------------

    def initialize_population(self):

        population = []

        for _ in range(self.population_size):

            arch = generate_architecture()

            population.append(arch)

        return population

    # --------------------------------------------------

    def evolve_population(self, population):

        return self.mutator.evolve_population(
            population,
            generations=self.generations
        )

    # --------------------------------------------------

    def evaluate_population(self, population):

        results = []

        for architecture in population:

            result = self.engine.run()

            results.append(result)

        return results

    # --------------------------------------------------

    def run(self):

        print("Starting massive architecture search")

        population = self.initialize_population()

        population = self.evolve_population(population)

        results = self.evaluate_population(population)

        print("Search finished")

        return results


def run_search():

    search = MassiveArchitectureSearch(
        population_size=50,
        generations=20
    )

    results = search.run()

    return results


if __name__ == "__main__":

    run_search()
