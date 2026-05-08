import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# ============================================================
# NEXAH — INTERACTIVE NAVIGATION MAP
# ============================================================

np.random.seed(7)

# ------------------------------------------------------------
# Generate structured trajectory
# ------------------------------------------------------------

t = np.linspace(0, 18 * np.pi, 4000)

x = np.sin(t) + 0.35 * np.sin(3 * t)
y = np.cos(t) * np.sin(t / 4)

# transition region
mask = (t > 20) & (t < 32)

x[mask] += np.random.normal(scale=0.18, size=np.sum(mask))
y[mask] += np.random.normal(scale=0.18, size=np.sum(mask))

# ------------------------------------------------------------
# Density field
# ------------------------------------------------------------

xy = np.vstack([x, y])
kde = gaussian_kde(xy)

xmin, xmax = x.min() - 0.5, x.max() + 0.5
ymin, ymax = y.min() - 0.5, y.max() + 0.5

xx, yy = np.meshgrid(
    np.linspace(xmin, xmax, 320),
    np.linspace(ymin, ymax, 320)
)

coords = np.vstack([xx.ravel(), yy.ravel()])
density = kde(coords).reshape(xx.shape)

density_norm = density / density.max()

# ------------------------------------------------------------
# Gradient field
# ------------------------------------------------------------

gy, gx = np.gradient(density_norm)

# ------------------------------------------------------------
# Coherence proxy
# ------------------------------------------------------------

dx = np.gradient(x)
dy = np.gradient(y)

speed = np.sqrt(dx**2 + dy**2)

coherence = (
    np.abs(dx[:-1] * dx[1:] + dy[:-1] * dy[1:])
    /
    (speed[:-1] * speed[1:] + 1e-8)
)

coherence = np.clip(coherence, 0, 1)

# ------------------------------------------------------------
# Gate estimation
# ------------------------------------------------------------

gate_idx = np.where(coherence < 0.35)[0]

# ------------------------------------------------------------
# Navigation path
# ------------------------------------------------------------

path_idx = np.arange(300, 900, 5)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

fig = plt.figure(figsize=(16, 12))

# ============================================================
# PANEL 1 — Density Structure
# ============================================================

ax1 = plt.subplot(2, 2, 1)

im1 = ax1.imshow(
    density_norm,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    cmap="plasma",
    aspect="auto"
)

ax1.plot(x, y, color="white", lw=0.4, alpha=0.55)

ax1.scatter(
    x[gate_idx],
    y[gate_idx],
    s=12,
    c="red",
    alpha=0.8,
    label="gate regions"
)

ax1.set_title("Density Structure + Gate Regions")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.legend()

# ============================================================
# PANEL 2 — Gradient / Drift Field
# ============================================================

ax2 = plt.subplot(2, 2, 2)

ax2.imshow(
    density_norm,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    cmap="viridis",
    alpha=0.9,
    aspect="auto"
)

step = 12

ax2.quiver(
    xx[::step, ::step],
    yy[::step, ::step],
    gx[::step, ::step],
    gy[::step, ::step],
    color="white",
    alpha=0.9,
    scale=20
)

ax2.set_title("Structural Gradient Field ∇ρ(x)")
ax2.set_xlabel("x")
ax2.set_ylabel("y")

# ============================================================
# PANEL 3 — Navigation Path
# ============================================================

ax3 = plt.subplot(2, 2, 3)

ax3.imshow(
    density_norm,
    extent=[xmin, xmax, ymin, ymax],
    origin="lower",
    cmap="magma",
    aspect="auto"
)

ax3.plot(
    x,
    y,
    color="lightgray",
    lw=0.4,
    alpha=0.25
)

ax3.plot(
    x[path_idx],
    y[path_idx],
    color="cyan",
    lw=3,
    label="navigation path"
)

ax3.scatter(
    x[path_idx[0]],
    y[path_idx[0]],
    s=90,
    c="lime",
    label="start"
)

ax3.scatter(
    x[path_idx[-1]],
    y[path_idx[-1]],
    s=90,
    c="red",
    label="target"
)

ax3.set_title("Interactive Navigation Path")
ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.legend()

# ============================================================
# PANEL 4 — Structural Grammar
# ============================================================

ax4 = plt.subplot(2, 2, 4)

ax4.axis("off")

grammar = r"""
NEXAH STRUCTURAL GRAMMAR

x          → state
ẋ          → motion
F(x)       → flow field
ρ(x)       → structural density
∇ρ(x)      → structural drift
C(x)       → coherence
A(x)       → change dynamics
G(x)       → gate susceptibility
M(t)       → mismatch
T(x)       → transition tension
J(x)       → directional coupling
s(t)       → navigation / control

Core Principle:

Dynamics
→ Structure
→ Gates
→ Transition
→ Navigation
"""

ax4.text(
    0.02,
    0.98,
    grammar,
    va="top",
    fontsize=13,
    family="monospace"
)

# ------------------------------------------------------------
# Global title
# ------------------------------------------------------------

plt.suptitle(
    "NEXAH — interactive_navigation_map",
    fontsize=22
)

plt.tight_layout()

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

plt.savefig(
    "interactive_navigation_map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
