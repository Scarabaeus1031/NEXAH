"""
NEXAH Architecture Navigation
=============================

Navigation utilities for exploring architecture stability landscapes.

Given a stability field defined over architecture parameters

    n = node count
    p = edge probability

this module provides methods for

- finding local stability maxima
- constructing navigation graphs
- exploring transitions between architecture regimes

These tools allow the NEXAH kernel to treat architecture search
as navigation within a stability landscape.
"""

import numpy as np


def find_local_maxima(stability_field):
    """
    Detect local maxima in a stability field.

    Parameters
    ----------
    stability_field : ndarray

    Returns
    -------
    list
        List of (i, j) indices of local maxima.
    """

    maxima = []

    rows, cols = stability_field.shape

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):

            value = stability_field[i, j]

            neighbors = [
                stability_field[i - 1, j],
                stability_field[i + 1, j],
                stability_field[i, j - 1],
                stability_field[i, j + 1],
            ]

            if value > max(neighbors):
                maxima.append((i, j))

    return maxima


def stability_gradient(stability_field):
    """
    Compute gradient directions across the stability field.

    Returns
    -------
    tuple
        (dx, dy) gradient fields.
    """

    gy, gx = np.gradient(stability_field)

    return gx, gy


def build_navigation_graph(stability_field, threshold=0.05):
    """
    Build a navigation graph between stable regions.

    Nodes correspond to stability maxima.
    Edges connect maxima with similar stability levels.

    Parameters
    ----------
    stability_field : ndarray
    threshold : float

    Returns
    -------
    dict
        Navigation graph structure.
    """

    maxima = find_local_maxima(stability_field)

    graph = {m: [] for m in maxima}

    for i, a in enumerate(maxima):
        for b in maxima[i + 1:]:

            va = stability_field[a]
            vb = stability_field[b]

            if abs(va - vb) < threshold:

                graph[a].append(b)
                graph[b].append(a)

    return graph


def best_architecture(stability_field):
    """
    Locate the globally most stable architecture.

    Returns
    -------
    tuple
        (i, j) index of maximum stability.
    """

    idx = np.argmax(stability_field)

    return np.unravel_index(idx, stability_field.shape)
