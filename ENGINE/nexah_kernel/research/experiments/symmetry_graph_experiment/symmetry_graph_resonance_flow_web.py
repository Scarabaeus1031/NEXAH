"""
NEXAH Symmetry Graph – Resonance Flow Web
-----------------------------------------

Simulates gradient-flow trajectories through an automatically generated
resonance landscape.

Energy:
    E = Σ cos(n φA − m φB)

Trajectories follow negative gradient of the energy.

Outputs:
- energy landscape
- flow vector field
- resonance trajectories
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Resonance generator
# --------------------------------------------------

def generate_resonances(max_n=8):

    resonances = []

    for n in range(1, max_n + 1):
        for m in range(1, max_n + 1):

            if n == m:
                continue

            g = np.gcd(n, m)

            n_r = n // g
            m_r = m // g

            if (n_r, m_r) not in resonances:
                resonances.append((n_r, m_r))

    return resonances


# --------------------------------------------------
# Energy
# --------------------------------------------------

def resonance_energy(phi_a, phi_b, resonances, base_strength=0.4):

    E = 0.0

    for (n, m) in resonances:

        strength = base_strength / (n + m)

        E += -strength * np.cos(n * phi_a - m * phi_b)

    return E


# --------------------------------------------------
# Gradient
# --------------------------------------------------

def resonance_gradient(phi_a, phi_b, resonances, base_strength=0.4):

    dA = 0.0
    dB = 0.0

    for (n, m) in resonances:

        strength = base_strength / (n + m)

        angle = n * phi_a - m * phi_b

        dA += strength * n * np.sin(angle)
        dB += -strength * m * np.sin(angle)

    return dA, dB


# --------------------------------------------------
# Compute landscape
# --------------------------------------------------

def compute_landscape(resonances, grid=220):

    phi = np.linspace(-np.pi, np.pi, grid)

    X, Y = np.meshgrid(phi, phi)

    E = resonance_energy(X, Y, resonances)

    dA, dB = resonance_gradient(X, Y, resonances)

    return phi, X, Y, E, dA, dB


# --------------------------------------------------
# Flow simulation
# --------------------------------------------------

def simulate_trajectory(start, resonances, steps=250, dt=0.04):

    phi_a, phi_b = start

    traj = []

    for _ in range(steps):

        dA, dB = resonance_gradient(phi_a, phi_b, resonances)

        phi_a -= dt * dA
        phi_b -= dt * dB

        # wrap phases
        phi_a = (phi_a + np.pi) % (2*np.pi) - np.pi
        phi_b = (phi_b + np.pi) % (2*np.pi) - np.pi

        traj.append((phi_a, phi_b))

    return np.array(traj)


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_flow(phi, X, Y, E, dA, dB, resonances):

    fig, ax = plt.subplots(figsize=(8,7))

    c = ax.contourf(X, Y, E, levels=40)

    plt.colorbar(c)

    # vector field
    step = 10
    ax.quiver(
        X[::step,::step],
        Y[::step,::step],
        -dA[::step,::step],
        -dB[::step,::step],
        color="black",
        alpha=0.5
    )

    # trajectories
    starts = [
        (-2.5,-2.5),
        (-1.5,2.0),
        (1.5,-2.0),
        (2.0,2.0),
        (-2.0,1.0),
        (1.0,-1.5)
    ]

    for s in starts:

        traj = simulate_trajectory(s, resonances)

        ax.plot(traj[:,0], traj[:,1], linewidth=2)

        ax.scatter(s[0], s[1], s=40)

    ax.set_xlabel("phi_A")
    ax.set_ylabel("phi_B")
    ax.set_title("Resonance Flow Web")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nComputing resonance flow web...\n")

    resonances = generate_resonances(max_n=8)

    print("Number of resonance channels:", len(resonances))

    phi, X, Y, E, dA, dB = compute_landscape(resonances)

    print("Landscape shape:", E.shape)

    print("Energy min:", np.min(E))
    print("Energy max:", np.max(E))

    plot_flow(phi, X, Y, E, dA, dB, resonances)


if __name__ == "__main__":
    main()
