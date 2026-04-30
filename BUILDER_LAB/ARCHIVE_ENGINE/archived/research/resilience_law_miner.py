"""
NEXAH Resilience Law Miner

Discovers empirical relationships between
network structure and resilience from experiment results.
"""

import os
import json
import statistics


RESULT_DIR = "results"


def load_results():

    results = []

    if not os.path.exists(RESULT_DIR):
        return results

    for file in os.listdir(RESULT_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, file)

        with open(path, "r") as f:

            data = json.load(f)
            results.append(data)

    return results


def extract_metrics(results):

    nodes = []
    edges = []
    resilience = []

    for r in results:

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


def compute_correlations(nodes, edges, resilience):

    correlations = {}

    if len(nodes) < 2:
        return correlations

    def corr(x, y):

        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)

        num = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
        den_x = sum((a - mean_x) ** 2 for a in x) ** 0.5
        den_y = sum((b - mean_y) ** 2 for b in y) ** 0.5

        if den_x == 0 or den_y == 0:
            return 0

        return num / (den_x * den_y)

    correlations["nodes_vs_resilience"] = corr(nodes, resilience)
    correlations["edges_vs_resilience"] = corr(edges, resilience)

    degrees = [e / n if n > 0 else 0 for n, e in zip(nodes, edges)]
    correlations["degree_vs_resilience"] = corr(degrees, resilience)

    return correlations


def infer_laws(nodes, edges, resilience):

    laws = []

    degrees = [e / n if n > 0 else 0 for n, e in zip(nodes, edges)]

    avg_degree = statistics.mean(degrees)
    avg_resilience = statistics.mean(resilience)

    laws.append(
        f"Average degree ≈ {avg_degree:.2f} → resilience ≈ {avg_resilience:.3f}"
    )

    best_index = resilience.index(max(resilience))

    laws.append(
        f"Best architecture: nodes={nodes[best_index]}, edges={edges[best_index]}, resilience={resilience[best_index]:.3f}"
    )

    return laws


def run_law_miner():

    print("\nNEXAH Resilience Law Miner")
    print("--------------------------")

    results = load_results()

    if not results:
        print("No experiment results found.")
        return

    nodes, edges, resilience = extract_metrics(results)

    correlations = compute_correlations(nodes, edges, resilience)

    print("\nCorrelations")

    for k, v in correlations.items():
        print(f"{k}: {v:.3f}")

    laws = infer_laws(nodes, edges, resilience)

    print("\nInferred Laws")

    for law in laws:
        print("-", law)


if __name__ == "__main__":

    run_law_miner()
