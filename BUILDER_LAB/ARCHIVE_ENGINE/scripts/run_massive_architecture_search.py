"""
NEXAH Massive Architecture Search

Runs large-scale architecture exploration using the NEXAH discovery engine
and stores results for later discovery analysis.
"""

from ENGINE.nexah_engine import NexahEngine
from ENGINE.results_store import store_result


class MassiveArchitectureSearch:

    def __init__(self, runs=100):
        """
        runs : number of architecture experiments
        """
        self.runs = runs
        self.engine = NexahEngine()

    def run(self):

        print("\nStarting Massive Architecture Search\n")

        results = []

        for i in range(self.runs):

            print(f"\n--- Experiment {i+1}/{self.runs} ---")

            result = self.engine.run()

            # store experiment result
            store_result(result, i + 1)

            results.append(result)

        print("\nMassive Architecture Search finished\n")

        return results


# ------------------------------------------------
# Runner
# ------------------------------------------------

def run_search():

    search = MassiveArchitectureSearch(runs=20)

    results = search.run()

    print("\nExperiments completed:", len(results))

    return results


if __name__ == "__main__":

    run_search()
