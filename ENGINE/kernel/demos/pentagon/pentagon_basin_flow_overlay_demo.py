"""
Pentagon Basin + Flow Overlay Demo
=================================

This demo overlays attractor basin regions with the
vector flow field.

The background shows which attractor dominates each
region of space, while streamlines show the dynamics
guiding trajectories toward the attractors.
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Attractors
# --------------------------------------------------

attractors = {
    "Q1°": (-4, 0),
    "Q2°": (4, 0),
    "Q3°": (0, 4)
}

print("\nAttractors\n")
for name,pos in attractors.items():
    print(name,pos)


# --------------------------------------------------
# Parameters
# --------------------------------------------------

epsilon = 0.4
rotation_strength = 0.9

xmin, xmax = -6, 6
ymin, ymax = -6, 6

resolution = 120


# --------------------------------------------------
# Grid
# --------------------------------------------------

xs = np.linspace(xmin, xmax, resolution)
ys = np.linspace(ymin, ymax, resolution)

X, Y = np.meshgrid(xs, ys)


# --------------------------------------------------
# Basin computation
# --------------------------------------------------

basin = np.zeros_like(X)

for i,(ax,ay) in enumerate(attractors.values(), start=1):

    dx = X - ax
    dy = Y - ay

    dist = np.sqrt(dx*dx + dy*dy)

    if i == 1:
        min_dist = dist
        basin[:] = i
    else:
        mask = dist < min_dist
        basin[mask] = i
        min_dist = np.minimum(min_dist, dist)


# --------------------------------------------------
# Flow field
# --------------------------------------------------

U = np.zeros_like(X)
V = np.zeros_like(Y)

for ax, ay in attractors.values():

    dx = X - ax
    dy = Y - ay

    dist = np.sqrt(dx*dx + dy*dy) + epsilon

    U += -dx / dist**2
    V += -dy / dist**2

    U += -rotation_strength * dy / dist**2
    V +=  rotation_strength * dx / dist**2


# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(7,6))

plt.imshow(
    basin,
    origin="lower",
    extent=[xmin,xmax,ymin,ymax],
    cmap="Pastel1",
    alpha=0.6
)

plt.streamplot(
    X, Y,
    U, V,
    density=1.5,
    linewidth=1
)

for name,(ax,ay) in attractors.items():

    plt.scatter(ax,ay,marker="*",s=260)
    plt.text(ax+0.2,ay+0.2,name)


plt.title("NEXAH Basin + Flow Overlay")
plt.xlabel("x")
plt.ylabel("y")

plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)

plt.gca().set_aspect("equal")

plt.tight_layout()
plt.show()
