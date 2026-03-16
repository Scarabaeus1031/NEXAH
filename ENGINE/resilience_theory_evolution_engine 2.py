"""
NEXAH Resilience Theory Evolution Engine

Attempts to evolve candidate mathematical laws
that explain resilience behaviour from experimental data.
"""

import os
import json
import math
import random

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

            # skip files that do not contain required fields
            if (
                "nodes" not in r
                or "edges" not in r
                or "resilience_score" not in r
            ):
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
                "inv_degree": 1 / degree if degree else 0,
                "log_nodes": math.log(nodes) if nodes > 0 else 0,
                "log_edges": math.log(edges) if edges > 0 else 0,
                "resilience": resilience
            })

        except Exception:
            # ignore malformed JSON files
            continue

    return data


VARIABLES = [
    "nodes",
    "edges",
    "degree",
    "inv_degree",
    "log_nodes",
    "log_edges"
]


def random_equation():

    v1 = random.choice(VARIABLES)
    v2 = random.choice(VARIABLES)

    a = random.uniform(-1, 1)
    b = random.uniform(-1, 1)
    c = random.uniform(-1, 1)

    return (a, b, c, v1, v2)


def evaluate_equation(eq, data):

    a, b, c, v1, v2 = eq

    errors = []

    for r in data:

        predicted = a + b * r[v1] + c * r[v2]

        errors.append(abs(predicted - r["resilience"]))

    return sum(errors) / len(errors)


def run_evolution():

    print("\nNEXAH Theory Evolution Engine")
    print("-----------------------------")

    data = load_results()

    if len(data) < 5:
        print("Not enough experimental data.")
        return

    population = [random_equation() for _ in range(200)]

    scored = []

    for eq in population:

        score = evaluate_equation(eq, data)

        scored.append((score, eq))

    scored.sort(key=lambda x: x[0])

    print("\nTop Candidate Laws\n")

    for i in range(min(10, len(scored))):

        score, eq = scored[i]

        a, b, c, v1, v2 = eq

        print(
            f"{i+1}. Resilience ≈ {round(a,4)} "
            f"+ {round(b,4)}*{v1} "
            f"+ {round(c,4)}*{v2}"
        )

        print("   error:", round(score, 5))
        print()


if __name__ == "__main__":

    run_evolution()
