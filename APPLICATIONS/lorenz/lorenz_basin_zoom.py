"""
NEXAH Lorenz Basin Zoom

This script computes a zoomed basin-fractal view for the Lorenz system.

It focuses on the central switching region where the basin boundary
between left and right attractor outcomes becomes visible in finer detail.

Outputs stored in:

APPLICATIONS/outputs/lorenz_basin_zoom/

Artifacts:
- lorenz_basin_zoom.png
- lorenz_basin_zoom.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_basin_zoom"
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
    Classify a trajectory by the sign dominance of x
    over the final segment.

    Returns:
    0 = LEFT basin
    1 = RIGHT basin
    2 = TRANSITION / undecided
    """
    tail = traj[-500:, 0]

    pos = np.sum(tail > 2.0)
    neg = np.sum(tail < -2.0)
    total = len(tail)

    if neg / total > 0.75:
        return 0

    if pos / total > 0.75:
        return 1

    return 2


# ---------------------------------------------------
# Grid computation
# ---------------------------------------------------

def compute_zoom_grid(
    x_min=-4.0,
    x_max=4.0,
    z_min=15.0,
    z_max=35.0,
    resolution=320,
    t_max=30.0,
    steps=3000
):
    xs = np.linspace(x_min, x_max, resolution)
    zs = np.linspace(z_min, z_max, resolution)
    t = np.linspace(0, t_max, steps)

    grid = np.zeros((resolution, resolution), dtype=int)

    for i, z0 in enumerate(zs):
        print(f"Row {i + 1}/{resolution}")
        for j, x0 in enumerate(xs):
            y0 = 0.0
            init = [x0, y0, z0]

            traj = odeint(lorenz, init, t)
            basin = classify_trajectory(traj)

            grid[i, j] = basin

    return grid, xs, zs


# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

def save_csv(grid):
    path = os.path.join(OUTPUT_DIR, "lorenz_basin_zoom.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in grid:
            writer.writerow(row.tolist())

    print("Saved:", path)


# ---------------------------------------------------
# Plot
# ---------------------------------------------------

def plot_zoom(grid, xs, zs):
    plt.figure(figsize=(9, 9))

    plt.imshow(
        grid,
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
    plt.title("Lorenz Basin Zoom")

    path = os.path.join(OUTPUT_DIR, "lorenz_basin_zoom.png")
    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    print("\nGenerating Lorenz basin zoom...\n")

    grid, xs, zs = compute_zoom_grid()

    save_csv(grid)
    plot_zoom(grid, xs, zs)

    print("\nLorenz basin zoom finished.\n")


if __name__ == "__main__":
    main()
