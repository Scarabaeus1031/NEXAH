"""
NEXAH Resilience Stability Ridge Detector

Finds the most stable regions ("ridges") in the explored
architecture landscape based on stored experiment results.
"""

import os
import json
import statistics

RESULT_DIR = "results"


def load_results():

    results = []

    if not os.path.exists(RESULT_DIR):
        print("Results directory not found.")
        return results

    for file in os.listdir(RESULT_DIR):

        if not file.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, file)

        try:
            with open(path, "r") as f:

                data = json.load(f)

                graph = data.get("graph", {})
                resilience = data.get("resilience", {}).get("resilience_score")

                nodes = None
                edges = None

                # possible graph formats
                if "num_nodes" in graph:
                    nodes = graph["num_nodes"]

                if "num_edges" in graph:
                    edges = graph["num_edges"]

                if nodes is None and "nodes" in graph:
                    nodes = len(graph["nodes"])

                if edges is None and "edges" in graph:
                    edges = len(graph["edges"])

                if nodes is None or edges is None or resilience is None:
                    continue

                results.append(
                    {
                        "nodes": nodes,
                        "edges": edges,
                        "resilience": resilience
                    }
                )

        except Exception:
            continue

    return results


def detect_ridges(results):

    if not results:
        return []

    # sort by resilience descending
    sorted_results = sorted(
        results,
        key=lambda r: r["resilience"],
        reverse=True
    )

    # take top architectures
    top = sorted_results[:5]

    return top


def print_ridges(ridges):

    print("\nNEXAH Stability Ridge Detector")
    print("--------------------------------")

    if not ridges:
        print("No ridge candidates found.")
        return

    for i, r in enumerate(ridges):

        print(
            f"Rank {i+1} | "
            f"nodes: {r['nodes']} | "
            f"edges: {r['edges']} | "
            f"resilience: {round(r['resilience'],3)}"
        )


def compute_statistics(results):

    nodes = [r["nodes"] for r in results]
    edges = [r["edges"] for r in results]
    resilience = [r["resilience"] for r in results]

    print("\nLandscape Statistics")
    print("--------------------")

    print("Experiments:", len(results))
    print("Average nodes:", round(statistics.mean(nodes), 2))
    print("Average edges:", round(statistics.mean(edges), 2))
    print("Average resilience:", round(statistics.mean(resilience), 3))

    print("Max resilience:", round(max(resilience), 3))
    print("Min resilience:", round(min(resilience), 3))


def run():

    results = load_results()

    if not results:
        print("No experiment data found.")
        return

    compute_statistics(results)

    ridges = detect_ridges(results)

    print_ridges(ridges)


if __name__ == "__main__":

    run()
