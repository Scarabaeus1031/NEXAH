"""
NEXAH Symmetry Graph – Vector Field
-----------------------------------

Visualizes the reduced phase-flow field of the symmetry graph
in the 2D collective phase space (phi_A, phi_B).

Model:
- reduced resonance energy
- negative gradient flow
- resonance channels:
    1:1
    2:1
    3:2
    5:3

Outputs:
- energy contour background
- vector field (quiver)
- nullclines
- example trajectories
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Resonance energy
# --------------------------------------------------

def resonance_energy(
    phi_a,
    phi_b,
    K11=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K21=0.25,
    K32=0.18,
    K53=0.10
):

    E11 = -K11 * np.cos(phi_a - phi_b)
    Ea  = -K_ring_a * np.cos(phi_a)
    Eb  = -K_ring_b * np.cos(phi_b)

    E21 = -K21 * np.cos(2 * phi_a - phi_b)
    E32 = -K32 * np.cos(3 * phi_a - 2 * phi_b)
    E53 = -K53 * np.cos(5 * phi_a - 3 * phi_b)

    return E11 + Ea + Eb + E21 + E32 + E53


# --------------------------------------------------
# Gradient
# --------------------------------------------------

def resonance_gradient(
    phi_a,
    phi_b,
    K11=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K21=0.25,
    K32=0.18,
    K53=0.10
):

    dEa = (
        K11*np.sin(phi_a - phi_b)
        + K_ring_a*np.sin(phi_a)
        + 2*K21*np.sin(2*phi_a - phi_b)
        + 3*K32*np.sin(3*phi_a - 2*phi_b)
        + 5*K53*np.sin(5*phi_a - 3*phi_b)
    )

    dEb = (
        -K11*np.sin(phi_a - phi_b)
        + K_ring_b*np.sin(phi_b)
        - K21*np.sin(2*phi_a - phi_b)
        - 2*K32*np.sin(3*phi_a - 2*phi_b)
        - 3*K53*np.sin(5*phi_a - 3*phi_b)
    )

    return dEa, dEb


# --------------------------------------------------
# Flow field
# --------------------------------------------------

def flow_field(phi_a, phi_b):

    dEa, dEb = resonance_gradient(phi_a, phi_b)

    U = -dEa
    V = -dEb

    return U, V


# --------------------------------------------------
# Phase wrapping
# --------------------------------------------------

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi


# --------------------------------------------------
# Flow trajectory
# --------------------------------------------------

def run_flow(phi_a0, phi_b0, steps=200, dt=0.05):

    phi_a = phi_a0
    phi_b = phi_b0

    traj_a = []
    traj_b = []

    for _ in range(steps):

        traj_a.append(phi_a)
        traj_b.append(phi_b)

        U, V = flow_field(phi_a, phi_b)

        phi_a = wrap(phi_a + dt * U)
        phi_b = wrap(phi_b + dt * V)

    return np.array(traj_a), np.array(traj_b)


# --------------------------------------------------
# Build grids
# --------------------------------------------------

def build_grids():

    n_energy = 220
    n_field = 25

    phi_energy = np.linspace(-np.pi, np.pi, n_energy)
    XE, YE = np.meshgrid(phi_energy, phi_energy)
    ZE = resonance_energy(XE, YE)

    phi_field = np.linspace(-np.pi, np.pi, n_field)
    XF, YF = np.meshgrid(phi_field, phi_field)
    UF, VF = flow_field(XF, YF)

    return XE, YE, ZE, XF, YF, UF, VF


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_vector_field():

    XE, YE, ZE, XF, YF, UF, VF = build_grids()

    fig, axs = plt.subplots(1,2,figsize=(14,6))

    # Energy landscape
    contour = axs[0].contourf(XE, YE, ZE, levels=40)
    axs[0].contour(XE, YE, ZE, levels=25, colors="black", linewidths=0.25)

    # Vector field
    axs[0].quiver(
        XF, YF, UF, VF,
        angles="xy",
        scale_units="xy",
        scale=20
    )

    # Nullclines
    dEa, dEb = resonance_gradient(XE, YE)

    axs[0].contour(XE, YE, dEa, levels=[0], colors="cyan", linewidths=1.2)
    axs[0].contour(XE, YE, dEb, levels=[0], colors="magenta", linewidths=1.2)

    # Example trajectories
    initial_points = [
        (-2.5,-2.3),
        (-1.5,2.2),
        (-0.8,-0.6),
        (0.5,2.1),
        (1.0,-2.0)
    ]

    for i,(pa,pb) in enumerate(initial_points):

        ta,tb = run_flow(pa,pb)

        axs[0].plot(ta,tb,label=f"traj {i+1}")
        axs[0].scatter(pa,pb,s=25)

    axs[0].set_title("Resonance Vector Field")
    axs[0].set_xlabel("phi_A")
    axs[0].set_ylabel("phi_B")
    axs[0].legend()

    plt.colorbar(contour, ax=axs[0])


    # Energy along trajectories
    for pa,pb in initial_points:

        ta,tb = run_flow(pa,pb)

        energies = resonance_energy(ta,tb)

        axs[1].plot(energies)

    axs[1].set_title("Energy Descent")
    axs[1].set_xlabel("step")
    axs[1].set_ylabel("Energy")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nComputing symmetry graph vector field...\n")

    XE, YE, ZE, _, _, _, _ = build_grids()

    print("Landscape shape:", ZE.shape)
    print("Energy min:", float(np.min(ZE)))
    print("Energy max:", float(np.max(ZE)))

    plot_vector_field()
