"""
NEXAH Resilience Experiment Planner

Designs new architecture experiments based on
discovered resilience patterns and stores them
for future hypothesis discovery.
"""

import os
import json
import random

import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


RESULT_DIR = "results"


def ensure_results_dir():

    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)


def generate_architecture():

    # cluster range discovered earlier
    nodes = random.randint(4, 12)

    # preferred degree window
    degree = random.uniform(2.5, 5.0)

    edges = int(nodes * degree)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def run_experiment():

    G = generate_architecture()

    report = analyze_resilience(G)

    result = {
        "nodes": report["nodes"],
        "edges": report["edges"],
        "degree": report["edges"] / report["nodes"],
        "resilience_score": report["resilience_score"]
    }

    return result


def store_result(result):

    existing = len(os.listdir(RESULT_DIR))

    filename = f"experiment_{existing+1}.json"

    path = os.path.join(RESULT_DIR, filename)

    with open(path, "w") as f:
        json.dump(result, f, indent=2)


def run_planner():

    print("\nNEXAH Experiment Planner")
    print("------------------------")

    ensure_results_dir()

    for i in range(10):

        result = run_experiment()

        store_result(result)

        print(
            f"Experiment {i+1} | "
            f"nodes={result['nodes']} | "
            f"edges={result['edges']} | "
            f"degree={round(result['degree'],2)} | "
            f"resilience={round(result['resilience_score'],3)}"
        )


if __name__ == "__main__":

    run_planner()
