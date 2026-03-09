"""
NEXAH Resilience Architecture Unified Law Finder

Attempts to discover a unified empirical law for resilience
based on architecture parameters.

Variables used:
- nodes
- edges
- degree
- log(nodes)
- log(edges)
- 1/degree
"""

import os
import json
import math
import statistics


RESULT_DIR = "results"


def load_results():

    results = []

    if not os.path.exists(RESULT_DIR):
        return results

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        with open(path, "r") as file:

            data = json.load(file)

            nodes = data["graph"]["nodes"]
            edges = data["graph"]["edges"]

            resilience = data["resilience"]["resilience_score"]

            degree = edges / nodes if nodes > 0 else 0

            results.append({
                "nodes": nodes,
                "edges": edges,
                "degree": degree,
                "resilience": resilience
            })

    return results


def correlation(xs, ys):

    if len(xs) < 2:
        return 0

    mean_x = statistics.mean(xs)
    mean_y = statistics.mean(ys)

    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))

    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))

    if den_x == 0 or den_y == 0:
        return 0

    return num / (den_x * den_y)


def build_feature_sets(results):

    features = {}

    nodes = [r["nodes"] for r in results]
    edges = [r["edges"] for r in results]
    degree = [r["degree"] for r in results]
    resilience = [r["resilience"] for r in results]

    features["nodes"] = nodes
    features["edges"] = edges
    features["degree"] = degree

    features["log(nodes)"] = [math.log(n) for n in nodes]
    features["log(edges)"] = [math.log(e) for e in edges]

    features["1/degree"] = [1/d if d != 0 else 0 for d in degree]

    features["edges/nodes"] = [
        edges[i] / nodes[i] if nodes[i] > 0 else 0
        for i in range(len(nodes))
    ]

    features["nodes/edges"] = [
        nodes[i] / edges[i] if edges[i] > 0 else 0
        for i in range(len(nodes))
    ]

    features["log(nodes)/degree"] = [
        math.log(nodes[i]) / degree[i] if degree[i] > 0 else 0
        for i in range(len(nodes))
    ]

    return features, resilience


def discover_laws(results):

    features, resilience = build_feature_sets(results)

    correlations = []

    for name, values in features.items():

        corr = correlation(values, resilience)

        correlations.append((name, corr))

    correlations.sort(key=lambda x: abs(x[1]), reverse=True)

    return correlations


def print_results(correlations):

    print("\nNEXAH Architecture Unified Law Finder")
    print("-------------------------------------")

    print("\nFeature correlations\n")

    for name, corr in correlations:

        print(f"{name:20s} correlation = {round(corr,3)}")

    best = correlations[0]

    print("\nBest candidate unified law:")

    print(f"Resilience ≈ f({best[0]})")


def run_discovery():

    results = load_results()

    if not results:

        print("No experiment results found.")
        return

    correlations = discover_laws(results)

    print_results(correlations)


if __name__ == "__main__":

    run_discovery()
