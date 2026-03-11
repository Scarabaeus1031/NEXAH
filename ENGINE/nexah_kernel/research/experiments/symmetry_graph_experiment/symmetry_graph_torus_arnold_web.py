"""
NEXAH Symmetry Graph – Arnold Web on Torus
------------------------------------------

Draws resonance lines directly on the torus surface.

Resonance condition:

    n * phi_A - m * phi_B = const

These curves form the Arnold web of the phase system.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# torus geometry
# --------------------------------------------------

def torus(u, v, R=3, r=1):

    x = (R + r*np.cos(v))*np.cos(u)
    y = (R + r*np.cos(v))*np.sin(u)
    z = r*np.sin(v)

    return x, y, z


# --------------------------------------------------
# resonance curve
# --------------------------------------------------

def resonance_curve(n, m, const=0, points=800):

    phi = np.linspace(-np.pi, np.pi, points)

    a = phi
    b = (n*phi - const)/m

    return a, b


# --------------------------------------------------
# main
# --------------------------------------------------

def main():

    print("Drawing Arnold resonance web on torus...")

    grid = 120

    u = np.linspace(-np.pi, np.pi, grid)
    v = np.linspace(-np.pi, np.pi, grid)

    U, V = np.meshgrid(u, v)

    X, Y, Z = torus(U, V)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(
        X,
        Y,
        Z,
        color="lightgray",
        alpha=0.4,
        linewidth=0
    )


    # --------------------------------------------------
    # resonance families
    # --------------------------------------------------

    resonances = [
        (1,1),
        (2,1),
        (3,2),
        (5,3),
        (7,5)
    ]

    for n,m in resonances:

        a,b = resonance_curve(n,m)

        x,y,z = torus(a,b)

        ax.plot(
            x,
            y,
            z,
            linewidth=2,
            label=f"{n}:{m}"
        )


    ax.set_title("Arnold Resonance Web on Torus")

    plt.show()


# --------------------------------------------------

if __name__ == "__main__":
    main()
