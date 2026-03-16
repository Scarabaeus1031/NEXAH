"""
NEXAH Universal Architecture Law AI

Attempts to derive a universal architecture law
from discovered resilience experiments.
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


def analyze_architecture(data):

    # take top architectures
    ranked = sorted(data, key=lambda x: x["resilience"], reverse=True)

    top = ranked[:20]

    nodes = [r["nodes"] for r in top]
    edges = [r["edges"] for r in top]
    degrees = [r["degree"] for r in top]
    res = [r["resilience"] for r in top]

    return {
        "nodes_mean": statistics.mean(nodes),
        "edges_mean": statistics.mean(edges),
        "degree_mean": statistics.mean(degrees),
        "resilience_mean": statistics.mean(res),
        "resilience_max": max(res)
    }


def derive_law(stats):

    nodes = stats["nodes_mean"]
    degree = stats["degree_mean"]

    edges = nodes * degree

    law = {
        "optimal_nodes": round(nodes, 2),
        "optimal_degree": round(degree, 2),
        "optimal_edges": round(edges, 2)
    }

    return law


def print_law(stats, law):

    print("\nNEXAH Universal Architecture Law")
    print("--------------------------------")

    print("\nObserved Stability Region\n")

    print("average nodes:", round(stats["nodes_mean"], 2))
    print("average degree:", round(stats["degree_mean"], 2))
    print("average edges:", round(stats["edges_mean"], 2))

    print("\nPeak Resilience\n")

    print("mean resilience:", round(stats["resilience_mean"], 3))
    print("max resilience:", round(stats["resilience_max"], 3))

    print("\nDerived Architecture Law\n")

    print(
        "Optimal Architecture:\n"
        f"nodes ≈ {law['optimal_nodes']}\n"
        f"degree ≈ {law['optimal_degree']}\n"
        f"edges ≈ nodes × degree ≈ {law['optimal_edges']}"
    )


def run():

    print("\nNEXAH Universal Architecture Law AI")
    print("-----------------------------------")

    data = load_results()

    if len(data) < 10:

        print("Not enough experiment data.")

        return

    stats = analyze_architecture(data)

    law = derive_law(stats)

    print_law(stats, law)


if __name__ == "__main__":

    run()
