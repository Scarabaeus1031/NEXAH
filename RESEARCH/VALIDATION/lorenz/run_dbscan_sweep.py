"""
NEXAH — DBSCAN Parameter Sweep

Goal:
Analyze how partition resolution (eps) affects:
- number of clusters
- transition structure

This reveals:
→ when structure emerges
→ when it collapses
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


# ============================================================
# CONFIG
# ============================================================

OUTPUT_DIR = "RESEARCH/validation/lorenz/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

N_STEPS = 5000
DT = 0.01

EPS_VALUES = np.linspace(0.1, 0.6, 10)
MIN_SAMPLES = 20


# ============================================================
# LORENZ
# ============================================================

def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


def simulate():
    x, y, z = 1.0, 1.0, 1.0
    traj = []

    for _ in range(N_STEPS):
        dx, dy, dz = lorenz_step(x, y, z)
        x += dx * DT
        y += dy * DT
        z += dz * DT
        traj.append([x, y, z])

    return np.array(traj)


# ============================================================
# TRANSITION MATRIX
# ============================================================

def compute_transition_matrix(labels):
    valid = labels >= 0
    unique = np.unique(labels[valid])

    if len(unique) <= 1:
        return None, len(unique)

    mapping = {old: i for i, old in enumerate(unique)}
    mapped = np.array([mapping[l] if l >= 0 else -1 for l in labels])

    n = len(unique)
    T = np.zeros((n, n))

    for i in range(len(mapped) - 1):
        a, b = mapped[i], mapped[i + 1]
        if a >= 0 and b >= 0:
            T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1

    return T / row_sums, n


# ============================================================
# MAIN
# ============================================================

def main():
    print("Running DBSCAN sweep...")

    traj = simulate()
    X = StandardScaler().fit_transform(traj)

    cluster_counts = []
    valid_counts = []

    fig, axs = plt.subplots(2, 5, figsize=(14, 6))
    axs = axs.flatten()

    summary_lines = []

    for i, eps in enumerate(EPS_VALUES):
        db = DBSCAN(eps=eps, min_samples=MIN_SAMPLES)
        labels = db.fit_predict(X)

        valid = labels >= 0
        unique = np.unique(labels[valid])

        n_clusters = len(unique)
        cluster_counts.append(n_clusters)
        valid_counts.append(np.sum(valid) / len(labels))

        T, n_states = compute_transition_matrix(labels)

        ax = axs[i]
        ax.scatter(traj[:, 0], traj[:, 1], c=labels, s=2, cmap="viridis")
        ax.set_title(f"eps={eps:.2f}, k={n_clusters}")
        ax.set_xticks([])
        ax.set_yticks([])

        summary_lines.append(
            f"eps={eps:.3f}, clusters={n_clusters}, valid_ratio={valid_counts[-1]:.3f}"
        )

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "dbscan_partition_sweep.png")
    plt.savefig(path, dpi=200)
    plt.close()

    print(f"✅ Saved: {path}")

    # Plot cluster count vs eps
    plt.figure(figsize=(6, 4))
    plt.plot(EPS_VALUES, cluster_counts, marker="o")
    plt.xlabel("eps")
    plt.ylabel("number of clusters")
    plt.title("DBSCAN cluster count vs eps")

    path2 = os.path.join(OUTPUT_DIR, "dbscan_cluster_count.png")
    plt.savefig(path2, dpi=200)
    plt.close()

    print(f"✅ Saved: {path2}")

    # Save summary
    summary_path = os.path.join(
        OUTPUT_DIR,
        "dbscan_sweep_summary.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH — DBSCAN Sweep\n\n")
        for line in summary_lines:
            f.write(line + "\n")

        f.write("\nInterpretation:\n")
        f.write(
            "Low eps → many clusters (over-segmentation)\n"
            "High eps → 1 cluster (collapse)\n"
            "Intermediate eps → meaningful structure\n"
        )

    print(f"✅ Saved: {summary_path}")
    print("Done.")


if __name__ == "__main__":
    main()
