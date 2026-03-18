"""
N-Fold Symmetry Explorer Demo
=============================

This demo allows exploration of rotational symmetry systems
with an arbitrary number of attractors.

The system generates n attractors arranged on a circle
plus a central attractor.

Adjust parameter:

    n_symmetry

to explore different symmetry regimes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Adjustable symmetry parameter
# --------------------------------------------------

n_symmetry = 9     # try: 3..20


# --------------------------------------------------
# Parameters
# --------------------------------------------------

radius = 4.5
rotation_strength = 0.75

outer_weight = 1.0
center_weight = 1.4

epsilon = 0.4

particles = 1000
dt = 0.05

xmin, xmax = -7, 7
ymin, ymax = -7, 7


# --------------------------------------------------
# Build attractors
# --------------------------------------------------

outer = {}

for i in range(n_symmetry):

    angle = 2 * np.pi * i / n_symmetry

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    outer[f"A{i+1}"] = (x, y)


center = (0.0, 0.0)


print("\nSymmetry order:", n_symmetry)
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

    for ax, ay in outer.values():

        dx = x - ax
        dy = y - ay

        d = np.sqrt(dx*dx + dy*dy) + epsilon

        U += outer_weight * (-dx / d**2)
        V += outer_weight * (-dy / d**2)

        U += outer_weight * (-rotation_strength * dy / d**2)
        V += outer_weight * ( rotation_strength * dx / d**2)


    # center attractor
    dx = x
    dy = y

    d = np.sqrt(dx*dx + dy*dy) + epsilon

    U += center_weight * (-dx / d**2)
    V += center_weight * (-dy / d**2)

    return U, V


# --------------------------------------------------
# Plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7,7))

sc = ax.scatter(x, y, s=4)

for name,(px,py) in outer.items():

    ax.scatter(px, py, s=70)
    ax.text(px+0.1, py+0.1, name, fontsize=8)

ax.scatter(center[0], center[1], marker="*", s=300)


# radial guides
for i in range(n_symmetry):

    angle = 2*np.pi*i/n_symmetry

    x2 = 7*np.cos(angle)
    y2 = 7*np.sin(angle)

    ax.plot([0,x2],[0,y2], linestyle="--", alpha=0.15)


ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")

ax.set_title(f"{n_symmetry}-Fold Symmetry Field")


# --------------------------------------------------
# Animation
# --------------------------------------------------

def update(frame):

    global x, y

    U, V = flow(x, y)

    x = x + U * dt
    y = y + V * dt

    sc.set_offsets(np.c_[x,y])

    return sc,


ani = FuncAnimation(
    fig,
    update,
    frames=450,
    interval=40,
    blit=True
)

plt.show()
