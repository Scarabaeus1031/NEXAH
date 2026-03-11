"""
NEXAH Symmetry Graph – PhiC Lissajous Flow
------------------------------------------

Three-phase resonance flow experiment.

Phases:
    phi_A
    phi_B
    phi_C

Interpretation:
- A-B acts as the backbone / synchronization axis
- C acts as the shell / modulation layer
- triad term produces Lissajous-like interference patterns

Dynamics:
    dphi/dt = -grad(E)

Energy:
    E =
      - K_ab * cos(phi_A - phi_B)
      - K_ac * cos(phi_A - phi_C)
      - K_bc * cos(phi_B - phi_C)
      - K_triad * cos(phi_A + phi_B - phi_C)

Outputs:
- energy projections
- Lissajous-like trajectories in phase space
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# helpers
# --------------------------------------------------

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi


# --------------------------------------------------
# energy
# --------------------------------------------------

def resonance_energy(phi_a, phi_b, phi_c,
                     K_ab=0.45,
                     K_ac=0.80,
                     K_bc=0.80,
                     K_triad=1.10):

    E_ab = -K_ab * np.cos(phi_a - phi_b)
    E_ac = -K_ac * np.cos(phi_a - phi_c)
    E_bc = -K_bc * np.cos(phi_b - phi_c)

    E_triad = -K_triad * np.cos(phi_a + phi_b - phi_c)

    return E_ab + E_ac + E_bc + E_triad


# --------------------------------------------------
# gradient
# --------------------------------------------------

def resonance_gradient(phi_a, phi_b, phi_c,
                       K_ab=0.45,
                       K_ac=0.80,
                       K_bc=0.80,
                       K_triad=1.10):

    dE_a = (
        K_ab * np.sin(phi_a - phi_b)
        + K_ac * np.sin(phi_a - phi_c)
        + K_triad * np.sin(phi_a + phi_b - phi_c)
    )

    dE_b = (
        -K_ab * np.sin(phi_a - phi_b)
        + K_bc * np.sin(phi_b - phi_c)
        + K_triad * np.sin(phi_a + phi_b - phi_c)
    )

    dE_c = (
        -K_ac * np.sin(phi_a - phi_c)
        -K_bc * np.sin(phi_b - phi_c)
        -K_triad * np.sin(phi_a + phi_b - phi_c)
    )

    return dE_a, dE_b, dE_c


# --------------------------------------------------
# trajectory simulation
# --------------------------------------------------

def simulate(start,
             steps=600,
             dt=0.035):

    phi_a, phi_b, phi_c = start

    traj_a = [phi_a]
    traj_b = [phi_b]
    traj_c = [phi_c]

    for _ in range(steps):

        dA, dB, dC = resonance_gradient(phi_a, phi_b, phi_c)

        phi_a = wrap(phi_a - dt * dA)
        phi_b = wrap(phi_b - dt * dB)
        phi_c = wrap(phi_c - dt * dC)

        traj_a.append(phi_a)
        traj_b.append(phi_b)
        traj_c.append(phi_c)

    return np.array(traj_a), np.array(traj_b), np.array(traj_c)


# --------------------------------------------------
# projection energy field
# --------------------------------------------------

def compute_projection_AB(grid=180):

    phi = np.linspace(-np.pi, np.pi, grid)

    A, B = np.meshgrid(phi, phi)

    C_vals = np.linspace(-np.pi, np.pi, 40)

    E = np.zeros_like(A)

    for phi_c in C_vals:
        E += resonance_energy(A, B, phi_c)

    E /= len(C_vals)

    return phi, A, B, E


# --------------------------------------------------
# plot
# --------------------------------------------------

def plot_system():

    phi, A, B, E = compute_projection_AB()

    fig, ax = plt.subplots(figsize=(7,6))

    c = ax.contourf(A, B, E, levels=40)
    plt.colorbar(c)

    ax.set_title("A–B Projection with Lissajous Flow")
    ax.set_xlabel("phi_A")
    ax.set_ylabel("phi_B")

    # trajectories
    seeds = [
        (0.2, -1.5, 1.2),
        (-2.1, 0.4, -1.0),
        (1.3, 2.2, -2.0),
        (-1.2, -2.5, 0.8)
    ]

    for s in seeds:

        a,b,c = simulate(s)

        ax.plot(a, b, linewidth=2)

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nRunning PhiC Lissajous Flow...\n")

    plot_system()
