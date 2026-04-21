"""
NEXAH Universal Resilience Law Detector

Attempts to discover simple scaling relations between
system topology and resilience score.
"""

import statistics

from ENGINE.results_store import load_all_results


class UniversalResilienceLawDetector:

    def __init__(self):

        self.results = load_all_results()

    def extract_metrics(self, result):

        graph = result.get("graph", {})
        resilience = result.get("resilience", {})

        nodes = len(graph.get("nodes", []))
        edges = len(graph.get("edges", []))

        degree = 0
        if nodes > 0:
            degree = (2 * edges) / nodes

        score = resilience.get("resilience_score")

        return nodes, edges, degree, score

    def compute_correlation(self, xs, ys):

        if len(xs) < 2:
            return None

        mean_x = statistics.mean(xs)
        mean_y = statistics.mean(ys)

        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        den_x = sum((x - mean_x) ** 2 for x in xs)
        den_y = sum((y - mean_y) ** 2 for y in ys)

        if den_x == 0 or den_y == 0:
            return 0

        return num / (den_x ** 0.5 * den_y ** 0.5)

    def analyze(self):

        nodes = []
        edges = []
        degrees = []
        resilience = []

        for r in self.results:

            n, e, d, s = self.extract_metrics(r)

            if s is None:
                continue

            nodes.append(n)
            edges.append(e)
            degrees.append(d)
            resilience.append(s)

        if not resilience:

            print("No resilience data found.")
            return

        print("\nNEXAH Universal Law Analysis")
        print("-----------------------------")

        corr_nodes = self.compute_correlation(nodes, resilience)
        corr_edges = self.compute_correlation(edges, resilience)
        corr_degree = self.compute_correlation(degrees, resilience)

        print("Correlation(nodes, resilience):", round(corr_nodes, 3))
        print("Correlation(edges, resilience):", round(corr_edges, 3))
        print("Correlation(degree, resilience):", round(corr_degree, 3))

        best = max(
            [
                ("nodes", corr_nodes),
                ("edges", corr_edges),
                ("degree", corr_degree),
            ],
            key=lambda x: abs(x[1]) if x[1] is not None else 0
        )

        print("\nStrongest structural predictor:", best[0])

        return {
            "nodes_corr": corr_nodes,
            "edges_corr": corr_edges,
            "degree_corr": corr_degree,
            "best_predictor": best[0],
        }


def run_law_detection():

    detector = UniversalResilienceLawDetector()

    summary = detector.analyze()

    return summary


if __name__ == "__main__":

    run_law_detection()
