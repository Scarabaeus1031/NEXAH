import os
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# CONFIG
# ==============================
BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# ==============================
# LOAD DATA
# ==============================
def load_data():
    collapse_likelihood = np.load(os.path.join(BASE_DIR, "collapse_likelihood.npy"))
    PC1_grid = np.load(os.path.join(BASE_DIR, "PC1_grid.npy"))
    PC2_grid = np.load(os.path.join(BASE_DIR, "PC2_grid.npy"))
    trajectory = np.load(os.path.join(BASE_DIR, "trajectory_pca.npy"))

    print("✅ Data loaded")
    return collapse_likelihood, PC1_grid, PC2_grid, trajectory

# ==============================
# EXTRACT RIFT CURVE
# ==============================
def extract_rift(collapse_likelihood, PC1_grid, PC2_grid):

    rift_points = []

    # iterate over PC1 axis (columns)
    for i in range(PC1_grid.shape[1]):
        col = collapse_likelihood[:, i]

        idx = np.argmax(col)

        x = PC1_grid[idx, i]
        y = PC2_grid[idx, i]

        rift_points.append([x, y])

    rift_curve = np.array(rift_points)

    print("✅ Rift extracted")
    return rift_curve

# ==============================
# PLOT
# ==============================
def plot_rift(collapse_likelihood, PC1_grid, PC2_grid, trajectory, rift_curve):

    plt.figure(figsize=(8, 5))

    plt.imshow(
        collapse_likelihood,
        extent=[
            PC1_grid.min(), PC1_grid.max(),
            PC2_grid.min(), PC2_grid.max()
        ],
        origin="lower",
        aspect="auto",
        cmap="viridis"
    )

    plt.plot(trajectory[:,0], trajectory[:,1], color="lime", label="trajectory")
    plt.plot(rift_curve[:,0], rift_curve[:,1], color="cyan", linewidth=2, label="rift curve")

    plt.legend()
    plt.title("NEXAH FIELD — Extracted Rift Curve")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.tight_layout()
    plt.show()

# ==============================
# MAIN
# ==============================
def main():

    collapse_likelihood, PC1_grid, PC2_grid, trajectory = load_data()

    rift_curve = extract_rift(collapse_likelihood, PC1_grid, PC2_grid)

    # ---- SAVE (CRITICAL FIX) ----
    os.makedirs(RIFT_DIR, exist_ok=True)

    np.save(os.path.join(RIFT_DIR, "rift_curve.npy"), rift_curve)

    print(f"💾 Rift curve saved → {RIFT_DIR}/rift_curve.npy")

    # ---- OPTIONAL DEBUG SAVE ----
    np.save(os.path.join(RIFT_DIR, "rift_curve_debug.npy"), rift_curve)

    plot_rift(collapse_likelihood, PC1_grid, PC2_grid, trajectory, rift_curve)

    print("🚀 Rift extraction complete")

# ==============================
if __name__ == "__main__":
    main()
