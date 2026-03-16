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
- gradient-ascent architecture search

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


def gradient_ascent_architecture_search(
    node_values,
    p_values,
    stability_field,
    start=None,
    max_steps=50
):
    """
    Perform gradient ascent in the architecture stability landscape.

    Starting from an initial architecture configuration,
    the algorithm moves toward neighboring configurations
    with higher stability.

    Parameters
    ----------
    node_values : list
        Node counts corresponding to stability_field rows.
    p_values : list
        Edge probabilities corresponding to stability_field columns.
    stability_field : ndarray
        Stability landscape.
    start : tuple or None
        Starting index (i, j). If None, a random start is used.
    max_steps : int
        Maximum number of ascent steps.

    Returns
    -------
    dict
        Search result containing

        - path
        - final_position
        - final_nodes
        - final_p
        - final_stability
    """

    rows, cols = stability_field.shape

    if start is None:
        i = np.random.randint(0, rows)
        j = np.random.randint(0, cols)
    else:
        i, j = start

    path = [(i, j)]

    for _ in range(max_steps):

        current = stability_field[i, j]

        neighbors = []

        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:

            ni = i + di
            nj = j + dj

            if 0 <= ni < rows and 0 <= nj < cols:
                neighbors.append((ni, nj))

        best_neighbor = None
        best_value = current

        for ni, nj in neighbors:

            value = stability_field[ni, nj]

            if value > best_value:
                best_value = value
                best_neighbor = (ni, nj)

        if best_neighbor is None:
            break

        i, j = best_neighbor
        path.append((i, j))

    return {
        "path": path,
        "final_position": (i, j),
        "final_nodes": node_values[i],
        "final_p": p_values[j],
        "final_stability": stability_field[i, j],
    }
