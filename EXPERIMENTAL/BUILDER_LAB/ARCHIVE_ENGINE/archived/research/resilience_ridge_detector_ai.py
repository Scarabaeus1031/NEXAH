"""
NEXAH Resilience Ridge Detector AI

Detects stability ridges and maxima in the resilience landscape.

Input:
stored experiment results

Output:
most stable architecture regions
"""

import os
import json
import statistics


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
                res = r["resilience_score"]

                degree = edges / nodes if nodes else 0

                data.append({
                    "nodes": nodes,
                    "edges": edges,
                    "degree": degree,
                    "resilience": res
                })

        except:
            continue

    return data


def detect_ridges(data):

    # sort by resilience
    ranked = sorted(data, key=lambda x: x["resilience"], reverse=True)

    top = ranked[:10]

    nodes = [r["nodes"] for r in top]
    degrees = [r["degree"] for r in top]
    resilience = [r["resilience"] for r in top]

    ridge = {
        "avg_nodes": statistics.mean(nodes),
        "avg_degree": statistics.mean(degrees),
        "avg_resilience": statistics.mean(resilience),
        "max_resilience": max(resilience)
    }

    return top, ridge


def print_results(top, ridge):

    print("\nNEXAH Resilience Ridge Detector")
    print("--------------------------------")

    print("\nTop Stable Architectures\n")

    for i, r in enumerate(top):

        print(
            f"{i+1}. nodes={r['nodes']} "
            f"edges={r['edges']} "
            f"degree={round(r['degree'],2)} "
            f"resilience={round(r['resilience'],3)}"
        )

    print("\nDetected Ridge Region\n")

    print(
        f"nodes ≈ {round(ridge['avg_nodes'],2)}"
    )

    print(
        f"degree ≈ {round(ridge['avg_degree'],2)}"
    )

    print(
        f"average resilience ≈ {round(ridge['avg_resilience'],3)}"
    )

    print(
        f"max resilience ≈ {round(ridge['max_resilience'],3)}"
    )


def run_detector():

    data = load_results()

    if len(data) < 5:

        print("Not enough experiment data.")

        return

    top, ridge = detect_ridges(data)

    print_results(top, ridge)


if __name__ == "__main__":

    run_detector()
