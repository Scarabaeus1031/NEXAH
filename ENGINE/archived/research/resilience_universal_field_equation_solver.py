"""
NEXAH Resilience Universal Field Equation Solver

Attempts to discover an analytic field equation for resilience
based on observed architecture parameters.

Tested variables:

x1 = lambda2 / lambda_max
x2 = clustering
x3 = nodes

Model form:

R ≈ a
   + b*x1
   + c*x2
   + d*x3
   + e*(x1*x2)
   + f*(x1^2)

This tries to approximate the resilience field discovered
in the NEXAH architecture simulations.
"""

import os
import json
import numpy as np
import networkx as nx


RESULT_DIR = "results"


def load_graphs():

    graphs = []

    if not os.path.exists(RESULT_DIR):
        return graphs

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        try:

            path = os.path.join(RESULT_DIR, f)

            with open(path) as file:
                r = json.load(file)

            nodes = r["nodes"]
            edges = r["edges"]
            resilience = r["resilience_score"]

            if nodes < 2:
                continue

            G = nx.gnm_random_graph(nodes, edges)

            graphs.append((G, resilience))

        except Exception:
            continue

    return graphs


def spectral_ratio(G):

    UG = G.to_undirected()

    L = nx.laplacian_matrix(UG).toarray()

    eigvals = np.linalg.eigvals(L)
    eigvals = np.real(eigvals)
    eigvals.sort()

    if len(eigvals) < 2:
        return None

    lambda2 = eigvals[1]
    lambdamax = eigvals[-1]

    if lambdamax == 0:
        return None

    return lambda2 / lambdamax


def collect_dataset():

    graphs = load_graphs()

    X = []
    y = []

    for G, resilience in graphs:

        ratio = spectral_ratio(G)

        if ratio is None:
            continue

        clustering = nx.average_clustering(G)

        nodes = G.number_of_nodes()

        X.append([
            1,
            ratio,
            clustering,
            nodes,
            ratio * clustering,
            ratio ** 2
        ])

        y.append(resilience)

    return np.array(X), np.array(y)


def solve_field_equation():

    print("\nNEXAH Universal Field Equation Solver")
    print("------------------------------------")

    X, y = collect_dataset()

    if len(X) < 5:
        print("Not enough data.")
        return

    coeffs, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

    labels = [
        "a",
        "b*(λ2/λmax)",
        "c*(clustering)",
        "d*(nodes)",
        "e*(ratio*clustering)",
        "f*(ratio^2)"
    ]

    print("\nDerived Field Equation\n")

    for label, c in zip(labels, coeffs):

        print(f"{label:20s} = {c:.6f}")

    print("\nApproximate equation\n")

    print(
        "R ≈ "
        f"{coeffs[0]:.3f} "
        f"+ {coeffs[1]:.3f}*(λ2/λmax) "
        f"+ {coeffs[2]:.3f}*clustering "
        f"+ {coeffs[3]:.3f}*nodes "
        f"+ {coeffs[4]:.3f}*(ratio*clustering) "
        f"+ {coeffs[5]:.3f}*(ratio^2)"
    )


def run():

    solve_field_equation()


if __name__ == "__main__":

    run()
