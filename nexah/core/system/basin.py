import numpy as np


def assign_basins_by_threshold(x, thresholds):
    """
    Assign basin IDs based on scalar thresholds.

    Parameters
    ----------
    x : array-like
        1D signal (e.g. r(t), energy, etc.)
    thresholds : list
        Sorted threshold values

    Returns
    -------
    basin_ids : np.ndarray
    """
    x = np.asarray(x)
    basin_ids = np.zeros_like(x, dtype=int)

    for i, val in enumerate(x):
        for j, t in enumerate(thresholds):
            if val < t:
                basin_ids[i] = j
                break
        else:
            basin_ids[i] = len(thresholds)

    return basin_ids


def assign_basins_kmeans(X, k=3, max_iter=100):
    """
    Simple k-means clustering for basin assignment.

    Parameters
    ----------
    X : np.ndarray (N, d)
    k : int

    Returns
    -------
    labels : np.ndarray (N,)
    centroids : np.ndarray (k, d)
    """
    X = np.asarray(X)
    N, d = X.shape

    # init random centroids
    rng = np.random.default_rng(42)
    centroids = X[rng.choice(N, k, replace=False)]

    for _ in range(max_iter):
        # assign
        distances = np.linalg.norm(X[:, None] - centroids[None, :], axis=2)
        labels = np.argmin(distances, axis=1)

        # update
        new_centroids = np.array([
            X[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i]
            for i in range(k)
        ])

        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    return labels, centroids
