"""
NEXAH Resilience Topology Miner

Analyzes stored experiment results and detects structural
patterns in resilient architectures.
"""

import statistics

from ENGINE.results_store import load_all_results


class ResilienceTopologyMiner:

    def __init__(self):

        self.results = load_all_results()

    def extract_graph_metrics(self, graph):

        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])

        n = len(nodes)
        e = len(edges)

        avg_degree = 0
        if n > 0:
            avg_degree = (2 * e) / n

        return {
            "nodes": n,
            "edges": e,
            "avg_degree": avg_degree
        }

    def analyze(self):

        if not self.results:

            print("No experiment results found.")
            return

        resilience_scores = []
        node_counts = []
        edge_counts = []
        degrees = []

        for result in self.results:

            graph = result.get("graph")

            if not graph:
                continue

            metrics = self.extract_graph_metrics(graph)

            node_counts.append(metrics["nodes"])
            edge_counts.append(metrics["edges"])
            degrees.append(metrics["avg_degree"])

            resilience = result.get("resilience", {})
            score = resilience.get("resilience_score")

            if score is not None:
                resilience_scores.append(score)

        print("\nNEXAH Topology Analysis")
        print("----------------------")

        print("Experiments analyzed:", len(self.results))

        if resilience_scores:
            print("Average resilience:", round(statistics.mean(resilience_scores), 3))
            print("Best resilience:", round(max(resilience_scores), 3))
            print("Worst resilience:", round(min(resilience_scores), 3))

        if node_counts:
            print("Average nodes:", round(statistics.mean(node_counts), 2))

        if edge_counts:
            print("Average edges:", round(statistics.mean(edge_counts), 2))

        if degrees:
            print("Average degree:", round(statistics.mean(degrees), 2))

        return {
            "experiments": len(self.results),
            "avg_resilience": statistics.mean(resilience_scores) if resilience_scores else None,
            "avg_nodes": statistics.mean(node_counts) if node_counts else None,
            "avg_edges": statistics.mean(edge_counts) if edge_counts else None,
            "avg_degree": statistics.mean(degrees) if degrees else None
        }


def run_topology_mining():

    miner = ResilienceTopologyMiner()

    summary = miner.analyze()

    return summary


if __name__ == "__main__":

    run_topology_mining()
