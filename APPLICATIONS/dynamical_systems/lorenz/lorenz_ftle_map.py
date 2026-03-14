"""
Lorenz FTLE Map
Finite-Time Lyapunov Exponent field for the Lorenz system.

Part of the NEXAH Chaos Navigator.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------

OUTPUT_DIR = Path("../../outputs/lorenz_navigation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Lorenz system
# ---------------------------------------------------------------------

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])


def integrate(x0, dt=0.01, steps=2000):
    x = np.array(x0, dtype=float)
    traj = []

    for _ in range(steps):
        x = x + dt * lorenz(x)
        traj.append(x.copy())

    return np.array(traj)


# ---------------------------------------------------------------------
# FTLE computation
# ---------------------------------------------------------------------

def compute_ftle(grid_x, grid_y, z0=25.0, eps=1e-6):

    ftle = np.zeros((len(grid_x), len(grid_y)))

    for i, x in enumerate(grid_x):
        for j, y in enumerate(grid_y):

            p = np.array([x, y, z0])
            p_eps = np.array([x + eps, y, z0])

            traj1 = integrate(p)
            traj2 = integrate(p_eps)

            d0 = eps
            dT = np.linalg.norm(traj1[-1] - traj2[-1])

            if dT > 0:
                ftle[i, j] = np.log(dT / d0)

    return ftle


# ---------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------

def plot_ftle(ftle, grid_x, grid_y):

    plt.figure(figsize=(8, 6))

    plt.imshow(
        ftle.T,
        origin="lower",
        extent=[grid_x.min(), grid_x.max(), grid_y.min(), grid_y.max()],
        cmap="inferno",
        aspect="auto"
    )

    plt.colorbar(label="FTLE")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Lorenz FTLE Field")

    output_file = OUTPUT_DIR / "lorenz_ftle_map.png"

    plt.savefig(output_file, dpi=200)
    plt.close()

    print("FTLE map saved to:", output_file)


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

def main():

    print("Running Lorenz FTLE map")

    grid_x = np.linspace(-20, 20, 80)
    grid_y = np.linspace(-30, 30, 80)

    ftle = compute_ftle(grid_x, grid_y)

    plot_ftle(ftle, grid_x, grid_y)


# ---------------------------------------------------------------------

if name == "main":
    main()
