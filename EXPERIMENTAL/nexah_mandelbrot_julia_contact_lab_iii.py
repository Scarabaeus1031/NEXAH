# ============================================================
# NEXAH_BREATHING_MACHINE.py
#
# THE BREATHING MACHINE
# OVAL • PRIME GRID • PM/VM • Lissajous Gate • Observer • Emergence
#
# Run:
#   pip install numpy matplotlib pillow
#   python NEXAH_BREATHING_MACHINE.py
#
# Output:
#   nexah_breathing_machine.gif
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Ellipse, Circle
from matplotlib.collections import LineCollection

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

FPS = 30
FRAMES = 320

BG = "#020611"

CYAN = "#4deaff"
GOLD = "#ffd34d"
MAGENTA = "#ff4df0"
ORANGE = "#ffb347"
PURPLE = "#b266ff"
WHITE = "#f4f4f4"

np.random.seed(4)

# ------------------------------------------------------------
# FIGURE
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10), facecolor=BG)

ax.set_facecolor(BG)
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)

ax.set_xticks([])
ax.set_yticks([])

for s in ax.spines.values():
    s.set_visible(False)

# ------------------------------------------------------------
# ROOT-2 BACKGROUND FIELD
# ------------------------------------------------------------

x = np.linspace(-8, 8, 1200)
y = np.linspace(-8, 8, 1200)

X, Y = np.meshgrid(x, y)

# ROOT2 carrier
Z = np.sin(
    (X * np.sqrt(2) * 1.7)
    + np.sin(Y * 0.7)
)

bg = ax.imshow(
    Z,
    extent=[-8, 8, -8, 8],
    cmap="gray",
    alpha=0.10,
    origin="lower"
)

# ------------------------------------------------------------
# OVAL CONTAINMENT
# ------------------------------------------------------------

oval = Ellipse(
    (0, 0),
    width=10,
    height=14,
    edgecolor=CYAN,
    linewidth=2.5,
    fill=False,
    alpha=0.95
)

ax.add_patch(oval)

inner_oval = Ellipse(
    (0, 0),
    width=7,
    height=10,
    edgecolor=WHITE,
    linewidth=1.2,
    fill=False,
    alpha=0.25
)

ax.add_patch(inner_oval)

# ------------------------------------------------------------
# PRIME GRID
# ------------------------------------------------------------

grid_points = []

rings = [1.2, 2.1, 3.0, 3.9, 4.8]

for ridx, r in enumerate(rings):

    n = 12 + ridx * 8

    for k in range(n):

        a = 2 * np.pi * k / n

        px = r * np.cos(a)
        py = r * np.sin(a)

        grid_points.append([px, py])

grid_points = np.array(grid_points)

grid_scatter = ax.scatter(
    grid_points[:, 0],
    grid_points[:, 1],
    s=18,
    color=GOLD,
    alpha=0.85
)

# ------------------------------------------------------------
# PRIME CONNECTIONS
# ------------------------------------------------------------

segments = []

for i in range(0, len(grid_points), 2):

    j = (i * 7 + 13) % len(grid_points)

    segments.append([
        grid_points[i],
        grid_points[j]
    ])

lc = LineCollection(
    segments,
    colors=[(0.2, 1, 1, 0.07)],
    linewidths=0.6
)

ax.add_collection(lc)

# ------------------------------------------------------------
# CORE
# ------------------------------------------------------------

core = Circle(
    (0, 0),
    radius=0.75,
    facecolor=GOLD,
    edgecolor="none",
    alpha=0.95
)

ax.add_patch(core)

core_glow = Circle(
    (0, 0),
    radius=1.8,
    facecolor=ORANGE,
    edgecolor="none",
    alpha=0.06
)

ax.add_patch(core_glow)

# ------------------------------------------------------------
# OBSERVER / Q0
# ------------------------------------------------------------

observer_x = -7.2
observer_y = 6.5

observer = Circle(
    (observer_x, observer_y),
    radius=0.42,
    facecolor=WHITE,
    edgecolor="none",
    alpha=0.95
)

ax.add_patch(observer)

# injection line
inj_line, = ax.plot(
    [],
    [],
    color="#00ffd5",
    linewidth=2.0,
    alpha=0.85
)

# ------------------------------------------------------------
# PM / VM CARRIERS
# ------------------------------------------------------------

carrier_x = np.linspace(-7, 7, 1500)

pm_line, = ax.plot(
    [],
    [],
    color=ORANGE,
    linewidth=2.6,
    alpha=0.95
)

vm_line, = ax.plot(
    [],
    [],
    color=MAGENTA,
    linewidth=2.6,
    alpha=0.95
)

# ------------------------------------------------------------
# Lissajous Gate
# ------------------------------------------------------------

liss_line, = ax.plot(
    [],
    [],
    color=PURPLE,
    linewidth=1.6,
    alpha=0.9
)

# ------------------------------------------------------------
# 13-PULSE RING
# ------------------------------------------------------------

pulse_dots = ax.scatter([], [], s=20)

# ------------------------------------------------------------
# LABELS
# ------------------------------------------------------------

ax.text(
    0,
    7.5,
    "NEXAH — THE BREATHING MACHINE",
    color=WHITE,
    fontsize=24,
    ha="center",
    fontweight="bold"
)

ax.text(
    0,
    6.8,
    "OVAL • PRIME GRID • PM/VM • GATE • CORE • Q0",
    color=CYAN,
    fontsize=11,
    ha="center"
)

ax.text(
    0,
    -7.3,
    "containment • reflection • emergence • breathing",
    color=MAGENTA,
    fontsize=11,
    ha="center"
)

# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------

def animate(frame):

    t = frame / 18.0

    # --------------------------------------------------------
    # ROOT FIELD DRIFT
    # --------------------------------------------------------

    drift = np.sin(
        (X * np.sqrt(2) * 1.7)
        + np.sin(Y * 0.7 + t * 0.3)
        + t * 0.15
    )

    bg.set_array(drift)

    # --------------------------------------------------------
    # OVAL BREATHING
    # --------------------------------------------------------

    breath = 1 + 0.03 * np.sin(t)

    oval.width = 10 * breath
    oval.height = 14 * breath

    inner_oval.width = 7 * (1 + 0.02 * np.cos(t * 1.3))
    inner_oval.height = 10 * (1 + 0.02 * np.cos(t * 1.3))

    # --------------------------------------------------------
    # PRIME GRID VIBRATION
    # --------------------------------------------------------

    pts = []

    for i, (gx, gy) in enumerate(grid_points):

        a = np.arctan2(gy, gx)

        wobble = 0.05 * np.sin(t * 2 + i * 0.15)

        px = gx + wobble * np.cos(a)
        py = gy + wobble * np.sin(a)

        pts.append([px, py])

    pts = np.array(pts)

    grid_scatter.set_offsets(pts)

    # --------------------------------------------------------
    # INJECTION LINE
    # --------------------------------------------------------

    inj_x = np.sin(t * 0.8) * 0.3
    inj_y = np.cos(t * 0.7) * 0.3

    inj_line.set_data(
        [observer_x, inj_x],
        [observer_y, inj_y]
    )

    # --------------------------------------------------------
    # PM / VM
    # --------------------------------------------------------

    pm = (
        1.6 * np.sin(carrier_x * 0.9 + t)
        + 0.5 * np.sin(carrier_x * 4.5 - t * 2)
        + 0.2 * np.sin(carrier_x * 11 + t * 3)
    )

    # delayed mirrored memory field
    vm = (
        -1.6 * np.sin(carrier_x * 0.9 + t - 0.85)
        + 0.5 * np.sin(carrier_x * 4.5 + t * 1.4)
        - 0.2 * np.sin(carrier_x * 11 - t * 2)
    )

    pm_line.set_data(carrier_x, pm)
    vm_line.set_data(carrier_x, vm)

    # --------------------------------------------------------
    # Lissajous Gate
    # --------------------------------------------------------

    th = np.linspace(0, 2*np.pi, 900)

    delta = np.pi/2 + 0.25*np.sin(t * 0.6)

    lx = 1.3 * np.sin(3 * th + delta)
    ly = 1.3 * np.sin(2 * th)

    liss_line.set_data(lx, ly)

    # --------------------------------------------------------
    # 13-PULSE
    # --------------------------------------------------------

    pulse_pts = []

    pulse_cols = []

    for k in range(13):

        a = 2 * np.pi * k / 13 + t * 0.15

        rr = 1.2 + 0.12 * np.sin(t * 2 + k)

        px = rr * np.cos(a)
        py = rr * np.sin(a)

        pulse_pts.append([px, py])

        glow = 0.4 + 0.6 * (
            0.5 + 0.5*np.sin(t * 4 + k)
        )

        pulse_cols.append((1, 0.8, 0.3, glow))

    pulse_dots.set_offsets(np.array(pulse_pts))
    pulse_dots.set_color(pulse_cols)

    return (
        bg,
        grid_scatter,
        pm_line,
        vm_line,
        liss_line,
        pulse_dots,
        inj_line
    )

# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

anim = FuncAnimation(
    fig,
    animate,
    frames=FRAMES,
    interval=1000/FPS,
    blit=False
)

writer = PillowWriter(fps=FPS)

anim.save(
    "nexah_breathing_machine.gif",
    writer=writer
)

print("Saved:")
print("nexah_breathing_machine.gif")
