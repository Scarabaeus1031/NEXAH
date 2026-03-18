"""
NEXAH Symmetry Graph – Resonance Landscape
------------------------------------------

Extended reduced energy landscape with multiple resonance couplings.

Idea:
- keep the reduced two-phase picture (phi_A, phi_B)
- include several locking channels:
    1:1   hub synchronization
    2:1   asymmetric cross-lock
    3:2   higher resonance split
    5:3   weaker harmonic channel
- visualize the resulting potential landscape

This is still a reduced collective model, but it is richer than the
basic energy landscape and can generate multiple valleys / islands.

Output:
- 3D surface
- contour map
- printed minima
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Reduced resonance energy
# --------------------------------------------------

def resonance_energy(
    phi_a,
    phi_b,
    K11=1.00,   # 1:1 hub-lock
    K_ring_a=0.70,
    K_ring_b=0.70,
    K21=0.25,   # 2:1 cross term
    K32=0.18,   # 3:2 resonance
    K53=0.10    # 5:3 resonance
):
    """
    Extended reduced energy function.

    Terms:
    - 1:1 locking term:
        - 1:1 locking term
    - ring coherence wells
    - 2:1 resonance
    - 3:2 resonance
    - 5:3 resonance
    """

    # hub synchronization
    E11 = -K11 * np.cos(phi_a - phi_b)

    # local ring coherence
    Ea = -K_ring_a * np.cos(phi_a)
    Eb = -K_ring_b * np.cos(phi_b)

    # asymmetric cross coupling
    E21 = -K21 * np.cos(2 * phi_a - phi_b)

    # higher resonances
    E32 = -K32 * np.cos(3 * phi_a - 2 * phi_b)
    E53 = -K53 * np.cos(5 * phi_a - 3 * phi_b)

    return E11 + Ea + Eb + E21 + E32 + E53


# --------------------------------------------------
# Landscape grid
# --------------------------------------------------

def build_resonance_landscape(n=240):

    phi_vals = np.linspace(-np.pi, np.pi, n)

    X, Y = np.meshgrid(phi_vals, phi_vals)

    Z = resonance_energy(X, Y)

    return phi_vals, X, Y, Z


# --------------------------------------------------
# Find minima
# --------------------------------------------------

def find_minima(phi_vals, Z, n_min=8):

    flat = Z.flatten()
    idx = np.argsort(flat)

    print("\nLowest energy minima:\n")

    for i in range(n_min):

        k = idx[i]
        iy, ix = np.unravel_index(k, Z.shape)

        print(
            f"{i+1:2d} : "
            f"phi_A = {phi_vals[ix]: .3f}, "
            f"phi_B = {phi_vals[iy]: .3f}, "
            f"E = {Z[iy, ix]: .6f}"
        )


# --------------------------------------------------
# Plotting
# --------------------------------------------------

def plot_landscape(phi_vals, X, Y, Z):

    fig = plt.figure(figsize=(14,6))

    # --- 3D surface ---
    ax1 = fig.add_subplot(1,2,1, projection="3d")

    ax1.plot_surface(
        X, Y, Z,
        cmap="plasma",
        linewidth=0,
        antialiased=True
    )

    ax1.set_title("Resonance Energy Surface")
    ax1.set_xlabel("phi_A")
    ax1.set_ylabel("phi_B")
    ax1.set_zlabel("Energy")

    # --- contour map ---
    ax2 = fig.add_subplot(1,2,2)

    contour = ax2.contourf(
        X,
        Y,
        Z,
        levels=60,
        cmap="plasma"
    )

    ax2.contour(
        X,
        Y,
        Z,
        levels=25,
        colors="black",
        linewidths=0.3,
        alpha=0.4
    )

    ax2.set_title("Resonance Landscape")
    ax2.set_xlabel("phi_A")
    ax2.set_ylabel("phi_B")

    plt.colorbar(contour, ax=ax2, label="Energy")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nComputing symmetry graph resonance landscape...\n")

    phi_vals, X, Y, Z = build_resonance_landscape()

    print("Landscape shape:", Z.shape)
    print("Energy min:", float(np.min(Z)))
    print("Energy max:", float(np.max(Z)))

    find_minima(phi_vals, Z)

    plot_landscape(phi_vals, X, Y, Z)
