import numpy as np
from sklearn.cluster import KMeans


def cluster_overlay(distance, residual, k=3):

    # Combine features
    X = np.column_stack([distance, residual])

    # =========================================
    # FILTER INVALID VALUES (NaN / inf)
    # =========================================
    valid = np.isfinite(X).all(axis=1)

    if np.sum(valid) < k:
        raise ValueError("Not enough valid points for clustering")

    X_valid = X[valid]

    # =========================================
    # RUN KMEANS ONLY ON CLEAN DATA
    # =========================================
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X_valid)

    # =========================================
    # REBUILD LABELS (FULL LENGTH)
    # =========================================
    labels = np.full(len(X), -1)  # -1 = invalid points
    labels[valid] = kmeans.labels_

    return labels, kmeans.cluster_centers_
