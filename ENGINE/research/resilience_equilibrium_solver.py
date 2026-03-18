"""
NEXAH Resilience Equilibrium Solver

Computes equilibrium / optimum architecture points from the learned
resilience field equation.

Model:

R(N, D) =
    a
    + b*N
    + c*D
    + d*log(N)
    + e*(1/D)
    + f*(N*D)

We numerically search for maxima of R(N,D).
"""

import os
import json
import math
import numpy as np


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

            if nodes == 0:
                continue

            degree = edges / nodes

            data.append((nodes, degree, res))

        except Exception:
            continue

    return data


def build_regression_matrix(data):

    X = []
    y = []

    for nodes, degree, res in data:

        if degree == 0:
            continue

        X.append([
            1,
            nodes,
            degree,
            math.log(nodes),
            1 / degree,
            nodes * degree
        ])

        y.append(res)

    return np.array(X), np.array(y)


def fit_field(X, y):

    coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)

    return coeffs


def predict_resilience(nodes, degree, coeffs):

    if degree == 0:
        return -999

    a, b, c, d, e, f = coeffs

    return (
        a
        + b * nodes
        + c * degree
        + d * math.log(nodes)
        + e * (1 / degree)
        + f * (nodes * degree)
    )


def search_equilibrium(coeffs):

    best_R = -999
    best_point = None

    # architecture search region
    for nodes in np.linspace(3, 15, 200):

        for degree in np.linspace(1.5, 6, 200):

            R = predict_resilience(nodes, degree, coeffs)

            if R > best_R:
                best_R = R
                best_point = (nodes, degree)

    return best_point, best_R


def run():

    print("\nNEXAH Resilience Equilibrium Solver")
    print("-----------------------------------")

    data = load_results()

    if len(data) < 6:
        print("Not enough data.")
        return

    X, y = build_regression_matrix(data)

    coeffs = fit_field(X, y)

    best_point, best_R = search_equilibrium(coeffs)

    nodes_opt, degree_opt = best_point

    edges_opt = nodes_opt * degree_opt

    print("\nEquilibrium Architecture")
    print("------------------------")

    print(f"optimal nodes  ≈ {nodes_opt:.2f}")
    print(f"optimal degree ≈ {degree_opt:.2f}")
    print(f"optimal edges  ≈ {edges_opt:.2f}")
    print(f"predicted resilience ≈ {best_R:.3f}")


if __name__ == "__main__":

    run()
