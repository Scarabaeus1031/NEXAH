"""
NEXAH Symmetry Graph – Torus Resonance Nodes
--------------------------------------------

Detects resonance nodes (critical points) on the torus.

Idea:
Find points where the gradient of the resonance energy vanishes.

Outputs:
- torus energy field
- resonance nodes
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# energy
# --------------------------------------------------

def resonance_energy(a, b, c):

    return (
        -np.cos(a - b)
        -0.8 * np.cos(a - c)
        -0.8 * np.cos(b - c)
        -1.2 * np.cos(a + b - c)
    )


# --------------------------------------------------
# gradient
# --------------------------------------------------

def gradient(a, b, c):

    dA = (
        np.sin(a - b)
        + np.sin(a - c)
        + np.sin(a + b - c)
    )

    dB = (
        -np.sin(a - b)
        + np.sin(b - c)
        + np.sin(a + b - c)
    )

    dC = (
        -np.sin(a - c)
        -np.sin(b - c)
        -np.sin(a + b - c)
    )

    return dA, dB, dC


# --------------------------------------------------
# torus geometry
# --------------------------------------------------

def torus(u, v, R=3, r=1):

    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)

    return x, y, z


# --------------------------------------------------
# search nodes
# --------------------------------------------------

def find_nodes(grid=140):

    phi = np.linspace(-np.pi, np.pi, grid)

    nodes = []

    c = 0.7

    for a in phi:
        for b in phi:

            dA, dB, dC = gradient(a, b, c)

            g = np.sqrt(dA**2 + dB**2)

            if g < 0.02:
                nodes.append((a, b))

    return np.array(nodes)


# --------------------------------------------------
# main
# --------------------------------------------------

def main():

    print("Searching resonance nodes on torus...")

    grid = 140

    u = np.linspace(-np.pi, np.pi, grid)
    v = np.linspace(-np.pi, np.pi, grid)

    U, V = np.meshgrid(u, v)

    phi_c = 0.7

    E = resonance_energy(U, V, phi_c)

    X, Y, Z = torus(U, V)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    norm = (E - E.min()) / (E.max() - E.min())

    ax.plot_surface(
        X,
        Y,
        Z,
        facecolors=plt.cm.viridis(norm),
        linewidth=0,
        antialiased=True,
        alpha=0.85
    )

    nodes = find_nodes()

    print("Nodes found:", len(nodes))

    if len(nodes) > 0:

        a = nodes[:, 0]
        b = nodes[:, 1]

        x, y, z = torus(a, b)

        ax.scatter(
            x,
            y,
            z,
            color="red",
            s=40
        )

    ax.set_title("Resonance Nodes on Torus")

    plt.show()


# --------------------------------------------------

if __name__ == "__main__":
    main()
