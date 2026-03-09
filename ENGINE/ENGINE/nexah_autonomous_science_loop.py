"""
NEXAH Autonomous Science Loop

Autonomous discovery cycle:

plan experiments
→ run resilience analysis
→ store results
→ generate simple statistics

This module orchestrates the existing NEXAH discovery system.
"""

import os
import json
import random
import statistics

import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


RESULT_DIR = "results"
EXPERIMENTS_PER_RUN = 12


def ensure_results_dir():

    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)


def next_filename():

    files = [
        f for f in os.listdir(RESULT_DIR)
        if f.startswith("auto_experiment") and f.endswith(".json")
    ]

    idx = len(files) + 1

    return os.path.join(
        RESULT_DIR,
        f"auto_experiment_{idx:04d}.json"
    )


def generate_architecture():

    nodes = random.randint(4, 12)

    degree = random.uniform(2.5, 5.0)

    edges = int(nodes * degree)

    edges = min(edges, nodes * nodes - 1)

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

    filename = next_filename()

    with open(filename, "w") as f:
        json.dump(result, f, indent=2)


def load_all_results():

    results = []

    if not os.path.exists(RESULT_DIR):
        return results

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        with open(path) as file:

            data = json.load(file)

            if "resilience_score" in data:

                results.append(data)

    return results


def summarize(results):

    if len(results) == 0:
        return

    best = max(results, key=lambda r: r["resilience_score"])

    avg_res = statistics.mean([r["resilience_score"] for r in results])

    print("\nCurrent Global Results")
    print("----------------------")

    print("Experiments:", len(results))
    print("Average resilience:", round(avg_res, 3))

    print(
        "Best architecture:",
        f"nodes={best['nodes']}",
        f"edges={best['edges']}",
        f"degree={round(best['degree'],2)}",
        f"resilience={round(best['resilience_score'],3)}"
    )


def run_autonomous_loop():

    print("\nNEXAH Autonomous Science Loop")
    print("-----------------------------")

    ensure_results_dir()

    for i in range(EXPERIMENTS_PER_RUN):

        result = run_experiment()

        store_result(result)

        print(
            f"Experiment {i+1} | "
            f"nodes={result['nodes']} | "
            f"edges={result['edges']} | "
            f"degree={round(result['degree'],2)} | "
            f"resilience={round(result['resilience_score'],3)}"
        )

    results = load_all_results()

    summarize(results)


if __name__ == "__main__":

    run_autonomous_loop()
