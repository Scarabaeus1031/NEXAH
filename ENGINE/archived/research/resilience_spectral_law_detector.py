"""
NEXAH Resilience Spectral Law Detector

Searches for empirical laws linking resilience with spectral graph properties.

Tested spectral variables:
- spectral_radius
- algebraic_connectivity
- largest_laplacian
- spectral_gap
- connectivity_ratio = algebraic_connectivity / largest_laplacian

The script attempts simple linear fits and reports the lowest error models.
"""

import os
import json
import numpy as np
import networkx as nx
import math

RESULT_DIR = "results"


def load_graphs():

    data = []

    if not os.path.exists(RESULT_DIR):
        return data

    for f in os.listdir(RESULT_DIR):

        if not f.endswith(".json"):
            continue

        try:

            path = os.path.join(RESULT_DIR, f)

            with open(path) as file:
                r = json.load(file)

            if "nodes" not in r:
                continue

            nodes = r["nodes"]
            edges = r["edges"]
            resilience = r["resilience_score"]

            if nodes < 2:
                continue

            G = nx.gnm_random_graph(nodes, edges)

            data.append((G, resilience))

        except Exception:
            continue

    return data


def spectral_metrics(G):

    UG = G.to_undirected()

    A = nx.to_numpy_array(UG)
    eigA = np.linalg.eigvals(A)

    spectral_radius = max(np.abs(eigA))

    L = nx.laplacian_matrix(UG).toarray()
    eigL = np.linalg.eigvals(L)
    eigL = np.sort(eigL)

    if len(eigL) < 2:
        return None

    algebraic_connectivity = eigL[1]
    largest_laplacian = eigL[-1]

    spectral_gap = largest_laplacian - algebraic_connectivity

    ratio = algebraic_connectivity / largest_laplacian if largest_laplacian > 0 else 0

    return {
        "spectral_radius": float(spectral_radius),
        "algebraic_connectivity": float(algebraic_connectivity),
        "largest_laplacian": float(largest_laplacian),
        "spectral_gap": float(spectral_gap),
        "connectivity_ratio": float(ratio),
    }


def collect_data():

    graphs = load_graphs()

    X = []
    y = []

    for G, resilience in graphs:

        m = spectral_metrics(G)

        if m is None:
            continue

        X.append([
            m["spectral_radius"],
            m["algebraic_connectivity"],
            m["largest_laplacian"],
            m["spectral_gap"],
            m["connectivity_ratio"],
        ])

        y.append(resilience)

    return np.array(X), np.array(y)


def fit_models(X, y):

    labels = [
        "spectral_radius",
        "algebraic_connectivity",
        "largest_laplacian",
        "spectral_gap",
        "connectivity_ratio",
    ]

    results = []

    for i in range(len(labels)):

        xi = X[:, i]

        A = np.vstack([np.ones(len(xi)), xi]).T

        coeffs, _, _, _ = np.linalg.lstsq(A, y, rcond=None)

        pred = A @ coeffs
        err = np.mean(np.abs(pred - y))

        results.append((labels[i], coeffs, err))

    results.sort(key=lambda r: r[2])

    return results


def run():

    print("\nNEXAH Resilience Spectral Law Detector")
    print("--------------------------------------")

    X, y = collect_data()

    if len(X) < 5:
        print("Not enough data.")
        return

    models = fit_models(X, y)

    print("\nCandidate Spectral Laws\n")

    for i, (label, coeffs, err) in enumerate(models[:5], 1):

        a = coeffs[0]
        b = coeffs[1]

        print(f"{i}. Resilience ≈ {a:.4f} + {b:.4f} * {label}")
        print(f"   error ≈ {err:.5f}\n")


if __name__ == "__main__":
    run()
