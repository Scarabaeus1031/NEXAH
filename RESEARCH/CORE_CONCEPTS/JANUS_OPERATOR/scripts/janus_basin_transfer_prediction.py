#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 11
janus_basin_transfer_prediction.py

Goal:
    Detect whether JANUS coherence changes
    before Lorenz attractor-side switching events.

Core idea:
    - detect left/right attractor occupancy
    - identify switching moments
    - analyze JANUS coherence around transitions
    - visualize transfer corridors

Outputs:
    outputs/janus_basin_transfer_overlay.png
    outputs/janus_basin_transfer_density.png
    outputs/janus_basin_transfer_timeseries.png
    outputs/janus_basin_transfer_phase.png
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.stats import gaussian_kde


OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent / "outputs"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Lorenz
# ------------------------------------------------------------

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0


def lorenz(_, s):
    x, y, z = s

    dx = SIGMA * (y - x)
    dy = x * (RHO - z) - y
    dz = x * y - BETA * z

    return [dx, dy, dz]


# ------------------------------------------------------------
# Simulation
# ------------------------------------------------------------

print("Running Lorenz simulation...")

dt = 0.01
t_eval = np.arange(0, 120, dt)

sol = solve_ivp(
    lorenz,
    (0, 120),
    [1.0, 1.0, 1.0],
    t_eval=t_eval,
    method="DOP853",
)

states = sol.y.T
t = sol.t

states = states[1500:]
t = t[1500:]

x = states[:, 0]
y = states[:, 1]
z = states[:, 2]


# ------------------------------------------------------------
# JANUS coherence
# ------------------------------------------------------------

print("Computing JANUS coherence...")

fwd = states[2:] - states[1:-1]
bwd = states[1:-1] - states[:-2]

fwd_norm = np.linalg.norm(fwd, axis=1)
bwd_norm = np.linalg.norm(bwd, axis=1)

overlap = fwd * bwd

janus = (
    np.linalg.norm(overlap, axis=1)
    / (fwd_norm * bwd_norm + 1e-8)
)

x_mid = x[1:-1]
y_mid = y[1:-1]


# ------------------------------------------------------------
# Basin switching
# ------------------------------------------------------------

print("Detecting basin transfer events...")

basin = np.sign(x_mid)

switch_idx = np.where(
    basin[1:] != basin[:-1]
)[0]

switch_idx = switch_idx[
    np.diff(
        np.concatenate(([0], switch_idx))
    ) > 100
]

print(f"switch events: {len(switch_idx)}")


# ------------------------------------------------------------
# Transition windows
# ------------------------------------------------------------

window = 80

segments = []

for idx in switch_idx:

    if idx > window and idx < len(janus) - window:
        seg = janus[idx - window : idx + window]
        segments.append(seg)

segments = np.array(segments)

mean_transfer = np.mean(segments, axis=0)


# ------------------------------------------------------------
# Plot 1
# Basin transfer overlay
# ------------------------------------------------------------

print("Generating visualizations...")

fig, ax = plt.subplots(figsize=(10, 8))

sc = ax.scatter(
    x_mid,
    y_mid,
    c=janus,
    s=0.6,
    cmap="viridis",
    alpha=0.7,
)

ax.scatter(
    x_mid[switch_idx],
    y_mid[switch_idx],
    c="red",
    s=12,
    label="transfer events",
)

cbar = fig.colorbar(sc, ax=ax)
cbar.set_label("JANUS coherence")

ax.set_title("JANUS Basin Transfer Overlay")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_basin_transfer_overlay.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 2
# Density
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 6))

vals = mean_transfer

density = gaussian_kde(vals)

xs = np.linspace(vals.min(), vals.max(), 500)

ax.plot(xs, density(xs), linewidth=2)

ax.set_title("JANUS Basin Transfer Density")
ax.set_xlabel("JANUS coherence")
ax.set_ylabel("density")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_basin_transfer_density.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 3
# Transfer timeseries
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 5))

for seg in segments:
    ax.plot(
        np.arange(-window, window),
        seg,
        alpha=0.12,
        linewidth=1,
    )

ax.plot(
    np.arange(-window, window),
    mean_transfer,
    linewidth=3,
    color="black",
)

ax.axvline(0, linestyle="--")

ax.set_title("JANUS Basin Transfer Timeseries")
ax.set_xlabel("relative lag")
ax.set_ylabel("JANUS coherence")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_basin_transfer_timeseries.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 4
# Phase structure
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

ax.scatter(
    janus[:-1],
    janus[1:],
    s=0.5,
    alpha=0.4,
)

ax.set_title("JANUS Basin Transfer Phase Structure")
ax.set_xlabel("J(t)")
ax.set_ylabel("J(t+1)")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_basin_transfer_phase.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print()
print("=" * 48)
print("JANUS BASIN TRANSFER ANALYSIS")
print("=" * 48)

print(f"samples: {len(janus)}")
print(f"switch events: {len(switch_idx)}")

print()
print("mean transfer coherence:")
print(f"{np.mean(mean_transfer):.6f}")

print()
print("minimum transfer coherence:")
print(f"{np.min(mean_transfer):.6f}")

print()
print("maximum transfer coherence:")
print(f"{np.max(mean_transfer):.6f}")

print()
print("outputs saved to:")
print(OUTPUT_DIR)

print("=" * 48)
