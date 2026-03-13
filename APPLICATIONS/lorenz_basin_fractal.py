"""
NEXAH Lorenz Basin Fractal

This script samples many initial conditions in the X-Z plane (with y=0),
simulates the Lorenz system, and classifies each point by its long-term wing:

- LEFT basin
- RIGHT basin
- TRANSITION / undecided

This creates a basin-style fractal boundary image.

Outputs stored in:

APPLICATIONS/outputs/lorenz_basin_fractal/

Artifacts:
- lorenz_basin_fractal.png
- lorenz_basin_fractal.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_basin_fractal"
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
    Classify by the sign of x over the final segment of the trajectory.

    Returns:
    - 0 = LEFT basin
    - 1 = RIGHT basin
    - 2 = TRANSITION / undecided
    """
    tail = traj[-400:, 0]  # x-values in final segment

    pos = np.sum(tail > 2.0)
    neg = np.sum(tail < -2.0)

    total = len(tail)

    if neg / total > 0.75:
        return 0

    if pos / total > 0.75:
        return 1

    return 2


# ---------------------------------------------------
# Grid simulation
# ---------------------------------------------------

def compute_basin_grid(
    x_min=-20.0,
    x_max=20.0,
    z_min=0.0,
    z_max=50.0,
    resolution=220,
    t_max=25.0,
    steps=2500
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
            basin = classify_trajectory(traj)

            grid[i, j] = basin

    return grid, xs, zs


# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

def save_csv(grid):
    path = os.path.join(OUTPUT_DIR, "lorenz_basin_fractal.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in grid:
            writer.writerow(row.tolist())

    print("Saved:", path)


# ---------------------------------------------------
# Plot
# ---------------------------------------------------

def plot_basin(grid, xs, zs):
    """
    0 = left, 1 = right, 2 = transition/undecided
    """
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
    plt.title("Lorenz Basin Fractal")

    path = os.path.join(OUTPUT_DIR, "lorenz_basin_fractal.png")
    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    print("\nGenerating Lorenz basin fractal...\n")

    grid, xs, zs = compute_basin_grid()

    save_csv(grid)
    plot_basin(grid, xs, zs)

    print("\nLorenz basin fractal finished.\n")


if __name__ == "__main__":
    main()
