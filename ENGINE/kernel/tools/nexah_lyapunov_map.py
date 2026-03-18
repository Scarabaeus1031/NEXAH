"""
NEXAH Lyapunov Map
==================

Computes Lyapunov exponents across the symmetry/drift parameter space.

Lyapunov exponent measures exponential divergence of trajectories.

Output
------
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/lyapunov_map.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/lyapunov_map.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Core angular dynamics
# --------------------------------------------------

def step(theta, n, drift):

    return (theta + (2*np.pi)/n + np.deg2rad(drift)) % (2*np.pi)


# --------------------------------------------------
# Lyapunov exponent
# --------------------------------------------------

def lyapunov_exponent(n, drift, steps=4000):

    theta = 0.1
    theta2 = theta + 1e-8

    divergence_sum = 0.0

    for _ in range(steps):

        theta = step(theta, n, drift)
        theta2 = step(theta2, n, drift)

        delta = abs(theta2 - theta)

        if delta == 0:
            delta = 1e-12

        divergence_sum += np.log(delta / 1e-8)

        theta2 = theta + (delta / abs(delta)) * 1e-8

    return divergence_sum / steps


# --------------------------------------------------
# Scan parameter space
# --------------------------------------------------

def compute_map():

    n_vals = list(range(3,21))
    drift_vals = np.linspace(0,6,40)

    grid = np.zeros((len(drift_vals), len(n_vals)))

    for i, drift in enumerate(drift_vals):

        for j, n in enumerate(n_vals):

            grid[i,j] = lyapunov_exponent(n, drift)

    return grid, n_vals, drift_vals


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_map(grid, n_vals, drift_vals):

    plt.figure(figsize=(10,6))

    im = plt.imshow(
        grid,
        origin="lower",
        aspect="auto",
        cmap="coolwarm"
    )

    plt.colorbar(im,label="Lyapunov exponent")

    plt.title("NEXAH Lyapunov Map")

    plt.xlabel("Symmetry (n)")
    plt.ylabel("Drift (deg)")

    plt.tight_layout()

    plt.savefig(OUT_IMG,dpi=300)

    print("\nSaved Lyapunov map:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nComputing Lyapunov map...\n")

    grid, n_vals, drift_vals = compute_map()

    plot_map(grid, n_vals, drift_vals)


if __name__ == "__main__":
    main()
