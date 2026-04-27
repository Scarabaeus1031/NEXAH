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
    """
