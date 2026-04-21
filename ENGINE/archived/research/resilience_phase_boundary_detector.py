"""
NEXAH Resilience Phase Boundary Detector

Detects boundaries between collapse, transition,
and resilient regimes in architecture space.
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


def compute_thresholds(resilience):

    mean = statistics.mean(resilience)
    std = statistics.stdev(resilience)

    collapse = mean - std * 0.5
    resilient = mean + std * 0.5

    return collapse, resilient


def classify(nodes, edges, resilience, collapse, resilient):

    collapse_points = []
    transition_points = []
    resilient_points = []

    for n, e, r in zip(nodes, edges, resilience):

        point = (n, e, r)

        if r <= collapse:
            collapse_points.append(point)

        elif r >= resilient:
            resilient_points.append(point)

        else:
            transition_points.append(point)

    return collapse_points, transition_points, resilient_points


def print_boundary_report(collapse_points, transition_points, resilient_points):

    print("\nNEXAH Phase Boundary Detector")
    print("-----------------------------")

    print("\nCollapse region size:", len(collapse_points))
    print("Transition region size:", len(transition_points))
    print("Resilient region size:", len(resilient_points))

    if resilient_points:

        best = max(resilient_points, key=lambda x: x[2])

        print("\nBest resilient architecture")
        print("Nodes:", best[0])
        print("Edges:", best[1])
        print("Resilience:", best[2])


def run_phase_boundary_detector():

    results = load_results()

    if not results:
        print("No experiment data available.")
        return

    nodes, edges, resilience = extract_metrics(results)

    collapse, resilient = compute_thresholds(resilience)

    print("\nPhase thresholds")
    print("Collapse threshold:", round(collapse, 3))
    print("Resilient threshold:", round(resilient, 3))

    collapse_points, transition_points, resilient_points = classify(
        nodes, edges, resilience, collapse, resilient
    )

    print_boundary_report(collapse_points, transition_points, resilient_points)


if __name__ == "__main__":

    run_phase_boundary_detector()
