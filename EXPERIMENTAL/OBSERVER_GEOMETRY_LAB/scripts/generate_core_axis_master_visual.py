# EXPERIMENTAL/scripts/generate_core_axis_master_visual.py

"""
NEXAH CORE AXIS GEOMETRY
Master Visualization Generator

This script generates a geometry-first visualization of:

- Core Axis / Q° reference spine
- Atwood-style reinjection loops
- Shell structures
- Aperture crossings
- Sphere → Drift → Fold → Tube transition
- Observer slice geometry
- Local ↔ Global relation fields

The goal is not physical proof,
but exploratory transport geometry visualization.

Author:
NEXAH / WHITE SERIES
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ------------------------------------------------------------
# OUTPUT STRUCTURE
# ------------------------------------------------------------

BASE_DIR = "EXPERIMENTAL"
SCRIPT_DIR = os.path.join(BASE_DIR, "scripts")
VISUAL_DIR = os.path.join(BASE_DIR, "visuals")

os.makedirs(SCRIPT_DIR, exist_ok=True)
os.makedirs(VISUAL_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(
    VISUAL_DIR,
    "core_axis_master_visual.png"
)


# ------------------------------------------------------------
# FIGURE SETUP
# ------------------------------------------------------------

fig = plt.figure(figsize=(14, 18), facecolor="black")
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor("black")

# Remove panes
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Remove grid
ax.grid(False)

# Remove ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Transparent panes
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.set_edgecolor('black')
ax.zaxis.pane.set_edgecolor('black')


# ------------------------------------------------------------
# CORE AXIS (Q° / C0)
# ------------------------------------------------------------

z_axis = np.linspace(-12, 12, 500)
x_axis = np.zeros_like(z_axis)
y_axis = np.zeros_like(z_axis)

ax.plot(
    x_axis,
    y_axis,
    z_axis,
    color="white",
    linewidth=3,
    alpha=0.95,
    label="Q° Core Axis"
)


# ------------------------------------------------------------
# SHELL STRUCTURES
# ------------------------------------------------------------

theta = np.linspace(0, 2*np.pi, 400)

for radius, z in zip(
    [2.5, 4.0, 5.5, 7.0],
    [-7, -2, 3, 8]
):
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z_shell = np.ones_like(theta) * z

    ax.plot(
        x,
        y,
        z_shell,
        color="#00d9ff",
        linewidth=1.2,
        alpha=0.35
    )


# ------------------------------------------------------------
# ATWOOD-STYLE REINJECTION LOOPS
# ------------------------------------------------------------

t = np.linspace(0, 18*np.pi, 4000)

x = (
    4*np.sin(t)
    + 0.8*np.sin(3*t)
)

y = (
    2.5*np.cos(t)
    + 0.5*np.cos(5*t)
)

z = (
    0.12*t
    + 2*np.sin(0.35*t)
)

ax.plot(
    x,
    y,
    z - 10,
    color="#ffd166",
    linewidth=1.4,
    alpha=0.85
)

# mirrored reinjection branch
ax.plot(
    -x,
    -y,
    z - 10,
    color="#ff4f81",
    linewidth=1.1,
    alpha=0.55
)


# ------------------------------------------------------------
# SPHERE → DRIFT → FOLD → TUBE
# ------------------------------------------------------------

t2 = np.linspace(0, 10*np.pi, 2500)

r = np.linspace(6, 1.5, len(t2))

x2 = r * np.cos(t2)
y2 = r * np.sin(t2)

z2 = np.linspace(-10, 10, len(t2))

ax.plot(
    x2,
    y2,
    z2,
    color="#a855f7",
    linewidth=1.2,
    alpha=0.7
)


# ------------------------------------------------------------
# APERTURE REGIONS
# ------------------------------------------------------------

aperture_z = [-6, 0, 6]

for z0 in aperture_z:

    theta_a = np.linspace(0, 2*np.pi, 200)

    radius = 1.2

    x_a = radius*np.cos(theta_a)
    y_a = radius*np.sin(theta_a)
    z_a = np.ones_like(theta_a)*z0

    ax.plot(
        x_a,
        y_a,
        z_a,
        color="white",
        linewidth=2.2,
        alpha=0.9
    )


# ------------------------------------------------------------
# OBSERVER SLICE PLANES
# ------------------------------------------------------------

plane_z = [-4, 4]

for pz in plane_z:

    xx = np.linspace(-8, 8, 30)
    yy = np.linspace(-8, 8, 30)

    XX, YY = np.meshgrid(xx, yy)
    ZZ = np.ones_like(XX) * pz

    ax.plot_surface(
        XX,
        YY,
        ZZ,
        color="#ffffff",
        alpha=0.03,
        linewidth=0
    )


# ------------------------------------------------------------
# LOCAL CORRIDOR TRAJECTORIES
# ------------------------------------------------------------

for phase in np.linspace(0, 2*np.pi, 6):

    t3 = np.linspace(0, 8*np.pi, 1200)

    x3 = 1.8*np.sin(t3 + phase)
    y3 = 1.8*np.cos(2*t3 + phase)

    z3 = np.linspace(-8, 8, len(t3))

    ax.plot(
        x3,
        y3,
        z3,
        color="#00ffb3",
        linewidth=0.8,
        alpha=0.18
    )


# ------------------------------------------------------------
# TITLE & TEXT
# ------------------------------------------------------------

fig.text(
    0.5,
    0.95,
    "NEXAH CORE AXIS GEOMETRY",
    color="white",
    fontsize=22,
    ha="center",
    family="monospace"
)

fig.text(
    0.5,
    0.92,
    "Observer Reference Axes • Aperture Transport • Reinjection Geometry",
    color="#cccccc",
    fontsize=11,
    ha="center"
)

fig.text(
    0.5,
    0.05,
    "The observer navigates slices of globally connected transport structure.",
    color="#bbbbbb",
    fontsize=10,
    ha="center"
)


# ------------------------------------------------------------
# CAMERA
# ------------------------------------------------------------

ax.view_init(
    elev=18,
    azim=36
)

ax.set_xlim(-9, 9)
ax.set_ylim(-9, 9)
ax.set_zlim(-12, 12)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH,
    dpi=300,
    facecolor="black",
    bbox_inches="tight"
)

print(f"[OK] Saved master visual to: {OUTPUT_PATH}")

plt.close()
