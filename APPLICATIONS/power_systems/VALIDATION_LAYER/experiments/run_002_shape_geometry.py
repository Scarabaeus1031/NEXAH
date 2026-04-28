# ============================================================
# 🧪 NEXAH — Experiment 002
# Shape Geometry Analysis (Crossings + Convergence)
# ============================================================

import sys
import os

# add repo root to path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.append(ROOT)
import numpy as np
import matplotlib.pyplot as plt

# reuse from your system
from APPLICATIONS.power_systems.VALIDATION_LAYER.experiments.run_001_shape_validation import (
    make_synthetic_scenario,
    run_validation,
    resample_shapes
)


# ============================================================
# HELPERS
# ============================================================

def compute_mean_shapes_per_cluster(X, cluster_ids):
    mean_shapes = {}

    for cid in np.unique(cluster_ids):
        cluster_shapes = X[cluster_ids == cid]
        mean_shapes[cid] = np.mean(cluster_shapes, axis=0)

    return mean_shapes


def compute_crossings(shape_a, shape_b):
    """
    Count zero crossings between two curves
    """
    diff = shape_a - shape_b
    signs = np.sign(diff)

    crossings = np.where(np.diff(signs) != 0)[0]
    return len(crossings), crossings


def compute_area_between(shape_a, shape_b):
    return float(np.mean(np.abs(shape_a - shape_b)))


def compute_end_gap(shape_a, shape_b):
    return float(abs(shape_a[-1] - shape_b[-1]))


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():

    scenarios = ["smooth", "nonlinear", "noisy"]

    all_shapes = {}
    all_resampled = []
    labels = []

    # --------------------------------------------------------
    # 1. Generate shapes
    # --------------------------------------------------------

    for s in scenarios:
        data = make_synthetic_scenario(s)
        res, shapes = run_validation(data, s)

        if len(shapes) == 0:
            continue

        resampled = resample_shapes(shapes, n=50)

        for r in resampled:
            all_resampled.append(r)
            labels.append(s)

    X = np.array(all_resampled)

    if len(X) < 3:
        print("Not enough shapes")
        return

    # --------------------------------------------------------
    # 2. Cluster
    # --------------------------------------------------------

    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=3, random_state=0)
    cluster_ids = kmeans.fit_predict(X)

    # --------------------------------------------------------
    # 3. Mean shapes
    # --------------------------------------------------------

    mean_shapes = compute_mean_shapes_per_cluster(X, cluster_ids)

    t = np.linspace(0, 1, X.shape[1])

    plt.figure(figsize=(8, 5))

    for cid, shape in mean_shapes.items():
        plt.plot(t, shape, label=f"Cluster {cid}", linewidth=2)

    plt.title("Mean Shape per Cluster")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # 4. Pairwise geometry analysis
    # --------------------------------------------------------

    print("\n=== SHAPE GEOMETRY ANALYSIS ===\n")

    cluster_keys = list(mean_shapes.keys())

    for i in range(len(cluster_keys)):
        for j in range(i + 1, len(cluster_keys)):

            c1 = cluster_keys[i]
            c2 = cluster_keys[j]

            s1 = mean_shapes[c1]
            s2 = mean_shapes[c2]

            crossings, idx = compute_crossings(s1, s2)
            area = compute_area_between(s1, s2)
            end_gap = compute_end_gap(s1, s2)

            print(f"Cluster {c1} vs {c2}")
            print(f"  crossings : {crossings}")
            print(f"  area      : {area:.4f}")
            print(f"  end gap   : {end_gap:.4f}")
            print()

    # --------------------------------------------------------
    # 5. Highlight crossings visually
    # --------------------------------------------------------

    plt.figure(figsize=(8, 5))

    for cid, shape in mean_shapes.items():
        plt.plot(t, shape, label=f"Cluster {cid}", linewidth=2)

    # mark crossings
    for i in range(len(cluster_keys)):
        for j in range(i + 1, len(cluster_keys)):

            s1 = mean_shapes[cluster_keys[i]]
            s2 = mean_shapes[cluster_keys[j]]

            _, idx = compute_crossings(s1, s2)

            for k in idx:
                plt.axvline(t[k], color="red", alpha=0.2)

    plt.title("Mean Shapes + Crossing Zones")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    run_experiment()
