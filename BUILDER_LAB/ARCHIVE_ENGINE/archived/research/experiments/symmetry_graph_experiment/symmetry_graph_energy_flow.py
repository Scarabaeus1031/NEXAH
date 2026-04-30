"""
NEXAH Symmetry Graph – Energy Flow
----------------------------------

Simulates gradient-like trajectories on the reduced energy landscape
of the symmetry graph.

Idea:
- use the same reduced two-phase energy model as in symmetry_graph_energy_landscape.py
- compute the negative gradient flow
- launch several trajectories from different initial points
- visualize how they move toward low-energy basins

This is a reduced collective-flow model, not the full 19-oscillator system.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Reduced collective energy
# --------------------------------------------------

def reduced_energy(phi_a, phi_b, K_hub=1.0, K_ring_a=0.7, K_ring_b=0.7, K_cross=0.25):
    """
    Reduced energy function for two collective phase coordinates.
    """
    E_hub = -K_hub * np.cos(phi_a - phi_b)
    E_a = -K_ring_a * np.cos(phi_a)
    E_b = -K_ring_b * np.cos(phi_b)
    E_cross = -K_cross * np.cos(2 * phi_a - phi_b)

    return E_hub + E_a + E_b + E_cross


# --------------------------------------------------
# Gradient
# --------------------------------------------------

def energy_gradient(phi_a, phi_b, K_hub=1.0, K_ring_a=0.7, K_ring_b=0.7, K_cross=0.25):
    """
    Analytical gradient of the reduced energy.

    E = -K_hub cos(phi_a - phi_b)
        -K_ring_a cos(phi_a)
        -K_ring_b cos(phi_b)
        -K_cross cos(2 phi_a - phi_b)
    """

    dE_dphi_a = (
        K_hub * np.sin(phi_a - phi_b)
        + K_ring_a * np.sin(phi_a)
        + 2.0 * K_cross * np.sin(2.0 * phi_a - phi_b)
    )

    dE_dphi_b = (
        -K_hub * np.sin(phi_a - phi_b)
        + K_ring_b * np.sin(phi_b)
        - K_cross * np.sin(2.0 * phi_a - phi_b)
    )

    return dE_dphi_a, dE_dphi_b


# --------------------------------------------------
# Wrapping helper
# --------------------------------------------------

def wrap_phase(x):
    """
    Wrap phase into [-pi, pi].
    """
    return (x + np.pi) % (2 * np.pi) - np.pi


# --------------------------------------------------
# Landscape grid
# --------------------------------------------------

def build_landscape(
    n=220,
    K_hub=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K_cross=0.25
):
    phi_vals = np.linspace(-np.pi, np.pi, n)
    X, Y = np.meshgrid(phi_vals, phi_vals)

    Z = reduced_energy(
        X, Y,
        K_hub=K_hub,
        K_ring_a=K_ring_a,
        K_ring_b=K_ring_b,
        K_cross=K_cross
    )

    return X, Y, Z


# --------------------------------------------------
# Flow simulation
# --------------------------------------------------

def run_energy_flow(
    phi_a0,
    phi_b0,
    steps=300,
    dt=0.06,
    damping=1.0,
    noise=0.0,
    K_hub=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K_cross=0.25
):
    """
    Negative-gradient flow:
        dphi/dt = - grad E

    Optional tiny noise can be added to explore basin switching.
    """

    phi_a = float(phi_a0)
    phi_b = float(phi_b0)

    traj_a = [phi_a]
    traj_b = [phi_b]
    energies = [float(reduced_energy(
        phi_a, phi_b,
        K_hub=K_hub,
        K_ring_a=K_ring_a,
        K_ring_b=K_ring_b,
        K_cross=K_cross
    ))]

    for _ in range(steps):
        dE_a, dE_b = energy_gradient(
            phi_a, phi_b,
            K_hub=K_hub,
            K_ring_a=K_ring_a,
            K_ring_b=K_ring_b,
            K_cross=K_cross
        )

        phi_a = phi_a - damping * dE_a * dt
        phi_b = phi_b - damping * dE_b * dt

        if noise > 0:
            phi_a += np.random.normal(0.0, noise)
            phi_b += np.random.normal(0.0, noise)

        phi_a = wrap_phase(phi_a)
        phi_b = wrap_phase(phi_b)

        traj_a.append(phi_a)
        traj_b.append(phi_b)
        energies.append(float(reduced_energy(
            phi_a, phi_b,
            K_hub=K_hub,
            K_ring_a=K_ring_a,
            K_ring_b=K_ring_b,
            K_cross=K_cross
        )))

    return np.array(traj_a), np.array(traj_b), np.array(energies)


# --------------------------------------------------
# Initial conditions
# --------------------------------------------------

def default_initial_points():
    return [
        (-2.6, -2.4),
        (-2.2,  1.8),
        (-1.2, -0.8),
        (-0.3,  2.0),
        ( 0.3, -2.2),
        ( 0.6,  0.9),
        ( 1.8, -0.5),
        ( 2.5,  2.2),
    ]


# --------------------------------------------------
# Plotting
# --------------------------------------------------

def plot_energy_flow(X, Y, Z, trajectories):
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # Contour map with trajectories
    contour = axs[0].contourf(X, Y, Z, levels=40, cmap="plasma")
    axs[0].contour(X, Y, Z, levels=25, colors="black", linewidths=0.35, alpha=0.35)

    for idx, (ta, tb, en) in enumerate(trajectories):
        axs[0].plot(ta, tb, linewidth=2, label=f"traj {idx+1}")
        axs[0].scatter(ta[0], tb[0], s=35, marker="o")
        axs[0].scatter(ta[-1], tb[-1], s=45, marker="x")

    axs[0].set_title("Symmetry Graph Energy Flow")
    axs[0].set_xlabel("phi_A")
    axs[0].set_ylabel("phi_B")
    axs[0].legend(fontsize=8, loc="upper right")
    plt.colorbar(contour, ax=axs[0], label="Energy")

    # Energy vs time
    for idx, (_, _, en) in enumerate(trajectories):
        axs[1].plot(en, linewidth=2, label=f"traj {idx+1}")

    axs[1].set_title("Energy Descent Along Trajectories")
    axs[1].set_xlabel("step")
    axs[1].set_ylabel("E")
    axs[1].legend(fontsize=8, loc="upper right")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nComputing symmetry graph energy flow...\n")

    X, Y, Z = build_landscape(
        n=220,
        K_hub=1.0,
        K_ring_a=0.7,
        K_ring_b=0.7,
        K_cross=0.25
    )

    print("Landscape shape:", Z.shape)
    print("Energy min:", float(np.min(Z)))
    print("Energy max:", float(np.max(Z)))

    trajectories = []

    for phi_a0, phi_b0 in default_initial_points():
        ta, tb, en = run_energy_flow(
            phi_a0,
            phi_b0,
            steps=320,
            dt=0.06,
            damping=1.0,
            noise=0.0,
            K_hub=1.0,
            K_ring_a=0.7,
            K_ring_b=0.7,
            K_cross=0.25
        )
        trajectories.append((ta, tb, en))

    plot_energy_flow(X, Y, Z, trajectories)
