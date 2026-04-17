"""
NEXAH Lorenz Field Visualization

Shows the transition:

density → field

This is the first step toward a true NEXAH field layer.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------
# Paths
# ---------------------------------------------------

DENSITY_PATH = "APPLICATIONS/outputs/lorenz_density/lorenz_density.csv"

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_field"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Load density
# ---------------------------------------------------

def load_density():
    print("→ Loading density...")
    return np.loadtxt(DENSITY_PATH, delimiter=",")


# ---------------------------------------------------
# Build field
# ---------------------------------------------------

def compute_field(density):
    print("→ Computing field from density...")

    # Variante 1: normalized density (stability)
    field = density / (np.max(density) + 1e-9)

    # Alternative später:
    # field = 1 / (density + 1e-6)

    return field


# ---------------------------------------------------
# Plot comparison
# ---------------------------------------------------

def plot_comparison(density, field):

    print("→ Rendering comparison...")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Density
    im1 = axes[0].imshow(density, cmap="inferno", origin="lower")
    axes[0].set_title("Density (Structure)")
    plt.colorbar(im1, ax=axes[0])

    # Field
    im2 = axes[1].imshow(field, cmap="viridis", origin="lower")
    axes[1].set_title("Field (Normalized Density)")
    plt.colorbar(im2, ax=axes[1])

    path = os.path.join(OUTPUT_DIR, "lorenz_density_vs_field.png")

    plt.savefig(path, dpi=300)
    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    print("\n🧠 NEXAH Field Visualization\n")

    density = load_density()
    field = compute_field(density)

    plot_comparison(density, field)

    print("\n✅ Field visualization complete.\n")


if __name__ == "__main__":
    main()
