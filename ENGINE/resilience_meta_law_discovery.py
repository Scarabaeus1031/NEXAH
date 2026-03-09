"""
NEXAH Meta Law Discovery Engine

Tries multiple candidate formulas to discover
scaling laws for resilience.

Resilience ≈ f(nodes, edges, degree)
"""

import os
import json
import math
import statistics


RESULT_DIR = "results"


def load_results():

    data = []

    if not os.path.exists(RESULT_DIR):
        return data

    for file in os.listdir(RESULT_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, file)

        try:

            with open(path) as f:

                r = json.load(f)

                graph = r.get("graph", {})
                res = r.get("resilience", {})

                nodes = None
                edges = None

                if "num_nodes" in graph:
                    nodes = graph["num_nodes"]

                if "num_edges" in graph:
                    edges = graph["num_edges"]

                if nodes is None and "nodes" in graph:
                    nodes = len(graph["nodes"])

                if edges is None and "edges" in graph:
                    edges = len(graph["edges"])

                resilience = res.get("resilience_score")

                if nodes and edges and resilience:

                    degree = edges / nodes

                    data.append({
                        "nodes": nodes,
                        "edges": edges,
                        "degree": degree,
                        "resilience": resilience
                    })

        except Exception:
            continue

    return data


def correlation(x, y):

    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)

    num = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
    den_x = sum((a - mean_x) ** 2 for a in x)
    den_y = sum((b - mean_y) ** 2 for b in y)

    if den_x == 0 or den_y == 0:
        return 0

    return num / math.sqrt(den_x * den_y)


def evaluate_models(data):

    nodes = [d["nodes"] for d in data]
    edges = [d["edges"] for d in data]
    degree = [d["degree"] for d in data]
    resilience = [d["resilience"] for d in data]

    models = {}

    models["degree"] = degree
    models["1/degree"] = [1/d for d in degree]
    models["log(nodes)"] = [math.log(n) for n in nodes]
    models["nodes/edges"] = [n/e for n, e in zip(nodes, edges)]
    models["edges/nodes"] = [e/n for n, e in zip(nodes, edges)]
    models["log(nodes)/degree"] = [math.log(n)/d for n, d in zip(nodes, degree)]
    models["nodes/log(edges)"] = [n/math.log(e) for n, e in zip(nodes, edges)]

    print("\nNEXAH Meta Law Discovery")
    print("------------------------\n")

    results = []

    for name, values in models.items():

        try:
            corr = correlation(values, resilience)
            results.append((name, corr))
        except Exception:
            continue

    results.sort(key=lambda x: abs(x[1]), reverse=True)

    for name, corr in results:

        print(f"{name:20} correlation = {round(corr,3)}")

    best = results[0]

    print("\nBest candidate law:")
    print(f"Resilience ≈ f({best[0]})")


def run():

    data = load_results()

    if not data:
        print("No experiment data found.")
        return

    evaluate_models(data)


if __name__ == "__main__":

    run()
