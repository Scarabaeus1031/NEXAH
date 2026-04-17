"""
NEXAH Lorenz Density Map

Computes a density map of the Lorenz attractor by projecting
trajectory points into a 2D histogram (X-Z plane).

Outputs:

APPLICATIONS/outputs/lorenz_density/

Files:
- lorenz_density_map.png
- lorenz_density.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output folder
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_density"
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
# Generate trajectory
# ---------------------------------------------------

def generate_trajectory(steps=60000):  # leicht reduziert für schnellere Demo
    print("→ Generating trajectory...")

    t = np.linspace(0, 60, steps)

    traj = odeint(
        lorenz,
        [1.0, 1.0, 1.0],
        t
    )

    return traj


# ---------------------------------------------------
# Density calculation
# ---------------------------------------------------

def compute_density(traj, bins=300):  # etwas weniger bins = schneller + cleaner
    print("→ Computing density map...")

    x = traj[:, 0]
    z = traj[:, 2]

    density, xedges, zedges = np.histogram2d(
        x,
        z,
        bins=bins
    )

    # kleine Stabilisierung für spätere Field-Nutzung
    density = density.astype(float)

    return density.T, xedges, zedges


# ---------------------------------------------------
# Save density CSV
# ---------------------------------------------------

def save_density_csv(density):
    path = os.path.join(OUTPUT_DIR, "lorenz_density.csv")

    np.savetxt(path, density, delimiter=",")

    print("Saved:", path)


# ---------------------------------------------------
# Plot density
# ---------------------------------------------------

def plot_density(density, xedges, zedges):
    print("→ Rendering density map...")

    plt.figure(figsize=(8, 8))

    plt.imshow(
        density,
        extent=[
            xedges[0],
            xedges[-1],
            zedges[0],
            zedges[-1]
        ],
        origin="lower",
        cmap="inferno",
        aspect="auto"
    )

    plt.colorbar(label="Density")

    plt.xlabel("X")
    plt.ylabel("Z")

    plt.title("Lorenz Attractor Density Map")

    path = os.path.join(OUTPUT_DIR, "lorenz_density_map.png")

    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# OPTIONAL: Minimal Field Layer (Preview)
# ---------------------------------------------------

def compute_field(density):
    print("→ Deriving simple field from density...")

    # einfache Normalisierung
    field = density / (np.max(density) + 1e-9)

    return field


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    print("\n🧠 Generating Lorenz Density Map\n")

    traj = generate_trajectory()

    density, xedges, zedges = compute_density(traj)

    save_density_csv(density)

    plot_density(density, xedges, zedges)

    # optional vorbereiten (noch nicht visualisieren)
    field = compute_field(density)

    print("\n✅ Density map finished.\n")


if __name__ == "__main__":
    main()
