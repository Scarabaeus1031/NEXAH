"""
NEXAH Resilience Architecture Universal Field

Fits a simple analytic resilience field of the form:

    resilience ≈ a
               + b * nodes
               + c * degree
               + d * log(nodes)
               + e * (1 / degree)
               + f * (nodes * degree)

and visualizes the learned field as a continuous surface.

Axes:
X = nodes
Y = degree
Z = predicted resilience field
"""

import os
import json
import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
        return 0

    a, b, c, d, e, f = coeffs

    return (
        a
        + b * nodes
        + c * degree
        + d * math.log(nodes)
        + e * (1 / degree)
        + f * (nodes * degree)
    )


def build_surface(data, coeffs, resolution=40):

    nodes_vals = [d[0] for d in data]
    degree_vals = [d[1] for d in data]

    n_min, n_max = min(nodes_vals), max(nodes_vals)
    d_min, d_max = min(degree_vals), max(degree_vals)

    nodes_grid = np.linspace(n_min, n_max, resolution)
    degree_grid = np.linspace(d_min, d_max, resolution)

    Xg, Yg = np.meshgrid(nodes_grid, degree_grid)
    Zg = np.zeros_like(Xg)

    for i in range(resolution):
        for j in range(resolution):

            n = Xg[i, j]
            d = Yg[i, j]

            Zg[i, j] = predict_resilience(n, d, coeffs)

    return Xg, Yg, Zg


def run():

    print("\nNEXAH Resilience Universal Field")
    print("--------------------------------")

    data = load_results()

    if len(data) < 6:
        print("Not enough experiment data.")
        return

    X, y = build_regression_matrix(data)

    coeffs = fit_field(X, y)

    print("\nLearned Field Coefficients")
    print("---------------------------")

    names = ["a", "b(nodes)", "c(degree)", "d(log nodes)", "e(1/degree)", "f(nodes*degree)"]

    for name, val in zip(names, coeffs):
        print(f"{name:15s} = {val:.6f}")

    Xg, Yg, Zg = build_surface(data, coeffs)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection="3d")

    surface = ax.plot_surface(
        Xg,
        Yg,
        Zg,
        cmap="plasma",
        alpha=0.85
    )

    xs = [d[0] for d in data]
    ys = [d[1] for d in data]
    zs = [d[2] for d in data]

    ax.scatter(xs, ys, zs, c="black", s=40)

    ax.set_xlabel("Nodes")
    ax.set_ylabel("Degree")
    ax.set_zlabel("Predicted Resilience")

    fig.colorbar(surface, label="Resilience")

    plt.title("NEXAH Universal Resilience Field")

    plt.show()


if __name__ == "__main__":

    run()
