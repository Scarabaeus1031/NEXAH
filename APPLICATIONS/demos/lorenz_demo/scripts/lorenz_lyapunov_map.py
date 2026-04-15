"""
Lorenz Lyapunov Map

Estimate local chaos intensity in the Lorenz system by measuring
how quickly two nearby trajectories diverge.

This script computes a 2D Lyapunov-like map over the (x, z) plane.
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Output folder
# ---------------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------------

sigma = 10.0
rho = 28.0
beta = 8 / 3


# ---------------------------------------------------------
# Lorenz system
# ---------------------------------------------------------

def lorenz(state):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz], dtype=float)


# ---------------------------------------------------------
# One-step Euler update
# ---------------------------------------------------------

def step(state, dt=0.01):
    return state + dt * lorenz(state)


# ---------------------------------------------------------
# Local Lyapunov estimate
# ---------------------------------------------------------

def local_lyapunov(x0, z0, dt=0.01, steps=2500, eps=1e-6):
    s1 = np.array([x0, 0.0, z0], dtype=float)
    s2 = np.array([x0 + eps, 0.0, z0], dtype=float)

    d0 = np.linalg.norm(s2 - s1)

    for _ in range(steps):
        s1 = step(s1, dt=dt)
        s2 = step(s2, dt=dt)

    dT = np.linalg.norm(s2 - s1)

    # avoid numerical issues
    d0 = max(d0, 1e-15)
    dT = max(dT, 1e-15)

    T = steps * dt
    lam = (1.0 / T) * np.log(dT / d0)

    return lam


# ---------------------------------------------------------
# Compute Lyapunov map
# ---------------------------------------------------------

def compute_map(resolution=120):
    x_vals = np.linspace(-20, 20, resolution)
    z_vals = np.linspace(0, 50, resolution)

    lyap_map = np.zeros((resolution, resolution), dtype=float)

    for i, x in enumerate(x_vals):
        print(f"row {i + 1} / {resolution}")

        for j, z in enumerate(z_vals):
            lyap_map[j, i] = local_lyapunov(x, z)

    return x_vals, z_vals, lyap_map


# ---------------------------------------------------------
# Plot
# ---------------------------------------------------------

def plot_map(x_vals, z_vals, lyap_map):
    plt.figure(figsize=(9, 7))

    plt.imshow(
        lyap_map,
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        cmap="inferno",
        aspect="auto"
    )

    plt.colorbar(label="Local Lyapunov Estimate")
    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("Lorenz Lyapunov Chaos Map")

    file_output = f"{OUTPUT_DIR}/lorenz_lyapunov_map_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("\nComputing Lorenz Lyapunov map...\n")

    x_vals, z_vals, lyap_map = compute_map(resolution=120)

    plot_map(x_vals, z_vals, lyap_map)

    print("\nLyapunov map complete.\n")


if __name__ == "__main__":
    main()
