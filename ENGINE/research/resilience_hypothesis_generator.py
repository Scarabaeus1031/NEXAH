"""
NEXAH Resilience Hypothesis Generator

Generates candidate mathematical hypotheses
that may explain resilience behaviour.

The generator explores combinations of
network variables and mathematical transforms.
"""

import os
import json
import math
import random

RESULT_DIR = "results"


def load_results():

    results = []

    if not os.path.exists(RESULT_DIR):
        return results

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        with open(path) as file:

            data = json.load(file)

            nodes = data.get("nodes")
            edges = data.get("edges")
            resilience = data.get("resilience_score")

            if nodes and edges:

                degree = edges / nodes

                results.append({
                    "nodes": nodes,
                    "edges": edges,
                    "degree": degree,
                    "inv_degree": 1 / degree if degree != 0 else 0,
                    "log_nodes": math.log(nodes),
                    "log_edges": math.log(edges),
                    "resilience": resilience
                })

    return results


def generate_hypotheses():

    base_vars = [
        "nodes",
        "edges",
        "degree",
        "inv_degree",
        "log_nodes",
        "log_edges"
    ]

    hypotheses = []

    for _ in range(25):

        v1 = random.choice(base_vars)
        v2 = random.choice(base_vars)

        hypothesis = f"Resilience ≈ a + b*{v1} + c*{v2}"

        hypotheses.append((v1, v2, hypothesis))

    return hypotheses


def evaluate_hypothesis(results, v1, v2):

    xs1 = []
    xs2 = []
    ys = []

    for r in results:

        xs1.append(r[v1])
        xs2.append(r[v2])
        ys.append(r["resilience"])

    # simple score: correlation with linear combination

    score = 0

    for i in range(len(xs1)):

        score += abs(xs1[i] * 0.5 + xs2[i] * 0.5 - ys[i])

    score = score / len(xs1)

    return score


def run_hypothesis_generation():

    print("\nNEXAH Hypothesis Generator")
    print("--------------------------")

    results = load_results()

    if len(results) < 5:
        print("Not enough experimental data.")
        return

    hypotheses = generate_hypotheses()

    scored = []

    for v1, v2, h in hypotheses:

        score = evaluate_hypothesis(results, v1, v2)

        scored.append((score, h))

    scored.sort()

    print("\nTop Hypotheses\n")

    for i in range(min(10, len(scored))):

        score, h = scored[i]

        print(f"{i+1}. {h}")
        print("   error:", round(score, 4))
        print()


if __name__ == "__main__":

    run_hypothesis_generation()
