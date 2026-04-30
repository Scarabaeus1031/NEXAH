"""
NEXAH KAM Surface Plot
======================

Visualizes a KAM-like torus surface generated from the NEXAH kernel.

This is a geometric summary plot for quasiperiodic / near-integrable
parameter regimes.

Output
------
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/kam_surface_plot.png
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/kam_surface_plot.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# NEXAH angular dynamics
# --------------------------------------------------

def step(theta, n, drift):
    return (theta + (2 * np.pi) / n + np.deg2rad(drift)) % (2 * np.pi)


# --------------------------------------------------
# Simulate torus-like orbit
# --------------------------------------------------

def simulate_torus(n=7, drift=1.3, steps=6000):
    theta = 0.12345
    points = []

    for k in range(steps):
        theta = step(theta, n, drift)

        # second slow angle for torus embedding
        phi = 0.017 * k

        # torus radii
        R = 2.8
        r = 0.9 + 0.08 * np.cos(theta * 3.0)

        x = (R + r * np.cos(theta)) * np.cos(phi)
        y = (R + r * np.cos(theta)) * np.sin(phi)
        z = r * np.sin(theta)

        points.append((x, y, z))

    return np.array(points)


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_surface():
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    test_cases = [
        (5, 0.2),
        (7, 1.3),
        (9, 2.0),
    ]

    for n, drift in test_cases:
        pts = simulate_torus(n=n, drift=drift, steps=4000)

        ax.plot(
            pts[:, 0],
            pts[:, 1],
            pts[:, 2],
            linewidth=0.7,
            alpha=0.85,
            label=f"n={n}, drift={drift}"
        )

    ax.set_title("NEXAH KAM Surface Plot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.legend()

    plt.tight_layout()
    plt.savefig(OUT_IMG, dpi=300)

    print("\nSaved KAM surface plot:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    print("\nGenerating NEXAH KAM surface plot...\n")
    plot_surface()


if __name__ == "__main__":
    main()
