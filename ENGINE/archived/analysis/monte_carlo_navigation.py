"""
NEXAH Monte Carlo Navigation Analysis

This module provides statistical analysis over multiple agent runs.

Core idea:
→ Not a single trajectory matters
→ The distribution of trajectories reveals system structure

Outputs:
- visit density
- endpoint distribution
- transition matrix (optional)
"""

import numpy as np


# --------------------------------------------------
# MONTE CARLO RUNNER
# --------------------------------------------------

def run_monte_carlo(landscape, agent_fn, n_runs=100, **agent_kwargs):
    """
    Run multiple agent simulations.

    Parameters:
        landscape: np.ndarray
        agent_fn: function that returns a path [(x,y), ...]
        n_runs: number of simulations
        agent_kwargs: additional args for agent_fn

    Returns:
        list of paths
    """
    paths = []

    for _ in range(n_runs):
        path = agent_fn(landscape, **agent_kwargs)
        paths.append(path)

    return paths


# --------------------------------------------------
# VISIT DENSITY
# --------------------------------------------------

def compute_visit_density(paths, size, normalize=True):
    """
    Count how often each cell is visited.

    Returns:
        density map (2D array)
    """
    density = np.zeros((size, size))

    for path in paths:
        for x, y in path:
            density[x, y] += 1

    if normalize:
        total = np.sum(density)
        if total > 0:
            density /= total

    return density


# --------------------------------------------------
# ENDPOINT DISTRIBUTION
# --------------------------------------------------

def compute_endpoint_density(paths, size, normalize=True):
    """
    Count where agents end.

    Returns:
        endpoint density map
    """
    density = np.zeros((size, size))

    for path in paths:
        x, y = path[-1]
        density[x, y] += 1

    if normalize:
        total = np.sum(density)
        if total > 0:
            density /= total

    return density


# --------------------------------------------------
# TRANSITION MATRIX
# --------------------------------------------------

def compute_transition_matrix(paths, size):
    """
    Compute transition probabilities between grid cells.

    Returns:
        transition matrix of shape (N, N)
        where N = size*size
    """
    N = size * size
    T = np.zeros((N, N))

    def idx(x, y):
        return x * size + y

    for path in paths:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            T[idx(x1, y1), idx(x2, y2)] += 1

    # normalize rows → probabilities
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1

    P = T / row_sums
    return P


# --------------------------------------------------
# BASIN MAP
# --------------------------------------------------

def compute_basin_map(paths, size):
    """
    Assign each visited cell to its most frequent endpoint.

    Returns:
        basin_map: same size as landscape
    """
    basin_map = np.zeros((size, size, 2))  # store endpoint coords

    visit_dict = {}

    for path in paths:
        endpoint = path[-1]

        for pos in path:
            if pos not in visit_dict:
                visit_dict[pos] = {}
            visit_dict[pos][endpoint] = visit_dict[pos].get(endpoint, 0) + 1

    for (x, y), endpoint_counts in visit_dict.items():
        best_endpoint = max(endpoint_counts, key=endpoint_counts.get)
        basin_map[x, y] = best_endpoint

    return basin_map


# --------------------------------------------------
# UTIL: EXTRACT ENDPOINT LIST
# --------------------------------------------------

def extract_endpoints(paths):
    return [path[-1] for path in paths]


# --------------------------------------------------
# SIMPLE VISUALIZATION (OPTIONAL)
# --------------------------------------------------

def plot_density(density, title="Density Map", cmap="hot"):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 6))
    plt.imshow(density, cmap=cmap, origin="lower")
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
