"""
NEXAH Resilience Phase Map

Detects phase regions in architecture space.
"""

import statistics
import matplotlib.pyplot as plt

from ENGINE.results_store import load_all_results


class ResiliencePhaseMap:

    def __init__(self):

        self.results = load_all_results()

    def extract_metrics(self):

        nodes = []
        edges = []
        resilience = []

        for r in self.results:

            graph = r.get("graph", {})
            res = r.get("resilience", {})

            n = len(graph.get("nodes", []))
            e = len(graph.get("edges", []))
            s = res.get("resilience_score")

            if s is None:
                continue

            nodes.append(n)
            edges.append(e)
            resilience.append(s)

        return nodes, edges, resilience

    def compute_phases(self, resilience):

        mean = statistics.mean(resilience)
        std = statistics.stdev(resilience) if len(resilience) > 1 else 0

        collapse_threshold = mean - std
        resilient_threshold = mean + std

        return collapse_threshold, resilient_threshold

    def visualize(self):

        nodes, edges, resilience = self.extract_metrics()

        if not nodes:
            print("No experiment data available.")
            return

        collapse_t, resilient_t = self.compute_phases(resilience)

        colors = []

        for r in resilience:

            if r < collapse_t:
                colors.append("red")

            elif r > resilient_t:
                colors.append("green")

            else:
                colors.append("orange")

        plt.figure()

        scatter = plt.scatter(
            nodes,
            edges,
            c=colors
        )

        plt.xlabel("Nodes")
        plt.ylabel("Edges")
        plt.title("NEXAH Resilience Phase Map")

        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label='Collapse Regime', markerfacecolor='red', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Transition Regime', markerfacecolor='orange', markersize=10),
            plt.Line2D([0], [0], marker='o', color='w', label='Resilient Regime', markerfacecolor='green', markersize=10)
        ]

        plt.legend(handles=legend_elements)

        plt.show()

        print("\nPhase thresholds:")
        print("Collapse threshold:", round(collapse_t, 3))
        print("Resilient threshold:", round(resilient_t, 3))


def run_phase_map():

    mapper = ResiliencePhaseMap()

    mapper.visualize()


if __name__ == "__main__":

    run_phase_map()
