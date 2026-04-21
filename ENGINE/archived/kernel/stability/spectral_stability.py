"""
NEXAH Spectral Stability
========================

Core spectral stability operators used by the NEXAH kernel.

The primary stability measure is the normalized spectral connectivity:

    S(G) = λ₂ / λ_max

Where

    λ₂     = algebraic connectivity (second-smallest Laplacian eigenvalue)
    λ_max  = largest Laplacian eigenvalue

This ratio measures how strongly connected a system is relative to its
maximum structural coupling.

High values indicate architectures that are globally cohesive and
structurally resilient.

These operators are used to build architecture stability landscapes
and navigation graphs within the NEXAH framework.
"""

import numpy as np
import networkx as nx


def spectral_stability_score(G):
    """
    Compute the normalized spectral stability score.

    Parameters
    ----------
    G : networkx.Graph
        Graph representing the system architecture.

    Returns
    -------
    float
        Stability score in the range [0, 1].
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

    return float(lambda_2 / lambda_max)


def resilience_estimate(G):
    """
    Empirical resilience estimate derived from experiments.

    The relationship observed in architecture exploration experiments:

        resilience ≈ 0.355 + 0.401 * (λ₂ / λ_max)

    Parameters
    ----------
    G : networkx.Graph

    Returns
    -------
    float
        Estimated resilience score.
    """

    ratio = spectral_stability_score(G)

    return 0.355 + 0.401 * ratio


def graph_metrics(G):
    """
    Compute structural metrics for an architecture graph.

    Returns
    -------
    dict
        Dictionary containing graph metrics and stability scores.
    """

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    degree = np.mean([d for _, d in G.degree()])
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
