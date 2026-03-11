"""
NEXAH Symmetry Graph – PhiC Bridge
----------------------------------

Extends the resonance system from 2 phases to 3 phases:

    (phi_A, phi_B, phi_C)

Energy model:

    pair resonances:
        cos(phi_A - phi_B)
        cos(phi_A - phi_C)
        cos(phi_B - phi_C)

    triad resonance:
        cos(phi_A + phi_B - phi_C)

Outputs:

    three projections

        A-B
        A-C
        B-C

Each projection shows the averaged energy landscape.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Resonance energy (3-phase)
# --------------------------------------------------

def resonance_energy(phi_a, phi_b, phi_c,
                     K_ab=1.0,
                     K_ac=0.8,
                     K_bc=0.8,
                     K_triad=0.6):

    E_ab = -K_ab * np.cos(phi_a - phi_b)
    E_ac = -K_ac * np.cos(phi_a - phi_c)
    E_bc = -K_bc * np.cos(phi_b - phi_c)

    E_triad = -K_triad * np.cos(phi_a + phi_b - phi_c)

    return E_ab + E_ac + E_bc + E_triad


# --------------------------------------------------
# Compute projections
# --------------------------------------------------

def compute_projection_AB(grid=160):

    phi = np.linspace(-np.pi, np.pi, grid)

    A, B = np.meshgrid(phi, phi)

    C_vals = np.linspace(-np.pi, np.pi, 40)

    E = np.zeros_like(A)

    for phi_c in C_vals:

        E += resonance_energy(A, B, phi_c)

    E /= len(C_vals)

    return phi, A, B, E


def compute_projection_AC(grid=160):

    phi = np.linspace(-np.pi, np.pi, grid)

    A, C = np.meshgrid(phi, phi)

    B_vals = np.linspace(-np.pi, np.pi, 40)

    E = np.zeros_like(A)

    for phi_b in B_vals:

        E += resonance_energy(A, phi_b, C)

    E /= len(B_vals)

    return phi, A, C, E


def compute_projection_BC(grid=160):

    phi = np.linspace(-np.pi, np.pi, grid)

    B, C = np.meshgrid(phi, phi)

    A_vals = np.linspace(-np.pi, np.pi, 40)

    E = np.zeros_like(B)

    for phi_a in A_vals:

        E += resonance_energy(phi_a, B, C)

    E /= len(A_vals)

    return phi, B, C, E


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_three_projections():

    print("\nComputing 3-phase resonance projections...\n")

    phi, A, B, Eab = compute_projection_AB()
    phi, A, C, Eac = compute_projection_AC()
    phi, B, C, Ebc = compute_projection_BC()

    fig, axes = plt.subplots(1,3, figsize=(16,5))

    p0 = axes[0].contourf(A, B, Eab, levels=40)
    axes[0].set_title("Projection A-B")
    axes[0].set_xlabel("phi_A")
    axes[0].set_ylabel("phi_B")
    plt.colorbar(p0, ax=axes[0])

    p1 = axes[1].contourf(A, C, Eac, levels=40)
    axes[1].set_title("Projection A-C")
    axes[1].set_xlabel("phi_A")
    axes[1].set_ylabel("phi_C")
    plt.colorbar(p1, ax=axes[1])

    p2 = axes[2].contourf(B, C, Ebc, levels=40)
    axes[2].set_title("Projection B-C")
    axes[2].set_xlabel("phi_B")
    axes[2].set_ylabel("phi_C")
    plt.colorbar(p2, ax=axes[2])

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    plot_three_projections()
