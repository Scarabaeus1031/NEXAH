"""
Symmetry Phase Map Generator
============================

Creates a phase map of symmetry vs rotational drift.

x-axis  → symmetry order n
y-axis  → drift angle

Each cell shows the resulting resonance pattern.
"""

import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# configuration
# --------------------------------------------------

radius = 5
iterations = 1500

n_values = range(3, 15)        # symmetry orders
drift_values = np.linspace(0, 6, 8)  # drift angles (degrees)

# --------------------------------------------------
# pattern generator
# --------------------------------------------------

def generate_pattern(n, drift_deg):

    base_angle = 2*np.pi/n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k * (base_angle + drift)

    r = radius * (0.7 + 0.3*np.cos(k*0.02))

    x = r*np.cos(theta)
    y = r*np.sin(theta)

    return x, y


# --------------------------------------------------
# plot grid
# --------------------------------------------------

rows = len(drift_values)
cols = len(n_values)

fig, axes = plt.subplots(rows, cols, figsize=(cols*2.2, rows*2.2))

for i, drift in enumerate(drift_values):
    for j, n in enumerate(n_values):

        ax = axes[i, j]

        x, y = generate_pattern(n, drift)

        ax.plot(x, y, lw=0.5)

        ax.set_xlim(-6,6)
        ax.set_ylim(-6,6)
        ax.set_aspect("equal")

        ax.axis("off")

        if i == 0:
            ax.set_title(f"n={n}", fontsize=9)

        if j == 0:
            ax.text(-7.5, 0, f"{drift:.1f}°",
                    rotation=90,
                    va="center",
                    fontsize=9)

plt.suptitle("Symmetry Phase Map (n vs Drift)", fontsize=14)

plt.tight_layout()
plt.show()
