"""
NEXAH Resilience Attractor Detector

Identifies stable architecture attractors
in the explored architecture landscape.
"""

import statistics

from ENGINE.results_store import load_all_results


class ResilienceAttractorDetector:

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

    def detect_attractor(self):

        nodes, edges, resilience = self.extract_metrics()

        if not resilience:

            print("No experiment data available.")
            return

        mean_nodes = statistics.mean(nodes)
        mean_edges = statistics.mean(edges)
        mean_resilience = statistics.mean(resilience)

        attractor = {
            "nodes_center": round(mean_nodes, 2),
            "edges_center": round(mean_edges, 2),
            "resilience_center": round(mean_resilience, 3)
        }

        print("\nNEXAH Architecture Attractor")
        print("----------------------------")

        print("Nodes center:", attractor["nodes_center"])
        print("Edges center:", attractor["edges_center"])
        print("Resilience center:", attractor["resilience_center"])

        return attractor


def run_attractor_detection():

    detector = ResilienceAttractorDetector()

    attractor = detector.detect_attractor()

    return attractor


if __name__ == "__main__":

    run_attractor_detection()
