"""
NEXAH Architecture Stability Landscape
======================================

Kernel utilities for constructing architecture stability landscapes.

The landscape is defined over two parameters:

    n = number of nodes
    p = edge probability (network density)

For each (n, p) pair, random graphs are sampled and the spectral
stability score

    S(G) = λ₂ / λ_max

is computed.

The result is a stability field describing how architecture stability
changes across structural parameter space.

This module provides the core data generator used by architecture
exploration demos and stability analysis tools.
"""

import numpy as np
import networkx as nx

from .spectral_stability import spectral_stability_score


def sample_architecture_stability(n, p, samples=20):
    """
    Estimate stability for a given architecture configuration.

    Parameters
    ----------
    n : int
        Number of nodes.
    p : float
        Edge probability.
    samples : int
        Number of random graphs sampled.

    Returns
    -------
    float
        Mean spectral stability score.
    """

    scores = []

    for _ in range(samples):

        G = nx.erdos_renyi_graph(n, p)

        score = spectral_stability_score(G)

        scores.append(score)

    return float(np.mean(scores))


def build_architecture_landscape(
    node_range=(4, 12),
    p_range=(0.05, 0.95),
    p_steps=20,
    samples=20
):
    """
    Build a stability landscape across architecture parameter space.

    Parameters
    ----------
    node_range : tuple
        Range of node counts (min, max).
    p_range : tuple
        Range of edge probabilities.
    p_steps : int
        Resolution of the probability axis.
    samples : int
        Number of graphs sampled per grid point.

    Returns
    -------
    dict
        Landscape data structure containing:

        - node_values
        - p_values
        - stability_field
    """

    node_values = list(range(node_range[0], node_range[1] + 1))

    p_values = np.linspace(p_range[0], p_range[1], p_steps)

    stability_field = np.zeros((len(node_values), len(p_values)))

    for i, n in enumerate(node_values):

        for j, p in enumerate(p_values):

            stability = sample_architecture_stability(
                n,
                p,
                samples=samples
            )

            stability_field[i, j] = stability

    return {
        "node_values": node_values,
        "p_values": p_values,
        "stability_field": stability_field
    }
