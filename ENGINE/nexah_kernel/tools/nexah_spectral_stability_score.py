"""
NEXAH Spectral Stability Score
==============================

Computes the spectral stability metric

    λ₂ / λmax

for a given network architecture.

λ₂     = algebraic connectivity (2nd smallest Laplacian eigenvalue)
λmax   = largest Laplacian eigenvalue

This ratio empirically correlates with system resilience.

Typical interpretation

    higher score → more structurally stable system

Example usage:

    python -m ENGINE.nexah_kernel.tools.nexah_spectral_stability_score

or import inside experiments:

    from ENGINE.nexah_kernel.tools.nexah_spectral_stability_score import spectral_stability_score
"""

import numpy as np
import networkx as nx


def spectral_stability_score(G):
    """
    Compute λ₂ / λmax for graph G.
    """

    if len(G.nodes) < 2:
        return 0.0

    L = nx.laplacian_matrix(G).toarray()

    eigenvalues = np.linalg.eigvals(L)
    eigenvalues = np.sort(np.real(eigenvalues))

    lambda_2 = eigenvalues[1]
    lambda_max = eigenvalues[-1]

    if lambda_max == 0:
        return 0.0

    return lambda_2 / lambda_max


def resilience_estimate(G):
    """
    Empirical resilience estimate from experiments.
    """

    ratio = spectral_stability_score(G)

    resilience = 0.355 + 0.401 * ratio

    return resilience


def graph_metrics(G):
    """
    Compute basic architecture metrics.
    """

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    degree = np.mean([d for n, d in G.degree()])
    clustering = nx.average_clustering(G)

    ratio = spectral_stability_score(G)
    resilience = resilience_estimate(G)

    return {
        "nodes": nodes,
        "edges": edges,
        "avg_degree": degree,
        "clustering": clustering,
        "lambda_ratio": ratio,
        "resilience_estimate": resilience,
    }


def demo_graph():
    """
    Generate a random demo architecture.
    """

    G = nx.gnm_random_graph(5, 8)

    metrics = graph_metrics(G)

    print("\nNEXAH Spectral Stability Analysis\n")

    for k, v in metrics.items():
        print(f"{k:20} {v}")


if __name__ == "__main__":
    demo_graph()
