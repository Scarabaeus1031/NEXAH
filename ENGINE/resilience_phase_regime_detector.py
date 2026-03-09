"""
NEXAH Resilience Phase Regime Detector

Detects sparse, transition, and dense resilience regimes
from stored experiment results.

Axes used:
- nodes
- degree = edges / nodes
- resilience
"""

import os
import json
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


def compute_thresholds(results):

    resilience_values = [r["resilience"] for r in results]

    collapse_threshold = statistics.quantiles(resilience_values, n=3)[0]
    resilient_threshold = statistics.quantiles(resilience_values, n=3)[1]

    return collapse_threshold, resilient_threshold


def classify_regimes(results, collapse_threshold, resilient_threshold):

    collapse = []
    transition = []
    resilient = []

    for r in results:

        if r["resilience"] <= collapse_threshold:
            collapse.append(r)

        elif r["resilience"] >= resilient_threshold:
            resilient.append(r)

        else:
            transition.append(r)

    return collapse, transition, resilient


def print_summary(collapse, transition, resilient):

    print("\nNEXAH Resilience Phase Regime Detector")
    print("--------------------------------------")

    print("\nCollapse regime:", len(collapse))
    print("Transition regime:", len(transition))
    print("Resilient regime:", len(resilient))

    if resilient:

        best = max(resilient, key=lambda r: r["resilience"])

        print("\nBest resilient architecture")

        print(
            f"nodes={best['nodes']} "
            f"| edges={best['edges']} "
            f"| degree={round(best['degree'],2)} "
            f"| resilience={round(best['resilience'],3)}"
        )


def run_detector():

    results = load_results()

    if not results:

        print("No experiment data found.")
        return

    collapse_threshold, resilient_threshold = compute_thresholds(results)

    print("\nPhase thresholds")
    print("Collapse threshold:", round(collapse_threshold, 3))
    print("Resilient threshold:", round(resilient_threshold, 3))

    collapse, transition, resilient = classify_regimes(
        results,
        collapse_threshold,
        resilient_threshold
    )

    print_summary(collapse, transition, resilient)


if __name__ == "__main__":

    run_detector()
