# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/loop_detector.py

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

DIST_THRESHOLD = 1.5       # spatial closeness
MIN_TIME_SEPARATION = 20   # avoid trivial neighbors
CLUSTER_EPS = 2.0
CLUSTER_MIN_SAMPLES = 5

MAX_SAMPLES = 1500         # safety limit (prevents O(N^2) explosion)


# --------------------------------------------------
# LOOP DETECTION CORE
# --------------------------------------------------

def detect_recurrences(trajectory):
    """
    Faster recurrence detection using local window
    """
    N = len(trajectory)
    recurrences = []

    WINDOW = 120  # limit search range

    for i in range(N):
        j_start = i + MIN_TIME_SEPARATION
        j_end = min(i + WINDOW, N)

        for j in range(j_start, j_end):
            dist = np.linalg.norm(trajectory[i] - trajectory[j])

            if dist < DIST_THRESHOLD:
                recurrences.append((i, j))

    return recurrences

def recurrence_points(trajectory, recurrences):
    """
    Convert recurrence pairs into point cloud
    """
    points = []

    for i, j in recurrences:
        midpoint = (trajectory[i] + trajectory[j]) / 2.0
        points.append(midpoint)

    if len(points) == 0:
        return None

    return np.array(points)


# --------------------------------------------------
# CLUSTERING → LOOP STRUCTURES
# --------------------------------------------------

def cluster_loops(points):
    """
    Cluster recurrence points into loop structures
    """
    if points is None or len(points) == 0:
        return None, None

    clustering = DBSCAN(eps=CLUSTER_EPS, min_samples=CLUSTER_MIN_SAMPLES)
    labels = clustering.fit_predict(points)

    return labels, clustering


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_loops(trajectory, points, labels):
    """
    Visualize loops over trajectory
    """
    plt.figure(figsize=(8, 8))

    # trajectory
    plt.plot(trajectory[:, 0], trajectory[:, 1], alpha=0.3)

    if points is not None and labels is not None:
        unique_labels = set(labels)

        for label in unique_labels:
            if label == -1:
                continue  # noise

            cluster_points = points[labels == label]
            plt.scatter(cluster_points[:, 0], cluster_points[:, 1], s=40)

    plt.title("Detected Loop Structures")
    plt.axis("equal")
    plt.show()


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def detect_loops(trajectory):
    """
    Full loop detection pipeline
    """

    # safety downsampling
    if len(trajectory) > MAX_SAMPLES:
        trajectory = trajectory[:MAX_SAMPLES]

    recurrences = detect_recurrences(trajectory)
    points = recurrence_points(trajectory, recurrences)

    if points is None:
        return None, None, None

    labels, clustering = cluster_loops(points)

    return recurrences, points, labels


# --------------------------------------------------
# TEST RUN (standalone)
# --------------------------------------------------

if __name__ == "__main__":
    # synthetic test trajectory (spiral + loop)
    t = np.linspace(0, 20, 2000)
    x = np.cos(t) * (1 + 0.1 * t)
    y = np.sin(t) * (1 + 0.1 * t)

    trajectory = np.stack([x, y], axis=1)

    recurrences, points, labels = detect_loops(trajectory)

    if points is not None:
        plot_loops(trajectory, points, labels)
