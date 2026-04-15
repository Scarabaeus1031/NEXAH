import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree


# ==================================================
# CONFIG
# ==================================================

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases"
INPUT_DIR = os.path.join(BASE_DIR, "outputs/analysis_export")
OUTPUT_DIR = os.path.join(INPUT_DIR, "likelihood_map")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==================================================
# LOAD DATA
# ==================================================

def load_data():
    trajectory = np.load(os.path.join(INPUT_DIR, "states.npy"))

    print("✅ trajectory loaded:", trajectory.shape)

    return trajectory


# ==================================================
# PCA PROJECTION (2D FIELD)
# ==================================================

def compute_pca_projection(data):
    mean = np.mean(data, axis=0)
    centered = data - mean

    U, S, Vt = np.linalg.svd(centered, full_matrices=False)

    PC = Vt[:2]
    projected = centered @ PC.T

    print("✅ PCA projection computed")

    return projected


# ==================================================
# BUILD GRID
# ==================================================

def build_grid(projected, resolution=150):

    x = projected[:, 0]
    y = projected[:, 1]

    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    xi = np.linspace(x_min, x_max, resolution)
    yi = np.linspace(y_min, y_max, resolution)

    PC1_grid, PC2_grid = np.meshgrid(xi, yi)

    print("✅ grid built:", PC1_grid.shape)

    return PC1_grid, PC2_grid


# ==================================================
# DISTANCE FIELD (TO TRAJECTORY CLOUD)
# ==================================================

def compute_distance_field(projected, PC1_grid, PC2_grid):

    points = np.vstack([PC1_grid.ravel(), PC2_grid.ravel()]).T

    tree = cKDTree(projected)

    dist, _ = tree.query(points, k=1)

    distance_field = dist.reshape(PC1_grid.shape)

    print("✅ distance field computed")

    return distance_field


# ==================================================
# COLLAPSE LIKELIHOOD
# ==================================================

def compute_likelihood(distance_field, scale=50.0):

    # exponential decay → high likelihood near trajectory manifold
    likelihood = np.exp(-distance_field * scale)

    print("✅ likelihood computed")

    return likelihood


# ==================================================
# PLOT
# ==================================================

def plot_likelihood(likelihood, PC1_grid, PC2_grid, projected):

    plt.figure(figsize=(10, 6))

    plt.imshow(
        likelihood,
        origin="lower",
        extent=[
            PC1_grid.min(), PC1_grid.max(),
            PC2_grid.min(), PC2_grid.max()
        ],
        aspect="auto"
    )

    plt.colorbar(label="Collapse likelihood")

    # trajectory overlay
    plt.plot(
        projected[:, 0],
        projected[:, 1],
        color="lime",
        linewidth=1,
        alpha=0.5,
        label="trajectory"
    )

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("NEXAH FIELD — Collapse Likelihood Map")
    plt.legend()

    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "collapse_likelihood.png")
    plt.savefig(out_path, dpi=200)

    print(f"💾 Plot saved → {out_path}")

    plt.show()


# ==================================================
# SAVE
# ==================================================

def save_all(likelihood, PC1_grid, PC2_grid, projected):

    np.save(os.path.join(INPUT_DIR, "collapse_likelihood.npy"), likelihood)
    np.save(os.path.join(INPUT_DIR, "PC1_grid.npy"), PC1_grid)
    np.save(os.path.join(INPUT_DIR, "PC2_grid.npy"), PC2_grid)
    np.save(os.path.join(INPUT_DIR, "trajectory_pca.npy"), projected)

    print("💾 All arrays saved → analysis_export/")


# ==================================================
# MAIN
# ==================================================

def main():

    trajectory = load_data()

    projected = compute_pca_projection(trajectory)

    PC1_grid, PC2_grid = build_grid(projected)

    distance_field = compute_distance_field(projected, PC1_grid, PC2_grid)

    likelihood = compute_likelihood(distance_field)

    plot_likelihood(likelihood, PC1_grid, PC2_grid, projected)

    save_all(likelihood, PC1_grid, PC2_grid, projected)

    print("🚀 Likelihood pipeline complete")


if __name__ == "__main__":
    main()
