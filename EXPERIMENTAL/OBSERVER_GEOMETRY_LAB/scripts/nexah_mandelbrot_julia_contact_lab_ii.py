# NEXAH_BIG_5_PLUS_1.py
# ---------------------------------------------------------
# BIG 5 +1
#
# 1. OVAL       -> containment / time shell
# 2. PRIME GRID -> discrete resonance lattice
# 3. CORRIDOR   -> transport / transition flow
# 4. GATE       -> bifurcation aperture
# 5. CORE       -> stability attractor ("Dotter")
# +1 OBSERVER   -> external pole / Q0
#
# Run:
# python NEXAH_BIG_5_PLUS_1.py
#
# Creates:
# nexah_big5plus1.png
#
# ---------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
from pathlib import Path

OUT = Path("nexah_big5plus1.png")

# ---------------------------------------------------------
# STYLE
# ---------------------------------------------------------

BG = "#05070d"

CYAN = "#5ef2ff"
TEAL = "#00d0aa"
GOLD = "#ffcc55"
MAGENTA = "#ff4fd8"
PURPLE = "#8f6bff"
WHITE = "#e8f0ff"

GRID = "#1a2330"

# ---------------------------------------------------------
# FIGURE
# ---------------------------------------------------------

fig = plt.figure(figsize=(14, 14), facecolor=BG)
ax = fig.add_subplot(111)

ax.set_facecolor(BG)
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)

ax.set_xticks([])
ax.set_yticks([])

for s in ax.spines.values():
    s.set_visible(False)

# ---------------------------------------------------------
# 1. OVAL
# ---------------------------------------------------------

oval_outer = Ellipse(
    (0, 0),
    width=12,
    height=18,
    edgecolor=CYAN,
    facecolor="none",
    lw=2.5,
    alpha=0.9
)

oval_inner = Ellipse(
    (0, 0),
    width=9,
    height=14,
    edgecolor=WHITE,
    facecolor="none",
    lw=1.2,
    alpha=0.35
)

ax.add_patch(oval_outer)
ax.add_patch(oval_inner)

# subtle shell layers

for i in range(1, 8):
    shell = Ellipse(
        (0, 0),
        width=12 - i * 0.7,
        height=18 - i * 1.0,
        edgecolor=CYAN,
        facecolor="none",
        lw=0.5,
        alpha=0.07
    )
    ax.add_patch(shell)

# ---------------------------------------------------------
# 2. PRIME GRID
# ---------------------------------------------------------

np.random.seed(4)

prime_angles = np.linspace(0, 2*np.pi, 29, endpoint=False)

nodes = []

for r in np.linspace(1.5, 5.5, 5):

    for i, theta in enumerate(prime_angles):

        modulation = 0.25 * np.sin(i * 2/9)
        rr = r + modulation

        x = rr * np.cos(theta)
        y = rr * np.sin(theta)

        nodes.append((x, y))

        ax.scatter(
            x,
            y,
            s=18,
            color=GOLD,
            alpha=0.85
        )

# lattice connections

for i in range(len(nodes)-1):

    x1, y1 = nodes[i]
    x2, y2 = nodes[(i+7) % len(nodes)]

    ax.plot(
        [x1, x2],
        [y1, y2],
        color=CYAN,
        lw=0.35,
        alpha=0.15
    )

# ---------------------------------------------------------
# 3. CORRIDOR
# ---------------------------------------------------------

t = np.linspace(-8, 8, 1200)

x = t

y = (
    1.8*np.sin(2*np.pi*(2/9)*t)
    + 0.8*np.sin(2*np.pi*(4/7)*t)
    + 0.35*np.sin(2*np.pi*(13/8)*t)
)

ax.plot(
    x,
    y,
    color=MAGENTA,
    lw=2.5,
    alpha=0.95
)

# corridor glow

for k in range(1, 8):

    ax.plot(
        x,
        y,
        color=MAGENTA,
        lw=2 + k,
        alpha=0.02
    )

# ---------------------------------------------------------
# 4. GATE
# ---------------------------------------------------------

gate_x = 0
gate_y = 0

gate = Circle(
    (gate_x, gate_y),
    radius=1.4,
    edgecolor=WHITE,
    facecolor="none",
    lw=2,
    alpha=0.7
)

ax.add_patch(gate)

# gate petals

petal_angles = np.linspace(0, 2*np.pi, 8, endpoint=False)

for th in petal_angles:

    px = 2.1 * np.cos(th)
    py = 2.1 * np.sin(th)

    ax.plot(
        [0, px],
        [0, py],
        color=PURPLE,
        lw=1.2,
        alpha=0.55
    )

# ---------------------------------------------------------
# 5. CORE
# ---------------------------------------------------------

core = Circle(
    (0, 0),
    radius=0.8,
    facecolor=GOLD,
    edgecolor="none",
    alpha=0.95
)

ax.add_patch(core)

# core glow

for r in np.linspace(1.2, 4.5, 14):

    glow = Circle(
        (0, 0),
        radius=r,
        facecolor=GOLD,
        edgecolor="none",
        alpha=0.015
    )

    ax.add_patch(glow)

# ---------------------------------------------------------
# +1 OBSERVER / Q0
# ---------------------------------------------------------

observer_x = -9.5
observer_y = 8.5

observer = Circle(
    (observer_x, observer_y),
    radius=0.5,
    facecolor=WHITE,
    edgecolor="none",
    alpha=0.95
)

ax.add_patch(observer)

# line toward system

ax.plot(
    [observer_x, 0],
    [observer_y, 0],
    color=WHITE,
    lw=1.2,
    alpha=0.3,
    linestyle="--"
)

# ---------------------------------------------------------
# AXES / DRIFT
# ---------------------------------------------------------

ax.axhline(
    0,
    color=CYAN,
    lw=0.8,
    alpha=0.18
)

ax.axvline(
    0,
    color=CYAN,
    lw=0.8,
    alpha=0.18
)

# golden-angle drift

golden_angle = np.deg2rad(137.5)

ax.plot(
    [0, 9*np.cos(golden_angle)],
    [0, 9*np.sin(golden_angle)],
    color=TEAL,
    lw=2,
    alpha=0.8
)

# counter vector

counter_angle = np.deg2rad(222.5)

ax.plot(
    [0, 9*np.cos(counter_angle)],
    [0, 9*np.sin(counter_angle)],
    color=GOLD,
    lw=2,
    alpha=0.8
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

ax.text(
    0,
    11,
    "NEXAH — BIG 5 +1",
    color=WHITE,
    fontsize=24,
    ha="center",
    fontweight="bold"
)

ax.text(
    0,
    10,
    "OVAL • PRIME GRID • CORRIDOR • GATE • CORE • Q0",
    color=CYAN,
    fontsize=12,
    ha="center",
    alpha=0.85
)

ax.text(
    0,
    -11,
    "Containment • Resonance • Transition • Emergence",
    color=MAGENTA,
    fontsize=11,
    ha="center",
    alpha=0.8
)

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

plt.tight_layout()

plt.savefig(
    OUT,
    dpi=300,
    facecolor=BG,
    bbox_inches="tight"
)

print(f"saved -> {OUT.resolve()}")

plt.show()
