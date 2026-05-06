"""
NEXAH Universal Resilience Scaling Law Detector

Attempts to discover scaling relations between
network structure and resilience.
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

    for file in os.listdir(RESULT_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, file)

        try:
            with open(path) as f:

                data = json.load(f)

                graph = data.get("graph", {})
                res = data.get("resilience", {})

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

                    results.append({
                        "nodes": nodes,
                        "edges": edges,
                        "degree": degree,
                        "resilience": resilience
                    })

        except Exception:
            continue

    return results


def correlation(x, y):

    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)

    num = sum((a - mean_x)*(b - mean_y) for a,b in zip(x,y))
    den_x = sum((a - mean_x)**2 for a in x)
    den_y = sum((b - mean_y)**2 for b in y)

    if den_x == 0 or den_y == 0:
        return 0

    return num / math.sqrt(den_x * den_y)


def detect_laws(data):

    nodes = [d["nodes"] for d in data]
    edges = [d["edges"] for d in data]
    degree = [d["degree"] for d in data]
    resilience = [d["resilience"] for d in data]

    print("\nNEXAH Universal Scaling Law Detector")
    print("------------------------------------")

    print("\nCorrelations")

    print("nodes vs resilience:", round(correlation(nodes,resilience),3))
    print("edges vs resilience:", round(correlation(edges,resilience),3))
    print("degree vs resilience:", round(correlation(degree,resilience),3))

    log_nodes = [math.log(n) for n in nodes]
    inv_degree = [1/d for d in degree]

    print("log(nodes) vs resilience:", round(correlation(log_nodes,resilience),3))
    print("1/degree vs resilience:", round(correlation(inv_degree,resilience),3))

    avg_degree = statistics.mean(degree)

    print("\nEstimated scaling law")

    print("Resilience ≈ f(degree)")
    print("Typical stable degree ≈", round(avg_degree,3))


def run():

    data = load_results()

    if not data:
        print("No experiment data found.")
        return

    detect_laws(data)


if __name__ == "__main__":

    run()
