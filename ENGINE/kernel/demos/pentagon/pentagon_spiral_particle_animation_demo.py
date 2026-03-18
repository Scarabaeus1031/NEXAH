"""
Pentagon Spiral Particle Animation Demo
======================================

Animated particle simulation inside the NEXAH spiral flow field.

The animation can optionally be saved as:

    GIF  (requires pillow)
    MP4  (requires ffmpeg)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Attractors
# --------------------------------------------------

attractors = {
    "Q1°": (-4, 0),
    "Q2°": (4, 0),
    "Q3°": (0, 4)
}

print("\nAttractors\n")
for name, pos in attractors.items():
    print(name, pos)


# --------------------------------------------------
# Parameters
# --------------------------------------------------

epsilon = 0.4
rotation_strength = 0.9

particles = 400
dt = 0.08

xmin, xmax = -6, 6
ymin, ymax = -6, 6


# --------------------------------------------------
# Initial particles
# --------------------------------------------------

x = np.random.uniform(xmin, xmax, particles)
y = np.random.uniform(ymin, ymax, particles)


# --------------------------------------------------
# Flow field
# --------------------------------------------------

def flow_field(x, y):

    U = np.zeros_like(x)
    V = np.zeros_like(y)

    for ax, ay in attractors.values():

        dx = x - ax
        dy = y - ay

        dist = np.sqrt(dx*dx + dy*dy) + epsilon

        U += -dx / dist**2
        V += -dy / dist**2

        U += -rotation_strength * dy / dist**2
        V +=  rotation_strength * dx / dist**2

    return U, V


# --------------------------------------------------
# Plot setup
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7,6))

scatter = ax.scatter(x, y, s=10)

for name,(axp,ayp) in attractors.items():

    ax.scatter(axp, ayp, marker="*", s=260)
    ax.text(axp+0.2, ayp+0.2, name)

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")

ax.set_title("NEXAH Spiral Particle Animation")


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
    frames=300,
    interval=40,
    blit=True
)

plt.show()


# --------------------------------------------------
# Optional export
# --------------------------------------------------

save_gif = False
save_mp4 = False

if save_gif:
    ani.save("nexah_spiral_particles.gif", writer="pillow", fps=30)

if save_mp4:
    ani.save("nexah_spiral_particles.mp4", writer="ffmpeg", fps=30)
    return U, V


# --------------------------------------------------
# Plot setup
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7,6))

scatter = ax.scatter(x, y, s=8)


for name, (axp, ayp) in attractors.items():

    ax.scatter(axp, ayp, marker="*", s=260)
    ax.text(axp+0.2, ayp+0.2, name)

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

ax.set_aspect("equal")

ax.set_title("NEXAH Spiral Particle Animation")
ax.set_xlabel("x")
ax.set_ylabel("y")


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
    frames=400,
    interval=40,
    blit=True
)

plt.show()
