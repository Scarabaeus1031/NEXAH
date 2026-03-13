"""
NEXAH Lorenz Lyapunov Field

This script estimates a local chaos-intensity field for the Lorenz system.

Pipeline:

Lorenz trajectory
    ↓
local velocity / local stretching proxy
    ↓
2D field accumulation in X-Z space
    ↓
Lyapunov-style intensity map

Outputs stored in:

APPLICATIONS/outputs/lorenz_lyapunov/

Artifacts:
- lorenz_lyapunov_field.png
- lorenz_lyapunov_field.csv

Note:
This is a local field approximation, not a rigorous global Lyapunov exponent.
It is designed as a practical exploratory NEXAH visualization tool.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_lyapunov"
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
# Jacobian of Lorenz system
# ---------------------------------------------------

def lorenz_jacobian(x, y, z, sigma=10.0, rho=28.0, beta=8/3):
    """
    Jacobian matrix of the Lorenz vector field.
    """
    return np.array([
        [-sigma, sigma, 0.0],
        [rho - z, -1.0, -x],
        [y, x, -beta]
    ], dtype=float)


# ---------------------------------------------------
# Generate trajectory
# ---------------------------------------------------

def generate_trajectory(steps=80000, t_max=80.0):
    t = np.linspace(0, t_max, steps)
    traj = odeint(lorenz, [1.0, 1.0, 1.0], t)
    return traj, t


# ---------------------------------------------------
# Local chaos proxy
# ---------------------------------------------------

def compute_local_chaos_proxy(traj):
    """
    Estimate local chaos intensity from the largest real part
    of the Jacobian eigenvalues at each point.

    This is a local instability proxy:
    positive values indicate local expansion tendency.
    """
    values = []

    for x, y, z in traj:
        J = lorenz_jacobian(x, y, z)
        eigvals = np.linalg.eigvals(J)
        max_real = np.max(np.real(eigvals))
        values.append(max_real)

    return np.array(values)


# ---------------------------------------------------
# Build field in X-Z plane
# ---------------------------------------------------

def accumulate_field(traj, values, bins=350):
    """
    Accumulate average local chaos intensity on an X-Z grid.
    """
    x = traj[:, 0]
    z = traj[:, 2]

    sum_grid, xedges, zedges = np.histogram2d(
        x, z,
        bins=bins,
        weights=values
    )

    count_grid, _, _ = np.histogram2d(
        x, z,
        bins=[xedges, zedges]
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        avg_grid = np.divide(
            sum_grid,
            count_grid,
            out=np.zeros_like(sum_grid),
            where=count_grid > 0
        )

    return avg_grid.T, count_grid.T, xedges, zedges


# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

def save_csv(field):
    path = os.path.join(OUTPUT_DIR, "lorenz_lyapunov_field.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for row in field:
            writer.writerow(row)

    print("Saved:", path)


# ---------------------------------------------------
# Plot field
# ---------------------------------------------------

def plot_field(field, xedges, zedges):
    plt.figure(figsize=(9, 8))

    plt.imshow(
        field,
        extent=[xedges[0], xedges[-1], zedges[0], zedges[-1]],
        origin="lower",
        cmap="magma",
        aspect="auto"
    )

    plt.colorbar(label="Local chaos intensity")

    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("Lorenz Lyapunov Field")

    path = os.path.join(OUTPUT_DIR, "lorenz_lyapunov_field.png")
    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Optional summary
# ---------------------------------------------------

def print_summary(values):
    print("\nLocal chaos proxy summary:\n")
    print("min  :", float(np.min(values)))
    print("max  :", float(np.max(values)))
    print("mean :", float(np.mean(values)))
    print("std  :", float(np.std(values)))


# ---------------------------------------------------
# Main pipeline
# ---------------------------------------------------

def main():
    print("\nGenerating Lorenz Lyapunov field...\n")

    traj, t = generate_trajectory()

    local_values = compute_local_chaos_proxy(traj)

    print_summary(local_values)

    field, counts, xedges, zedges = accumulate_field(
        traj=traj,
        values=local_values,
        bins=350
    )

    save_csv(field)
    plot_field(field, xedges, zedges)

    print("\nLorenz Lyapunov field finished.\n")


if __name__ == "__main__":
    main()
