"""
NEXAH Symmetry Graph – Basin Map
--------------------------------

Builds a basin-of-attraction map for the reduced resonance landscape.

Idea:
- use the reduced 2D phase model (phi_A, phi_B)
- evolve many initial points under negative gradient flow
- classify each start point by which attractor / minimum it reaches
- visualize the phase space as colored attraction basins

Model terms:
    1:1   hub synchronization
    2:1   cross resonance
    3:2   resonance split
    5:3   harmonic channel

Outputs:
- basin map
- energy contour overlay
- printed attractor summary
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

    dE_a = (
        K11 * np.sin(phi_a - phi_b)
        + K_ring_a * np.sin(phi_a)
        + 2 * K21 * np.sin(2 * phi_a - phi_b)
        + 3 * K32 * np.sin(3 * phi_a - 2 * phi_b)
        + 5 * K53 * np.sin(5 * phi_a - 3 * phi_b)
    )

    dE_b = (
        -K11 * np.sin(phi_a - phi_b)
        + K_ring_b * np.sin(phi_b)
        - K21 * np.sin(2 * phi_a - phi_b)
        - 2 * K32 * np.sin(3 * phi_a - 2 * phi_b)
        - 3 * K53 * np.sin(5 * phi_a - 3 * phi_b)
    )

    return dE_a, dE_b


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def angle_distance(a, b):
    d = abs(a - b)
    return min(d, 2*np.pi - d)


def torus_distance(a1, b1, a2, b2):
    da = angle_distance(a1, a2)
    db = angle_distance(b1, b2)
    return np.sqrt(da**2 + db**2)


# --------------------------------------------------
# Gradient flow
# --------------------------------------------------

def run_flow(phi_a0, phi_b0, steps=200, dt=0.05):

    phi_a = phi_a0
    phi_b = phi_b0

    for _ in range(steps):

        dEa, dEb = resonance_gradient(phi_a, phi_b)

        phi_a = phi_a - dt * dEa
        phi_b = phi_b - dt * dEb

        phi_a = wrap(phi_a)
        phi_b = wrap(phi_b)

    return phi_a, phi_b


# --------------------------------------------------
# Discover attractors
# --------------------------------------------------

def discover_attractors(grid=14):

    seeds = np.linspace(-np.pi, np.pi, grid)
    attractors = []

    for pa in seeds:
        for pb in seeds:

            fa, fb = run_flow(pa, pb)

            found = False
            for att in attractors:

                dist = torus_distance(fa, fb, att[0], att[1])

                if dist < 0.2:
                    found = True
                    break

            if not found:
                attractors.append((fa, fb))

    return attractors


# --------------------------------------------------
# Basin map
# --------------------------------------------------

def compute_basin_map(attractors, n=120):

    phi_vals = np.linspace(-np.pi, np.pi, n)

    basin = np.zeros((n, n))

    for i, pa in enumerate(phi_vals):
        for j, pb in enumerate(phi_vals):

            fa, fb = run_flow(pa, pb)

            best = None
            best_dist = 1e9

            for k, att in enumerate(attractors):

                dist = torus_distance(fa, fb, att[0], att[1])

                if dist < best_dist:
                    best_dist = dist
                    best = k

            basin[j, i] = best

    return phi_vals, basin


# --------------------------------------------------
# Energy background
# --------------------------------------------------

def build_energy_background(n=200):

    phi_vals = np.linspace(-np.pi, np.pi, n)
    X, Y = np.meshgrid(phi_vals, phi_vals)

    Z = resonance_energy(X, Y)

    return X, Y, Z


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_basin_map(phi_vals, basin, attractors, X, Y, Z):

    fig, axs = plt.subplots(1,2,figsize=(14,6))

    im = axs[0].imshow(
        basin,
        origin="lower",
        extent=[phi_vals[0],phi_vals[-1],phi_vals[0],phi_vals[-1]],
        interpolation="nearest"
    )

    axs[0].set_title("Basin Map")
    axs[0].set_xlabel("phi_A")
    axs[0].set_ylabel("phi_B")

    for i, att in enumerate(attractors):
        axs[0].scatter(att[0], att[1], color="white")
        axs[0].text(att[0], att[1], str(i))

    plt.colorbar(im, ax=axs[0])


    contour = axs[1].contourf(X, Y, Z, levels=40)
    axs[1].contour(X, Y, Z, levels=30, colors="black", linewidths=0.3)

    axs[1].set_title("Energy Landscape")
    axs[1].set_xlabel("phi_A")
    axs[1].set_ylabel("phi_B")

    plt.colorbar(contour, ax=axs[1])

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nComputing symmetry graph basin map...\n")

    attractors = discover_attractors()

    print("Detected attractors:", len(attractors))
    for i,a in enumerate(attractors):
        print(i, a)

    phi_vals, basin = compute_basin_map(attractors)

    X, Y, Z = build_energy_background()

    plot_basin_map(phi_vals, basin, attractors, X, Y, Z)
