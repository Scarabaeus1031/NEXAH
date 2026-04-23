"""
NEXAH Resilience Universal Equation Solver

Fits simple empirical equations for resilience based on
architecture variables.

Goal:
discover equations of the form

Resilience ≈ a + b*x + c*y

where x,y can be:
- nodes
- edges
- degree
- 1/degree
- log(nodes)
- log(edges)
"""

import os
import json
import math
import itertools

import numpy as np


RESULT_DIR = "results"


def load_results():

    results = []

    if not os.path.exists(RESULT_DIR):
        return results

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        path = os.path.join(RESULT_DIR, f)

        try:
            with open(path, "r") as file:

                data = json.load(file)

                graph = data.get("graph", {})
                res = data.get("resilience", {})

                if "nodes" in graph:
                    nodes = len(graph["nodes"])
                else:
                    nodes = graph.get("num_nodes", 0)

                if "edges" in graph:
                    edges = len(graph["edges"])
                else:
                    edges = graph.get("num_edges", 0)

                resilience = res.get("resilience_score", None)

                if nodes <= 0 or edges <= 0 or resilience is None:
                    continue

                degree = edges / nodes

                results.append({
                    "nodes": nodes,
                    "edges": edges,
                    "degree": degree,
                    "inv_degree": 1.0 / degree if degree != 0 else 0.0,
                    "log_nodes": math.log(nodes),
                    "log_edges": math.log(edges),
                    "resilience": resilience,
                })

        except Exception:
            continue

    return results


def build_feature_matrix(results):

    feature_names = [
        "nodes",
        "edges",
        "degree",
        "inv_degree",
        "log_nodes",
        "log_edges",
    ]

    y = np.array([r["resilience"] for r in results], dtype=float)

    feature_data = {
        name: np.array([r[name] for r in results], dtype=float)
        for name in feature_names
    }

    return feature_names, feature_data, y


def fit_linear_model(feature_arrays, y):

    """
    Fits y ≈ a + b*x + c*y2 + ...
    using least squares.
    """

    X_cols = [np.ones(len(y))]
    X_cols.extend(feature_arrays)

    X = np.column_stack(X_cols)

    coeffs, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)

    y_pred = X @ coeffs

    mse = float(np.mean((y - y_pred) ** 2))

    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    ss_res = float(np.sum((y - y_pred) ** 2))

    if ss_tot == 0:
        r2 = 0.0
    else:
        r2 = 1.0 - (ss_res / ss_tot)

    return coeffs, mse, r2, y_pred


def equation_string(feature_combo, coeffs):

    parts = [f"{coeffs[0]:.4f}"]

    for i, feat in enumerate(feature_combo, start=1):
        coef = coeffs[i]
        sign = "+" if coef >= 0 else "-"
        parts.append(f" {sign} {abs(coef):.4f}*{feat}")

    return "Resilience ≈ " + "".join(parts)


def search_best_equations(feature_names, feature_data, y):

    candidates = []

    # try 1-feature and 2-feature equations
    for k in [1, 2]:
        for combo in itertools.combinations(feature_names, k):

            arrays = [feature_data[name] for name in combo]

            coeffs, mse, r2, _ = fit_linear_model(arrays, y)

            candidates.append({
                "features": combo,
                "coeffs": coeffs,
                "mse": mse,
                "r2": r2,
                "equation": equation_string(combo, coeffs),
            })

    candidates.sort(key=lambda c: (c["mse"], -c["r2"]))

    return candidates


def print_report(candidates):

    print("\nNEXAH Universal Equation Solver")
    print("--------------------------------")

    if not candidates:
        print("No candidate equations found.")
        return

    print("\nTop candidate equations\n")

    for i, c in enumerate(candidates[:5], start=1):
        print(f"{i}. {c['equation']}")
        print(f"   MSE = {c['mse']:.6f} | R² = {c['r2']:.4f}")

    best = candidates[0]

    print("\nBest discovered equation\n")
    print(best["equation"])
    print(f"MSE = {best['mse']:.6f}")
    print(f"R² = {best['r2']:.4f}")


def run_solver():

    results = load_results()

    if not results:
        print("No experiment results found.")
        return

    feature_names, feature_data, y = build_feature_matrix(results)

    candidates = search_best_equations(feature_names, feature_data, y)

    print_report(candidates)

    return candidates


if __name__ == "__main__":

    run_solver()
