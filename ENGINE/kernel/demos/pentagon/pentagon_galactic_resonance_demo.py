"""
Pentagon Galactic Resonance Demo
================================

This demo extends the pentagon ring spiral particle system by adding
a central attractor.

The resulting field combines:

1. five outer attractors arranged on a pentagon
2. one central attractor
3. attraction + rotational spiral flow

This produces galaxy-like resonance arms and central clustering.

Kernel idea:

    F(x,y) = outer attractors + central attractor + spiral rotation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Pentagon ring attractors
# --------------------------------------------------

radius = 4.5
num_attractors = 5

attractors = {}

for i in range(num_attractors):

    angle = 2 * np.pi * i / num_attractors + np.pi / 2

    x = radius * np.cos(angle)
    y = radius * np.sin(angle)

    attractors[f"Q{i+1}°"] = (x, y)


# central attractor
center_name = "Q°"
center_attractor = (0.0, 0.0)


print("\nOuter Attractors\n")
for name, pos in attractors.items():
    print(name, pos)

print("\nCentral Attractor\n")
print(center_name, center_attractor)


# --------------------------------------------------
# Parameters
# --------------------------------------------------

epsilon = 0.45
rotation_strength = 0.95

outer_weight = 1.0
center_weight = 1.6

particles = 700
dt = 0.07

xmin, xmax = -7, 7
ymin, ymax = -7, 7


# --------------------------------------------------
# Initial particle positions
# --------------------------------------------------

x = np.random.uniform(xmin, xmax, particles)
y = np.random.uniform(ymin, ymax, particles)


# --------------------------------------------------
# Flow field
# --------------------------------------------------

def flow_field(x, y):

    U = np.zeros_like(x)
    V = np.zeros_like(y)

    # outer pentagon attractors
    for ax, ay in attractors.values():

        dx = x - ax
        dy = y - ay

        dist = np.sqrt(dx * dx + dy * dy) + epsilon

        # attraction
        U += outer_weight * (-dx / dist**2)
        V += outer_weight * (-dy / dist**2)

        # spiral rotation
        U += outer_weight * (-rotation_strength * dy / dist**2)
        V += outer_weight * ( rotation_strength * dx / dist**2)

    # central attractor
    ax, ay = center_attractor

    dx = x - ax
    dy = y - ay

    dist = np.sqrt(dx * dx + dy * dy) + epsilon

    U += center_weight * (-dx / dist**2)
    V += center_weight * (-dy / dist**2)

    # softer central rotation for galaxy-style swirl
    U += 0.55 * (-dy / dist**2)
    V += 0.55 * ( dx / dist**2)

    return U, V


# --------------------------------------------------
# Plot setup
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 7))

scatter = ax.scatter(x, y, s=7)

# outer attractors
for name, (axp, ayp) in attractors.items():

    ax.scatter(axp, ayp, marker="*", s=260)
    ax.text(axp + 0.18, ayp + 0.18, name)

# center attractor
ax.scatter(center_attractor[0], center_attractor[1], marker="*", s=320)
ax.text(center_attractor[0] + 0.18, center_attractor[1] + 0.18, center_name)

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

ax.set_aspect("equal")
ax.set_title("NEXAH Pentagon Galactic Resonance")


# --------------------------------------------------
# Animation step
# --------------------------------------------------

def update(frame):

    global x, y

    U, V = flow_field(x, y)

    x = x + U * dt
    y = y + V * dt

    scatter.set_offsets(np.c_[x, y])

    return scatter,


ani = FuncAnimation(
    fig,
    update,
    frames=420,
    interval=40,
    blit=True
)

plt.show()
