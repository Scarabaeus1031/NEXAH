# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/channel_extractor.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

CHANNEL_DISTANCE = 3.0
MIN_TRANSITIONS = 5


# --------------------------------------------------
# LOOP CENTERS
# --------------------------------------------------

def compute_loop_centers(points, labels):
    """
    Compute center of each detected loop cluster
    """
    centers = []

    unique_labels = set(labels)
    for label in unique_labels:
        if label == -1:
            continue

        cluster_points = points[labels == label]
        center = cluster_points.mean(axis=0)
        centers.append(center)

    return np.array(centers)


# --------------------------------------------------
# CHANNEL DETECTION
# --------------------------------------------------

def detect_channels(trajectory, centers):
    """
    Detect transitions between loop centers
    """
    if len(centers) < 2:
        return []

    channels = []

    # assign each trajectory point to nearest center
    dist_matrix = cdist(trajectory, centers)
    assignments = np.argmin(dist_matrix, axis=1)

    # detect transitions
    transitions = []

    for i in range(1, len(assignments)):
        a = assignments[i - 1]
        b = assignments[i]

        if a != b:
            transitions.append((a, b))

    # count transitions
    transition_counts = {}
    for a, b in transitions:
        key = (a, b)
        transition_counts[key] = transition_counts.get(key, 0) + 1

    # filter strong channels
    for (a, b), count in transition_counts.items():
        if count >= MIN_TRANSITIONS:
            channels.append((a, b, count))

    return channels


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_channels(trajectory, centers, channels):
    plt.figure(figsize=(8, 8))

    # trajectory
    plt.plot(trajectory[:, 0], trajectory[:, 1], alpha=0.2)

    # loop centers
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=80)

    # channels
    for a, b, count in channels:
        p1 = centers[a]
        p2 = centers[b]

        plt.plot([p1[0], p2[0]], [p1[1], p2[1]],
                 linewidth=1 + count * 0.3)

    plt.title("Detected Channels Between Loops")
    plt.axis("equal")
    plt.show()


# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

def extract_channels(trajectory, loop_points, loop_labels):
    centers = compute_loop_centers(loop_points, loop_labels)
    channels = detect_channels(trajectory, centers)

    return centers, channels


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":
    # synthetic trajectory with two loops
    t = np.linspace(0, 40, 3000)

    x = np.cos(t) + 0.5 * np.cos(3 * t)
    y = np.sin(t) + 0.5 * np.sin(2 * t)

    trajectory = np.stack([x, y], axis=1)

    # fake loop points (simulate output from loop_detector)
    from sklearn.cluster import DBSCAN
    clustering = DBSCAN(eps=0.5, min_samples=10).fit(trajectory)
    labels = clustering.labels_

    centers = compute_loop_centers(trajectory, labels)
    channels = detect_channels(trajectory, centers)

    if len(centers) > 0:
        plot_channels(trajectory, centers, channels)
