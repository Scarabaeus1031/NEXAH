# ============================================================
# 🧪 NEXAH — Experiment 003
# Shape Space Dynamics (Trajectories)
# ============================================================

import sys
import os

# fix import path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.append(ROOT)

import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.VALIDATION_LAYER.experiments.run_001_shape_validation import (
    make_synthetic_scenario,
    run_validation,
    resample_shapes
)


# ============================================================
# SHAPE SPACE (PCA)
# ============================================================

def compute_shape_space(all_shapes, n=50):

    X = []
    meta = []  # (scenario, event_index)

    for scenario, shapes in all_shapes.items():

        if len(shapes) == 0:
            continue

        resampled = resample_shapes(shapes, n=n)

        for i, r in enumerate(resampled):
            X.append(r)
            meta.append((scenario, i))

    X = np.array(X)

    if len(X) < 2:
        return None, None, None

    X_centered = X - np.mean(X, axis=0)

    _, _, Vt = np.linalg.svd(X_centered, full_matrices=False)

    coords = X_centered @ Vt[:2].T

    return coords, meta, X


# ============================================================
# TRAJECTORY PLOT
# ============================================================

def plot_shape_trajectories(coords, meta):

    plt.figure(figsize=(7, 6))

    # group by scenario
    scenarios = {}

    for (x, y), (scenario, idx) in zip(coords, meta):
        if scenario not in scenarios:
            scenarios[scenario] = []
        scenarios[scenario].append((idx, x, y))

    colors = {
        "smooth": "orange",
        "nonlinear": "green",
        "noisy": "blue"
    }

    for scenario, points in scenarios.items():

        # sort by time (event order)
        points = sorted(points, key=lambda x: x[0])

        xs = [p[1] for p in points]
        ys = [p[2] for p in points]

        plt.plot(xs, ys, marker="o", color=colors.get(scenario, "black"), label=scenario)

        # arrows
        for i in range(len(xs) - 1):
            dx = xs[i+1] - xs[i]
            dy = ys[i+1] - ys[i]

            plt.arrow(xs[i], ys[i], dx, dy,
                      head_width=0.02, length_includes_head=True,
                      color=colors.get(scenario, "black"), alpha=0.6)

        # annotate order
        for i, (x, y) in enumerate(zip(xs, ys)):
            plt.text(x, y, str(i), fontsize=8)

    plt.title("Shape Space Trajectories")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================

def run_experiment():

    scenarios = ["smooth", "nonlinear", "noisy"]

    all_shapes = {}

    # --------------------------------------------------------
    # 1. Extract shapes
    # --------------------------------------------------------

    for s in scenarios:
        data = make_synthetic_scenario(s)
        res, shapes = run_validation(data, s)

        print(res)

        all_shapes[s] = shapes

    # --------------------------------------------------------
    # 2. Build shape space
    # --------------------------------------------------------

    coords, meta, X = compute_shape_space(all_shapes)

    if coords is None:
        print("Not enough data")
        return

    # --------------------------------------------------------
    # 3. Plot trajectories
    # --------------------------------------------------------

    plot_shape_trajectories(coords, meta)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    run_experiment()
