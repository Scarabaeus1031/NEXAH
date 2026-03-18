"""
NEXAH Symmetry Graph – Resonance Flow
-------------------------------------

Simulates gradient-like trajectories on the extended resonance landscape
of the symmetry graph.

Model:
- reduced 2D collective phase space (phi_A, phi_B)
- multiple resonance channels:
    1:1
    2:1
    3:2
    5:3

Goal:
visualize how trajectories move through resonance valleys / channels.

Outputs:
- contour map with trajectories
- energy descent curves
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
# Gradient of energy
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

    dE_a = (
        K11*np.sin(phi_a - phi_b)
        + K_ring_a*np.sin(phi_a)
        + 2*K21*np.sin(2*phi_a - phi_b)
        + 3*K32*np.sin(3*phi_a - 2*phi_b)
        + 5*K53*np.sin(5*phi_a - 3*phi_b)
    )

    dE_b = (
        -K11*np.sin(phi_a - phi_b)
        + K_ring_b*np.sin(phi_b)
        - K21*np.sin(2*phi_a - phi_b)
        - 2*K32*np.sin(3*phi_a - 2*phi_b)
        - 3*K53*np.sin(5*phi_a - 3*phi_b)
    )

    return dE_a, dE_b


# --------------------------------------------------
# Phase wrap
# --------------------------------------------------

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi


# --------------------------------------------------
# Compute landscape grid
# --------------------------------------------------

def build_landscape(n=240):

    phi_vals = np.linspace(-np.pi, np.pi, n)
    X, Y = np.meshgrid(phi_vals, phi_vals)

    Z = resonance_energy(X, Y)

    return phi_vals, X, Y, Z


# --------------------------------------------------
# Run gradient flow
# --------------------------------------------------

def run_flow(phi_a0, phi_b0, steps=300, dt=0.05):

    phi_a = phi_a0
    phi_b = phi_b0

    traj_a = []
    traj_b = []
    energy = []

    for _ in range(steps):

        traj_a.append(phi_a)
        traj_b.append(phi_b)

        energy.append(resonance_energy(phi_a, phi_b))

        dEa, dEb = resonance_gradient(phi_a, phi_b)

        phi_a = phi_a - dt * dEa
        phi_b = phi_b - dt * dEb

        phi_a = wrap(phi_a)
        phi_b = wrap(phi_b)

    return np.array(traj_a), np.array(traj_b), np.array(energy)


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_flow(X, Y, Z, trajectories):

    fig, axs = plt.subplots(1,2,figsize=(14,6))

    # contour map
    contour = axs[0].contourf(X, Y, Z, levels=40)
    axs[0].contour(X, Y, Z, levels=40, linewidths=0.3)

    for i,(ta,tb,en) in enumerate(trajectories):
        axs[0].plot(ta, tb, label=f"traj {i+1}")
        axs[0].scatter(ta[0], tb[0], s=20)

    axs[0].set_title("Resonance Flow")
    axs[0].set_xlabel("phi_A")
    axs[0].set_ylabel("phi_B")
    axs[0].legend()

    plt.colorbar(contour, ax=axs[0])


    # energy curves
    for i,(ta,tb,en) in enumerate(trajectories):
        axs[1].plot(en, label=f"traj {i+1}")

    axs[1].set_title("Energy Descent")
    axs[1].set_xlabel("step")
    axs[1].set_ylabel("Energy")
    axs[1].legend()

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nComputing symmetry graph resonance flow...\n")

    phi_vals, X, Y, Z = build_landscape(n=240)

    print("Landscape shape:", Z.shape)
    print("Energy min:", float(np.min(Z)))
    print("Energy max:", float(np.max(Z)))

    initial_points = [
        (-2.5,-2.3),
        (-1.5, 2.2),
        (-0.8,-0.6),
        (0.5, 2.1),
        (1.0,-2.0),
        (2.4, 2.0)
    ]

    trajectories = []

    for pa,pb in initial_points:
        trajectories.append(run_flow(pa,pb))

    plot_flow(X, Y, Z, trajectories)
