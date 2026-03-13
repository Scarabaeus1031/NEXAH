"""
NEXAH Lorenz Basin Boundary

This script computes a basin-boundary estimate for the Lorenz system.

Pipeline:

grid of initial conditions
    ↓
left/right/transition basin classification
    ↓
local neighborhood comparison
    ↓
boundary extraction

Outputs stored in:

APPLICATIONS/outputs/lorenz_basin_boundary/

Artifacts:
- lorenz_basin_boundary.png
- lorenz_basin_boundary.csv
- lorenz_basin_labels.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_basin_boundary"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Lorenz system
# ---------------------------------------------------

def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ]


# ---------------------------------------------------
# Basin classification
# ---------------------------------------------------

def classify_trajectory(traj):
    """
    Classify a trajectory by the sign dominance of x in the final segment.

    Returns:
    0 = LEFT
    1 = RIGHT
    2 = TRANSITION / undecided
    """
    tail = traj[-700:, 0]

    pos = np.sum(tail > 3.0)
    neg = np.sum(tail < -3.0)
    total = len(tail)

    if neg / total > 0.85:
        return 0

    if pos / total > 0.85:
        return 1

    return 2


# ---------------------------------------------------
# Grid computation
# ---------------------------------------------------

def compute_basin_grid(
    x_min=-4.0,
    x_max=4.0,
    z_min=15.0,
    z_max=35.0,
    resolution=260,
    t_max=40.0,
    steps=4000
):
    xs = np.linspace(x_min, x_max, resolution)
    zs = np.linspace(z_min, z_max, resolution)
    t = np.linspace(0, t_max, steps)

    grid = np.zeros((resolution, resolution), dtype=int)

    for i, z0 in enumerate(zs):
        print(f"Row {i+1}/{resolution}")
        for j, x0 in enumerate(xs):
            y0 = 0.0
            init = [x0, y0, z0]

            traj = odeint(lorenz, init, t)
            grid[i, j] = classify_trajectory(traj)

    return grid, xs, zs


# ---------------------------------------------------
# Boundary extraction
# ---------------------------------------------------

def extract_boundary(label_grid):
    """
    Mark cells as boundary if their local neighborhood contains
    more than one basin class (ignoring only-everything-same cases).

    Output:
    0 = non-boundary
    1 = boundary
    """
    rows, cols = label_grid.shape
    boundary = np.zeros_like(label_grid, dtype=int)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            neighborhood = label_grid[i-1:i+2, j-1:j+2].flatten()
            unique = set(neighborhood.tolist())

            if len(unique) > 1:
                boundary[i, j] = 1

    return boundary


# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

def save_csv(grid, filename):
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in grid:
            writer.writerow(row.tolist())

    print("Saved:", path)


# ---------------------------------------------------
# Plot boundary
# ---------------------------------------------------

def plot_boundary(boundary, xs, zs):
    plt.figure(figsize=(9, 9))

    plt.imshow(
        boundary,
        extent=[xs[0], xs[-1], zs[0], zs[-1]],
        origin="lower",
        cmap="inferno",
        aspect="auto"
    )

    cbar = plt.colorbar()
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(["INTERIOR", "BOUNDARY"])

    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("Lorenz Basin Boundary Estimate")

    path = os.path.join(OUTPUT_DIR, "lorenz_basin_boundary.png")
    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Optional basin plot
# ---------------------------------------------------

def plot_labels(label_grid, xs, zs):
    plt.figure(figsize=(9, 9))

    plt.imshow(
        label_grid,
        extent=[xs[0], xs[-1], zs[0], zs[-1]],
        origin="lower",
        cmap="plasma",
        aspect="auto"
    )

    cbar = plt.colorbar()
    cbar.set_ticks([0, 1, 2])
    cbar.set_ticklabels(["LEFT", "RIGHT", "TRANSITION"])

    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("Lorenz Basin Labels")

    path = os.path.join(OUTPUT_DIR, "lorenz_basin_labels.png")
    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    print("\nGenerating Lorenz basin boundary...\n")

    label_grid, xs, zs = compute_basin_grid()

    boundary = extract_boundary(label_grid)

    save_csv(label_grid, "lorenz_basin_labels.csv")
    save_csv(boundary, "lorenz_basin_boundary.csv")

    plot_labels(label_grid, xs, zs)
    plot_boundary(boundary, xs, zs)

    print("\nLorenz basin boundary finished.\n")


if __name__ == "__main__":
    main()
