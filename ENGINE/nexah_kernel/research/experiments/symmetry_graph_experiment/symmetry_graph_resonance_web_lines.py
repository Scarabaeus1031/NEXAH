"""
NEXAH Symmetry Graph – Resonance Web Lines
------------------------------------------

Draws analytical resonance lines of the form

    n * phi_A - m * phi_B = c

on top of the generated resonance landscape.

Goal:
- make the resonance web itself visible
- compare analytical line families with the numerical energy field
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Resonance generator
# --------------------------------------------------

def generate_resonances(max_n=6):

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
# Energy field
# --------------------------------------------------

def resonance_energy(phi_a, phi_b, resonances, base_strength=0.4):

    E = 0

    for (n, m) in resonances:

        strength = base_strength / (n + m)

        E += -strength * np.cos(n * phi_a - m * phi_b)

    return E


# --------------------------------------------------
# Landscape computation
# --------------------------------------------------

def compute_landscape(resonances, grid=200):

    phi = np.linspace(-np.pi, np.pi, grid)

    X, Y = np.meshgrid(phi, phi)

    E = resonance_energy(X, Y, resonances)

    return phi, X, Y, E


# --------------------------------------------------
# Draw resonance lines
# --------------------------------------------------

def draw_resonance_lines(ax, resonances, num_lines=6):

    phi = np.linspace(-np.pi, np.pi, 400)

    for (n, m) in resonances:

        for k in range(-num_lines, num_lines + 1):

            c = k * np.pi / 2

            phi_a = phi
            phi_b = (n * phi_a - c) / m

            mask = (phi_b >= -np.pi) & (phi_b <= np.pi)

            ax.plot(
                phi_a[mask],
                phi_b[mask],
                linewidth=0.8,
                alpha=0.4
            )


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_resonance_web(phi, X, Y, E, resonances):

    fig, ax = plt.subplots(figsize=(8,7))

    c = ax.contourf(X, Y, E, levels=40)

    plt.colorbar(c)

    draw_resonance_lines(ax, resonances)

    ax.set_xlabel("phi_A")
    ax.set_ylabel("phi_B")

    ax.set_title("Analytical Resonance Web")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nComputing analytical resonance web...\n")

    resonances = generate_resonances(max_n=6)

    print("Number of resonance families:", len(resonances))

    phi, X, Y, E = compute_landscape(resonances)

    print("Landscape shape:", E.shape)
    print("Energy min:", np.min(E))
    print("Energy max:", np.max(E))

    plot_resonance_web(phi, X, Y, E, resonances)


if __name__ == "__main__":
    main()
