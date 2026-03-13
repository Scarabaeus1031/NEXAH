"""
12-Fold Symmetry Center Attractor Demo
=====================================

This demo illustrates a dynamical field with

12-fold rotational symmetry
+ one central attractor.

Particles move under the influence of the outer symmetry
structure and the central attractor.

This produces characteristic radial resonance patterns.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Parameters
# --------------------------------------------------

radius = 4.8
rotation_strength = 0.75

outer_weight = 1.0
center_weight = 1.5

epsilon = 0.4

particles = 1000
dt = 0.05

xmin, xmax = -7, 7
ymin, ymax = -7, 7


# --------------------------------------------------
# Build 12-fold symmetry attractors
# --------------------------------------------------

outer = {}

for i in range(12):

    angle = 2 * np.pi * i / 12

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    outer[f"A{i+1}"] = (x, y)


center = (0.0, 0.0)


print("\nOuter attractors\n")

for name, pos in outer.items():
    print(name, pos)

print("\nCenter\n", center)


# --------------------------------------------------
# Initial particle distribution
# --------------------------------------------------

x = np.random.uniform(xmin, xmax, particles)
y = np.random.uniform(ymin, ymax, particles)


# --------------------------------------------------
# Flow field
# --------------------------------------------------

def flow(x, y):

    U = np.zeros_like(x)
    V = np.zeros_like(y)

    # Outer attractors
    for ax, ay in outer.values():

        dx = x - ax
        dy = y - ay

        d = np.sqrt(dx * dx + dy * dy) + epsilon

        U += outer_weight * (-dx / d**2)
        V += outer_weight * (-dy / d**2)

        # rotational component
        U += outer_weight * (-rotation_strength * dy / d**2)
        V += outer_weight * ( rotation_strength * dx / d**2)


    # Center attractor
    dx = x
    dy = y

    d = np.sqrt(dx * dx + dy * dy) + epsilon

    U += center_weight * (-dx / d**2)
    V += center_weight * (-dy / d**2)

    return U, V


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 7))

sc = ax.scatter(x, y, s=4)


for name, (px, py) in outer.items():

    ax.scatter(px, py, s=70)
    ax.text(px + 0.1, py + 0.1, name, fontsize=8)


ax.scatter(center[0], center[1], marker="*", s=300)


# radial guides

for i in range(12):

    angle = 2 * np.pi * i / 12

    x2 = 7 * np.cos(angle)
    y2 = 7 * np.sin(angle)

    ax.plot([0, x2], [0, y2], linestyle="--", alpha=0.15)


ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")

ax.set_title("12-Fold Symmetry + Center Attractor")


# --------------------------------------------------
# Animation
# --------------------------------------------------

def update(frame):

    global x, y

    U, V = flow(x, y)

    x = x + U * dt
    y = y + V * dt

    sc.set_offsets(np.c_[x, y])

    return sc,


ani = FuncAnimation(
    fig,
    update,
    frames=450,
    interval=40,
    blit=True
)

plt.show()
