"""
NEXAH — Multi-Partition Invariance Test

Goal:
Test whether transition structure is stable across different partitions:

1. KMeans on full state space
2. PCA + KMeans
3. Random projection + KMeans
4. DBSCAN density-based partition

If different partitions show similar transition patterns,
this supports the hypothesis of intrinsic geometry.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.random_projection import GaussianRandomProjection
from sklearn.preprocessing import StandardScaler


# ============================================================
# CONFIG
# ============================================================

OUTPUT_DIR = "RESEARCH/validation/lorenz/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

N_STEPS = 5000
DT = 0.01
N_CLUSTERS = 6
NOISE_LEVEL = 0.0

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


# ============================================================
# LORENZ SYSTEM
# ============================================================

def lorenz_step(x, y, z, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


def simulate_lorenz(n_steps=N_STEPS, dt=DT, noise=NOISE_LEVEL):
    x, y, z = 1.0, 1.0, 1.0
    traj = []

    for _ in range(n_steps):
        dx, dy, dz = lorenz_step(x, y, z)

        if noise > 0:
            dx += noise * np.random.randn()
            dy += noise * np.random.randn()
            dz += noise * np.random.randn()

        x += dx * dt
        y += dy * dt
        z += dz * dt

        traj.append([x, y, z])

    return np.array(traj)


# ============================================================
# TRANSITION MATRIX
# ============================================================

def compute_transition_matrix(labels, n_states):
    T = np.zeros((n_states, n_states))

    for i in range(len(labels) - 1):
        a = labels[i]
        b = labels[i + 1]

        if a < 0 or b < 0:
            continue

        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1

    return T / row_sums


def matrix_distance(A, B):
    return np.mean(np.abs(A - B))


# ============================================================
# PARTITION METHODS
# ============================================================

def partition_kmeans(X):
    labels = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_SEED,
        n_init=20
    ).fit_predict(X)

    return labels, N_CLUSTERS


def partition_pca_kmeans(X):
    X_pca = PCA(n_components=2, random_state=RANDOM_SEED).fit_transform(X)

    labels = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_SEED,
        n_init=20
    ).fit_predict(X_pca)

    return labels, N_CLUSTERS


def partition_random_projection_kmeans(X):
    X_proj = GaussianRandomProjection(
        n_components=2,
        random_state=RANDOM_SEED
    ).fit_transform(X)

    labels = KMeans(
        n_clusters=N_CLUSTERS,
        random_state=RANDOM_SEED,
        n_init=20
    ).fit_predict(X_proj)

    return labels, N_CLUSTERS


def partition_dbscan(X):
    """
    DBSCAN can create variable number of clusters and noise labels (-1).
    We standardize first for stable eps behavior.
    """
    X_scaled = StandardScaler().fit_transform(X)

    labels = DBSCAN(
        eps=0.35,
        min_samples=20
    ).fit_predict(X_scaled)

    valid = labels[labels >= 0]

    if len(valid) == 0:
        raise RuntimeError("DBSCAN found no valid clusters. Try increasing eps.")

    unique = sorted(np.unique(valid))

    # remap labels to 0..n-1
    mapping = {old: new for new, old in enumerate(unique)}
    remapped = np.array([mapping[l] if l >= 0 else -1 for l in labels])

    return remapped, len(unique)


# ============================================================
# MAIN
# ============================================================

def main():
    print("Running multi-partition invariance test...")

    traj = simulate_lorenz()

    methods = {
        "KMeans": partition_kmeans,
        "PCA + KMeans": partition_pca_kmeans,
        "Random Projection + KMeans": partition_random_projection_kmeans,
        "DBSCAN": partition_dbscan,
    }

    matrices = {}
    labels_dict = {}
    n_states_dict = {}

    for name, method in methods.items():
        labels, n_states = method(traj)
        T = compute_transition_matrix(labels, n_states)

        matrices[name] = T
        labels_dict[name] = labels
        n_states_dict[name] = n_states

        print(f"{name}: states = {n_states}")

    # ========================================================
    # Pairwise distances
    # NOTE:
    # DBSCAN may have a different matrix shape.
    # We only compare same-shape matrices directly.
    # ========================================================

    names = list(matrices.keys())
    distances = {}

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = names[i]
            b = names[j]

            if matrices[a].shape == matrices[b].shape:
                d = matrix_distance(matrices[a], matrices[b])
                distances[(a, b)] = d
            else:
                distances[(a, b)] = None

    print("\n=== Pairwise Transition Matrix Distances ===")
    for (a, b), d in distances.items():
        if d is None:
            print(f"{a} vs {b}: different shapes, skipped")
        else:
            print(f"{a} vs {b}: {d:.6f}")

    # ========================================================
    # Plot matrices
    # ========================================================

    fig, axs = plt.subplots(2, 2, figsize=(10, 9))
    axs = axs.flatten()

    for ax, name in zip(axs, names):
        im = ax.imshow(matrices[name])
        ax.set_title(name)
        ax.set_xlabel("to state")
        ax.set_ylabel("from state")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    plt.tight_layout()

    matrix_path = os.path.join(
        OUTPUT_DIR,
        "multi_partition_transition_matrices.png"
    )
    plt.savefig(matrix_path, dpi=200)
    plt.close()

    print(f"✅ Saved: {matrix_path}")

    # ========================================================
    # Plot labels on trajectory projection
    # ========================================================

    fig, axs = plt.subplots(2, 2, figsize=(10, 9))
    axs = axs.flatten()

    for ax, name in zip(axs, names):
        labels = labels_dict[name]

        ax.scatter(
            traj[:, 0],
            traj[:, 1],
            c=labels,
            s=2,
            alpha=0.7
        )

        ax.set_title(name)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    plt.tight_layout()

    partition_path = os.path.join(
        OUTPUT_DIR,
        "multi_partition_state_partitions.png"
    )
    plt.savefig(partition_path, dpi=200)
    plt.close()

    print(f"✅ Saved: {partition_path}")

    # ========================================================
    # Summary
    # ========================================================

    summary_path = os.path.join(
        OUTPUT_DIR,
        "multi_partition_invariance_summary.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH — Multi-Partition Invariance Test\n\n")
        f.write(f"Steps: {N_STEPS}\n")
        f.write(f"Noise level: {NOISE_LEVEL}\n")
        f.write(f"KMeans clusters: {N_CLUSTERS}\n\n")

        f.write("States per method:\n")
        for name in names:
            f.write(f"- {name}: {n_states_dict[name]}\n")

        f.write("\nPairwise transition matrix distances:\n")
        for (a, b), d in distances.items():
            if d is None:
                f.write(f"- {a} vs {b}: different shapes, skipped\n")
            else:
                f.write(f"- {a} vs {b}: {d:.6f}\n")

        f.write("\nInterpretation:\n")
        f.write(
            "If transition matrices remain structurally similar across "
            "multiple partition methods, this supports the hypothesis that "
            "the observed transition structure reflects intrinsic geometry "
            "rather than a single discretization artifact.\n"
        )

    print(f"✅ Saved summary: {summary_path}")
    print("\n✅ Multi-partition invariance test complete.")


if __name__ == "__main__":
    main()
