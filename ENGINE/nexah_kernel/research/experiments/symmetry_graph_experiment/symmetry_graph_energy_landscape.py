"""
NEXAH Symmetry Graph – Energy Landscape
---------------------------------------

Builds a simple energy / potential landscape for the symmetry graph
using a reduced two-phase description.

Idea:
- project the full network onto two collective phase coordinates
- interpret synchronization as low-energy regions
- visualize the resulting potential surface

This is not the full exact Kuramoto energy of all 19 oscillators.
It is a reduced collective-mode landscape for intuition and exploration.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Reduced collective energy
# --------------------------------------------------

def reduced_energy(phi_a, phi_b, K_hub=1.0, K_ring_a=0.7, K_ring_b=0.7, K_cross=0.25):
    """
    Reduced energy function for two collective phase coordinates.

    phi_a : collective phase of hub_A + C5 + C6A block
    phi_b : collective phase of hub_B + C6B block

    Terms:
    - hub coupling
    - internal coherence wells
    - weak asymmetry / frustration
    """

    # hub-hub locking term
    E_hub = -K_hub * np.cos(phi_a - phi_b)

    # local coherence wells
    E_a = -K_ring_a * np.cos(phi_a)
    E_b = -K_ring_b * np.cos(phi_b)

    # weak cross frustration / asymmetry
    E_cross = -K_cross * np.cos(2 * phi_a - phi_b)

    return E_hub + E_a + E_b + E_cross


# --------------------------------------------------
# Grid evaluation
# --------------------------------------------------

def build_landscape(
    n=250,
    K_hub=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K_cross=0.25
):
    phi_vals = np.linspace(-np.pi, np.pi, n)

    X, Y = np.meshgrid(phi_vals, phi_vals)

    Z = reduced_energy(
        X,
        Y,
        K_hub=K_hub,
        K_ring_a=K_ring_a,
        K_ring_b=K_ring_b,
        K_cross=K_cross
    )

    return X, Y, Z


# --------------------------------------------------
# Plotting
# --------------------------------------------------

def plot_landscape(X, Y, Z):
    fig = plt.figure(figsize=(14, 6))

    # 3D surface
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.plot_surface(X, Y, Z, linewidth=0, antialiased=True)
    ax1.set_title("Reduced Energy Surface")
    ax1.set_xlabel("phi_A")
    ax1.set_ylabel("phi_B")
    ax1.set_zlabel("E")

    # 2D contour
    ax2 = fig.add_subplot(1, 2, 2)
    contour = ax2.contourf(X, Y, Z, levels=40)
    plt.colorbar(contour, ax=ax2, label="Energy")
    ax2.set_title("Energy Contour Map")
    ax2.set_xlabel("phi_A")
    ax2.set_ylabel("phi_B")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nBuilding symmetry graph energy landscape...\n")

    X, Y, Z = build_landscape(
        n=250,
        K_hub=1.0,
        K_ring_a=0.7,
        K_ring_b=0.7,
        K_cross=0.25
    )

    print("Landscape shape:", Z.shape)
    print("Min energy:", float(np.min(Z)))
    print("Max energy:", float(np.max(Z)))

    plot_landscape(X, Y, Z)
