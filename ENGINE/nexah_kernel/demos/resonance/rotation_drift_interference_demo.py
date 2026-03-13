"""
Rotation Drift Interference Demo
================================

This demo explores how rotational symmetry changes when a small
angular drift is added to an otherwise regular n-fold system.

Core idea:

    theta_k = k * (2*pi/n + drift)

This produces interference patterns such as:

- polygons
- rosettes
- spiral flowers
- quasi-periodic drift structures

The demo connects iterative angle systems with NEXAH-style
symmetry and resonance exploration.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# --------------------------------------------------
# Parameters
# --------------------------------------------------

n_symmetry = 5            # try: 5, 6, 7, 8, 9, 10, 12
drift_deg = 2.0           # angular drift in degrees
radius = 5.0

points_per_frame = 180
frames = 220

xmin, xmax = -6.5, 6.5
ymin, ymax = -6.5, 6.5


# --------------------------------------------------
# Derived values
# --------------------------------------------------

base_angle = 2 * np.pi / n_symmetry
drift = np.deg2rad(drift_deg)

print("\nRotation Drift Interference Demo\n")
print("n_symmetry =", n_symmetry)
print("base angle =", base_angle)
print("drift_deg  =", drift_deg)
print("effective angle =", base_angle + drift)


# --------------------------------------------------
# Plot setup
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 7))

line, = ax.plot([], [], lw=1.2, alpha=0.85)
pts = ax.scatter([], [], s=10)

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")

ax.set_title(
    f"Rotation Drift Interference  |  n={n_symmetry}, drift={drift_deg}°"
)
ax.set_xlabel("x")
ax.set_ylabel("y")


# faint guide circle
circle_t = np.linspace(0, 2*np.pi, 400)
ax.plot(radius*np.cos(circle_t), radius*np.sin(circle_t), alpha=0.12)


# symmetry guide rays
for i in range(n_symmetry):
    a = 2 * np.pi * i / n_symmetry
    ax.plot(
        [0, radius*np.cos(a)],
        [0, radius*np.sin(a)],
        linestyle="--",
        alpha=0.12
    )


# --------------------------------------------------
# State
# --------------------------------------------------

xs_all = []
ys_all = []


# --------------------------------------------------
# Animation update
# --------------------------------------------------

def update(frame):

    global xs_all, ys_all

    total_points = (frame + 1) * points_per_frame

    k = np.arange(total_points)

    theta = k * (base_angle + drift)

    # optional slow radial breathing for more visible structure
    r = radius * (0.65 + 0.35 * np.cos(k * 0.015))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    xs_all = x
    ys_all = y

    line.set_data(x, y)
    pts.set_offsets(np.c_[x[-800:], y[-800:]])

    return line, pts


ani = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=45,
    blit=True
)

plt.show()
