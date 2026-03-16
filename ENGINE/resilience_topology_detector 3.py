"""
NEXAH Resilience Topology Detector

Analyzes architecture experiment results and detects
topological structures in the resilience landscape.

Detects:

• stability ridge
• transition region
• outlier architectures
• architecture basins

Axes used:
nodes
degree
resilience
"""

import os
import json
import statistics
import math


RESULT_DIR = "results"


def load_results():

    data = []

    if not os.path.exists(RESULT_DIR):
        return data

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        try:

            with open(path) as file:

                r = json.load(file)

                if "nodes" not in r:
                    continue

                nodes = r["nodes"]
                edges = r["edges"]
                resilience = r["resilience_score"]

                if nodes == 0:
                    continue

                degree = edges / nodes

                data.append({
                    "nodes": nodes,
                    "edges": edges,
                    "degree": degree,
                    "resilience": resilience
                })

        except:
            continue

    return data


def detect_ridge(data):

    # ridge = top resilience region

    sorted_data = sorted(data, key=lambda x: x["resilience"], reverse=True)

    ridge = sorted_data[:max(3, len(sorted_data)//5)]

    nodes = [x["nodes"] for x in ridge]
    degree = [x["degree"] for x in ridge]
    res = [x["resilience"] for x in ridge]

    return {
        "nodes_mean": statistics.mean(nodes),
        "degree_mean": statistics.mean(degree),
        "resilience_mean": statistics.mean(res),
        "max_resilience": max(res)
    }


def detect_transition_region(data):

    # transition = mid resilience region

    res_values = [x["resilience"] for x in data]

    mean_res = statistics.mean(res_values)

    transition = []

    for x in data:

        if abs(x["resilience"] - mean_res) < 0.05:
            transition.append(x)

    if len(transition) == 0:
        return None

    nodes = [x["nodes"] for x in transition]
    degree = [x["degree"] for x in transition]

    return {
        "count": len(transition),
        "nodes_mean": statistics.mean(nodes),
        "degree_mean": statistics.mean(degree),
        "resilience_center": mean_res
    }


def detect_outliers(data):

    res_values = [x["resilience"] for x in data]

    mean_res = statistics.mean(res_values)
    std_res = statistics.stdev(res_values) if len(res_values) > 2 else 0

    outliers = []

    for x in data:

        if abs(x["resilience"] - mean_res) > 2 * std_res:
            outliers.append(x)

    return outliers


def run_detector():

    print("\nNEXAH Resilience Topology Detector")
    print("----------------------------------")

    data = load_results()

    if len(data) == 0:

        print("No experiment data found.")
        return

    ridge = detect_ridge(data)
    transition = detect_transition_region(data)
    outliers = detect_outliers(data)

    print("\nStability Ridge")
    print("----------------")

    print("nodes ≈", round(ridge["nodes_mean"],2))
    print("degree ≈", round(ridge["degree_mean"],2))
    print("avg resilience ≈", round(ridge["resilience_mean"],3))
    print("max resilience ≈", round(ridge["max_resilience"],3))

    print("\nTransition Region")
    print("-----------------")

    if transition:

        print("points:", transition["count"])
        print("nodes ≈", round(transition["nodes_mean"],2))
        print("degree ≈", round(transition["degree_mean"],2))
        print("center resilience ≈", round(transition["resilience_center"],3))

    else:

        print("No clear transition region detected.")

    print("\nOutlier Architectures")
    print("---------------------")

    if len(outliers) == 0:

        print("No strong outliers.")

    else:

        for o in outliers:

            print(
                "nodes=", o["nodes"],
                "degree=", round(o["degree"],2),
                "resilience=", round(o["resilience"],3)
            )


if __name__ == "__main__":

    run_detector()
