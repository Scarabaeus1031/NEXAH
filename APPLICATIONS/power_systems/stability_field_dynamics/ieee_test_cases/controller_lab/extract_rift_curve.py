import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ==================================================
# CONFIG
# ==================================================

INPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
OUTPUT_DIR = os.path.join(INPUT_DIR, "rift_extraction")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==================================================
# LOAD DATA
# ==================================================

def load_data():
    collapse_likelihood = np.load(os.path.join(INPUT_DIR, "collapse_likelihood.npy"))
    PC1_grid = np.load(os.path.join(INPUT_DIR, "PC1_grid.npy"))
    PC2_grid = np.load(os.path.join(INPUT_DIR, "PC2_grid.npy"))

    # optional
    trajectory_path = os.path.join(INPUT_DIR, "trajectory_pca.npy")
    trajectory = None
    if os.path.exists(trajectory_path):
        trajectory = np.load(trajectory_path)

    print("✅ Data loaded")

    return collapse_likelihood, PC1_grid, PC2_grid, trajectory


# ==================================================
# RIFT EXTRACTION
# ==================================================

def extract_rift_curve(collapse_likelihood, PC1_grid, PC2_grid, smooth=True):

    Ny, Nx = collapse_likelihood.shape

    rift_x = []
    rift_y = []
    rift_strength = []

    for i in range(Nx):
        column = collapse_likelihood[:, i]

        if np.all(column == 0):
            continue

        j = np.argmax(column)

        rift_x.append(PC1_grid[j, i])
        rift_y.append(PC2_grid[j, i])
        rift_strength.append(column[j])

    rift_x = np.array(rift_x)
    rift_y = np.array(rift_y)
    rift_strength = np.array(rift_strength)

    # smoothing
    if smooth and len(rift_y) > 5:
        rift_y = gaussian_filter1d(rift_y, sigma=2)

    print("✅ Rift extracted")

    return rift_x, rift_y, rift_strength


# ==================================================
# VISUALIZATION
# ==================================================

def plot_rift(collapse_likelihood, PC1_grid, PC2_grid,
              rift_x, rift_y, trajectory=None):

    plt.figure(figsize=(10, 6))

    plt.imshow(
        collapse_likelihood,
        origin='lower',
        extent=[
            PC1_grid.min(), PC1_grid.max(),
            PC2_grid.min(), PC2_grid.max()
        ],
        aspect='auto'
    )

    plt.colorbar(label="Collapse likelihood")

    # Rift line
    plt.plot(rift_x, rift_y, color='cyan', linewidth=2, label="rift curve")

    # trajectory overlay
    if trajectory is not None:
        plt.plot(
            trajectory[:, 0],
            trajectory[:, 1],
            color='lime',
            linewidth=1,
            alpha=0.7,
            label="trajectory"
        )

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("NEXAH FIELD — Extracted Rift Curve")
    plt.legend()

    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "rift_curve_plot.png")
    plt.savefig(out_path, dpi=200)

    print(f"💾 Plot saved → {out_path}")

    plt.show()


# ==================================================
# SAVE DATA
# ==================================================

def save_rift_curve(rift_x, rift_y, rift_strength):

    np.save(os.path.join(OUTPUT_DIR, "rift_x.npy"), rift_x)
    np.save(os.path.join(OUTPUT_DIR, "rift_y.npy"), rift_y)
    np.save(os.path.join(OUTPUT_DIR, "rift_strength.npy"), rift_strength)

    print(f"💾 Rift curve saved → {OUTPUT_DIR}")


# ==================================================
# MAIN
# ==================================================

def main():

    collapse_likelihood, PC1_grid, PC2_grid, trajectory = load_data()

    rift_x, rift_y, rift_strength = extract_rift_curve(
        collapse_likelihood,
        PC1_grid,
        PC2_grid
    )

    plot_rift(
        collapse_likelihood,
        PC1_grid,
        PC2_grid,
        rift_x,
        rift_y,
        trajectory
    )

    save_rift_curve(rift_x, rift_y, rift_strength)

    print("🚀 Rift extraction complete")


if __name__ == "__main__":
    main()
