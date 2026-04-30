"""
NEXAH Meta Discovery Engine

Self-directed research engine.

Strategy:

analyze discovered architecture law
→ focus exploration near stability ridge
→ generate targeted experiments
→ update knowledge base
"""

import os
import json
import random
import statistics

import networkx as nx

from tools.resilience_analyzer_v2 import analyze_resilience


RESULT_DIR = "results"
EXPERIMENTS = 12


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


def estimate_architecture_law(data):

    ranked = sorted(data, key=lambda x: x["resilience"], reverse=True)

    top = ranked[:20]

    nodes = statistics.mean([r["nodes"] for r in top])
    degree = statistics.mean([r["degree"] for r in top])

    return nodes, degree


def generate_targeted_architecture(target_nodes, target_degree):

    nodes = max(3, int(random.gauss(target_nodes, 1.2)))

    degree = max(1.5, random.gauss(target_degree, 0.6))

    edges = int(nodes * degree)

    edges = min(edges, nodes * nodes - 1)

    G = nx.gnm_random_graph(nodes, edges, directed=True)

    return G


def run_experiments(target_nodes, target_degree):

    print("\nRunning Targeted Experiments")
    print("-----------------------------")

    best = None

    for i in range(EXPERIMENTS):

        G = generate_targeted_architecture(target_nodes, target_degree)

        report = analyze_resilience(G)

        nodes = report["nodes"]
        edges = report["edges"]
        res = report["resilience_score"]

        degree = edges / nodes if nodes else 0

        print(
            f"Test {i+1} | "
            f"nodes={nodes} | "
            f"edges={edges} | "
            f"degree={round(degree,2)} | "
            f"resilience={round(res,3)}"
        )

        if best is None or res > best["resilience"]:

            best = {
                "nodes": nodes,
                "edges": edges,
                "degree": degree,
                "resilience": res
            }

    print("\nBest Architecture Found")
    print("-----------------------")

    print(
        f"nodes={best['nodes']} "
        f"edges={best['edges']} "
        f"degree={round(best['degree'],2)} "
        f"resilience={round(best['resilience'],3)}"
    )


def run():

    print("\nNEXAH Meta Discovery Engine")
    print("---------------------------")

    data = load_results()

    if len(data) < 10:

        print("Not enough experimental data.")

        return

    nodes, degree = estimate_architecture_law(data)

    print("\nCurrent Architecture Law Estimate\n")

    print(f"nodes ≈ {round(nodes,2)}")
    print(f"degree ≈ {round(degree,2)}")

    run_experiments(nodes, degree)


if __name__ == "__main__":

    run()
