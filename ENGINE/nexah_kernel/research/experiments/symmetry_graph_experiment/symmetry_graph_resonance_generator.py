"""
NEXAH Symmetry Graph – Resonance Generator
------------------------------------------

Generates extended resonance landscapes using automatic resonance terms.

Base idea:
Energy = sum of resonance channels

    cos(n φA − m φB)

This allows exploration of higher-order resonance structures.

Example channels:
    1:1
    2:1
    3:2
    5:3
    6:5
    7:4
    8:5
    ...

Outputs:
- generated resonance list
- energy landscape
- resonance web visualization
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

            # avoid duplicates like 2:2 etc
            g = np.gcd(n, m)

            n_r = n // g
            m_r = m // g

            if (n_r, m_r) not in resonances:
                resonances.append((n_r, m_r))

    return resonances


# --------------------------------------------------
# Energy function
# --------------------------------------------------

def resonance_energy(phi_a, phi_b, resonances, base_strength=0.4):

    E = 0.0

    for (n, m) in resonances:

        # weaker coupling for higher order resonances
        strength = base_strength / (n + m)

        E += -strength * np.cos(n * phi_a - m * phi_b)

    return E


# --------------------------------------------------
# Compute landscape
# --------------------------------------------------

def compute_landscape(resonances, grid=220):

    phi = np.linspace(-np.pi, np.pi, grid)

    X, Y = np.meshgrid(phi, phi)

    E = resonance_energy(X, Y, resonances)

    return phi, X, Y, E


# --------------------------------------------------
# Plot resonance web
# --------------------------------------------------

def plot_resonance_landscape(phi, X, Y, E, resonances):

    plt.figure(figsize=(8,7))

    c = plt.contourf(X, Y, E, levels=40)

    plt.colorbar(c)

    plt.xlabel("phi_A")
    plt.ylabel("phi_B")

    plt.title("Generated Resonance Landscape")

    plt.tight_layout()
    plt.show()

    print("\nResonance channels used:\n")

    for r in resonances:
        print(f"{r[0]} : {r[1]}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nGenerating resonance system...\n")

    resonances = generate_resonances(max_n=8)

    print("Number of resonance channels:", len(resonances))

    phi, X, Y, E = compute_landscape(resonances)

    print("Landscape shape:", E.shape)

    print("Energy min:", np.min(E))
    print("Energy max:", np.max(E))

    plot_resonance_landscape(phi, X, Y, E, resonances)


if __name__ == "__main__":
    main()
