"""
Lorenz Chaos Topography

Maps chaos intensity in the Lorenz system by counting
how often trajectories switch between the left and right lobes.

This script produces a chaos landscape over the (x, z) plane.

Output:
- Lorenz chaos topography heatmap
- saved automatically to APPLICATIONS/outputs/lorenz_navigation/
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

    return np.array([dx, dy, dz])


# ---------------------------------------------------------
# Chaos measure via lobe switch count
# ---------------------------------------------------------

def chaos_measure(x0, z0, dt=0.01, steps=6000):
    state = np.array([x0, 0.0, z0], dtype=float)

    last_lobe = np.sign(state[0])
    if last_lobe == 0:
        last_lobe = 1

    switches = 0

    for _ in range(steps):
        state = state + dt * lorenz(state)

        new_lobe = np.sign(state[0])
        if new_lobe == 0:
            new_lobe = last_lobe

        if new_lobe != last_lobe:
            switches += 1
            last_lobe = new_lobe

    return switches


# ---------------------------------------------------------
# Compute chaos topography
# ---------------------------------------------------------

def compute_chaos_map(resolution=200):
    x_vals = np.linspace(-20, 20, resolution)
    z_vals = np.linspace(0, 50, resolution)

    chaos_map = np.zeros((resolution, resolution), dtype=float)

    for i, x in enumerate(x_vals):
        print(f"row {i + 1} / {resolution}")

        for j, z in enumerate(z_vals):
            chaos_map[j, i] = chaos_measure(x, z)

    return x_vals, z_vals, chaos_map


# ---------------------------------------------------------
# Plot and save
# ---------------------------------------------------------

def save_heatmap(x_vals, z_vals, chaos_map):
    plt.figure(figsize=(9, 7))

    plt.imshow(
        chaos_map,
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        cmap="plasma",
        aspect="auto"
    )

    plt.colorbar(label="Lobe Switch Count")
    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title("Lorenz Chaos Topography")

    file_output = f"{OUTPUT_DIR}/lorenz_chaos_topography_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("\nComputing Lorenz Chaos Topography...\n")

    x_vals, z_vals, chaos_map = compute_chaos_map(resolution=200)

    save_heatmap(x_vals, z_vals, chaos_map)

    print("\nLorenz Chaos Topography complete.\n")


if __name__ == "__main__":
    main()
