import numpy as np


def compute_transition_matrix(basin_ids):
    """
    Compute transition probabilities between discrete basins.

    Parameters
    ----------
    basin_ids : array-like of shape (T,)
        Sequence of basin labels over time.

    Returns
    -------
    P : ndarray of shape (n_basins, n_basins)
        Transition probability matrix where:
        P[i, j] = probability of transitioning from basin i to j.

    basins : ndarray
        Sorted unique basin labels corresponding to indices in P.
    """

    basin_ids = np.asarray(basin_ids)

    if basin_ids.ndim != 1:
        raise ValueError("basin_ids must be a 1D array")

    # Identify unique basins
    basins = np.unique(basin_ids)
    n = len(basins)

    # Map basin labels → indices
    basin_to_idx = {b: i for i, b in enumerate(basins)}

    # Count transitions
    counts = np.zeros((n, n), dtype=float)

    for t in range(len(basin_ids) - 1):
        i = basin_to_idx[basin_ids[t]]
        j = basin_to_idx[basin_ids[t + 1]]
        counts[i, j] += 1.0

    # Normalize to probabilities
    P = np.zeros_like(counts)

    for i in range(n):
        row_sum = counts[i].sum()
        if row_sum > 0:
            P[i] = counts[i] / row_sum
        else:
            # No outgoing transitions observed
            P[i] = 0.0

    return P, basins


def compute_transition_counts(basin_ids):
    """
    Return raw transition counts (before normalization).
    Useful for diagnostics and validation.
    """
    basin_ids = np.asarray(basin_ids)

    basins = np.unique(basin_ids)
    n = len(basins)
    basin_to_idx = {b: i for i, b in enumerate(basins)}

    counts = np.zeros((n, n), dtype=int)

    for t in range(len(basin_ids) - 1):
        i = basin_to_idx[basin_ids[t]]
        j = basin_to_idx[basin_ids[t + 1]]
        counts[i, j] += 1

    return counts, basins


def compute_stationary_distribution(P, tol=1e-8, max_iter=10000):
    """
    Estimate stationary distribution of the transition matrix.

    Uses power iteration.

    Parameters
    ----------
    P : ndarray (n, n)
        Transition probability matrix

    Returns
    -------
    pi : ndarray (n,)
        Stationary distribution (if converged)
    """
    n = P.shape[0]

    pi = np.ones(n) / n

    for _ in range(max_iter):
        pi_next = pi @ P

        if np.linalg.norm(pi_next - pi) < tol:
            return pi_next

        pi = pi_next

    return pi  # return best estimate even if not fully converged
