"""
NEXAH Lorenz Field Gradient

Extends:
density → field → gradient (navigation structure)

Shows direction of movement inside the field.
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
# Compute field + gradient
# ---------------------------------------------------

def compute_field_and_gradient(density):

    print("→ Computing field and gradient...")

    # Field (stability interpretation)
    field = density / (np.max(density) + 1e-9)

    # Gradient (navigation direction)
    gy, gx = np.gradient(field)

    return field, gx, gy


# ---------------------------------------------------
# Plot field + vectors
# ---------------------------------------------------

def plot_field_with_vectors(field, gx, gy):

    print("→ Rendering field + gradient...")

    plt.figure(figsize=(8, 8))

    plt.imshow(field, cmap="viridis", origin="lower")

    # Sparse vector field
    step = 10
    plt.quiver(
        np.arange(0, field.shape[1], step),
        np.arange(0, field.shape[0], step),
        gx[::step, ::step],
        gy[::step, ::step],
        color="white",
        alpha=0.6,
        scale=50
    )

    plt.title("Lorenz Field + Gradient (Navigation Structure)")

    path = os.path.join(OUTPUT_DIR, "lorenz_field_gradient.png")

    plt.savefig(path, dpi=300)
    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    print("\n🧠 NEXAH Field Gradient Visualization\n")

    density = load_density()

    field, gx, gy = compute_field_and_gradient(density)

    plot_field_with_vectors(field, gx, gy)

    print("\n✅ Field gradient visualization complete.\n")


if __name__ == "__main__":
    main()
