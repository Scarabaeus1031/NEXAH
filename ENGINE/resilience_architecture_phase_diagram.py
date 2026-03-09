"""
NEXAH Resilience Architecture Phase Diagram

Builds a 2D phase diagram of architecture space.

Axes:
X = Nodes
Y = Edges / Nodes (degree proxy)

Color = Resilience
"""

import os
import json
import math

import matplotlib.pyplot as plt


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

                # possible formats
                if "num_nodes" in graph:
                    nodes = graph["num_nodes"]

                if "num_edges" in graph:
                    edges = graph["num_edges"]

                if nodes is None and "nodes" in graph:
                    nodes = len(graph["nodes"])

                if edges is None and "edges" in graph:
                    edges = len(graph["edges"])

                resilience = res.get("resilience_score")

                if nodes is None or edges is None or resilience is None:
                    continue

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


def plot_phase_diagram(data):

    nodes = [d["nodes"] for d in data]
    degree = [d["degree"] for d in data]
    resilience = [d["resilience"] for d in data]

    plt.figure(figsize=(10, 7))

    scatter = plt.scatter(
        nodes,
        degree,
        c=resilience,
        cmap="viridis",
        s=100
    )

    plt.xlabel("Nodes")
    plt.ylabel("Edges / Nodes (Average Degree)")
    plt.title("NEXAH Architecture Phase Diagram")

    cbar = plt.colorbar(scatter)
    cbar.set_label("Resilience")

    plt.grid(True)

    plt.show()


def run():

    data = load_results()

    if not data:
        print("No experiment results found.")
        return

    print(f"Loaded {len(data)} architectures")

    plot_phase_diagram(data)


if __name__ == "__main__":

    run()
