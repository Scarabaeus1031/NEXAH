#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 12
janus_local_flow_entropy.py

Goal:
    Test whether JANUS coherence is coupled to local flow entropy.

Core idea:
    - reconstruct Lorenz trajectory
    - compute JANUS coherence
    - estimate local directional entropy in XY phase space
    - compare entropy regions with JANUS coherence
    - visualize entropy ridges / coherence valleys

Outputs:
    outputs/janus_entropy_map.png
    outputs/janus_entropy_vs_janus.png
    outputs/janus_entropy_timeseries.png
    outputs/janus_entropy_density.png
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.stats import binned_statistic_2d


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Lorenz system
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
# Helpers
# ------------------------------------------------------------

def normalize(v: np.ndarray) -> np.ndarray:
    v_min = np.nanmin(v)
    v_max = np.nanmax(v)
    scale = v_max - v_min

    if scale <= 0:
        return np.zeros_like(v)

    return (v - v_min) / scale


def angular_entropy(angles: np.ndarray, bins: int = 16) -> float:
    if len(angles) < 6:
        return np.nan

    hist, _ = np.histogram(
        angles,
        bins=bins,
        range=(-np.pi, np.pi),
        density=False,
    )

    p = hist.astype(float)
    p = p / (np.sum(p) + 1e-12)
    p = p[p > 0]

    entropy = -np.sum(p * np.log(p))

    return entropy / np.log(bins)


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

if not sol.success:
    raise RuntimeError(sol.message)

states = sol.y.T
t = sol.t

# remove transient
states = states[1500:]
t = t[1500:]

x = states[:, 0]
y = states[:, 1]


# ------------------------------------------------------------
# JANUS coherence
# ------------------------------------------------------------

print("Computing JANUS coherence...")

forward = states[2:] - states[1:-1]
backward = states[1:-1] - states[:-2]

overlap = forward * backward

janus = (
    np.linalg.norm(overlap, axis=1)
    / (
        np.linalg.norm(forward, axis=1)
        * np.linalg.norm(backward, axis=1)
        + 1e-8
    )
)

x_mid = x[1:-1]
y_mid = y[1:-1]
t_mid = t[1:-1]

velocity_xy = forward[:, :2]
angles = np.arctan2(velocity_xy[:, 1], velocity_xy[:, 0])


# ------------------------------------------------------------
# Local entropy map
# ------------------------------------------------------------

print("Computing local flow entropy...")

grid_size = 120

x_edges = np.linspace(np.percentile(x_mid, 1), np.percentile(x_mid, 99), grid_size)
y_edges = np.linspace(np.percentile(y_mid, 1), np.percentile(y_mid, 99), grid_size)

entropy_grid = np.full((grid_size - 1, grid_size - 1), np.nan)
janus_grid = np.full((grid_size - 1, grid_size - 1), np.nan)

x_bin = np.digitize(x_mid, x_edges) - 1
y_bin = np.digitize(y_mid, y_edges) - 1

for i in range(grid_size - 1):
    for j in range(grid_size - 1):
        mask = (x_bin == i) & (y_bin == j)

        if np.sum(mask) >= 8:
            entropy_grid[j, i] = angular_entropy(angles[mask])
            janus_grid[j, i] = np.mean(janus[mask])

entropy_flat = entropy_grid.ravel()
janus_flat = janus_grid.ravel()

valid = np.isfinite(entropy_flat) & np.isfinite(janus_flat)

entropy_values = entropy_flat[valid]
janus_values = janus_flat[valid]

entropy_norm = normalize(entropy_values)


# ------------------------------------------------------------
# Timeseries entropy projection
# ------------------------------------------------------------

entropy_ts = np.full_like(janus, np.nan)

for k in range(len(janus)):
    i = x_bin[k]
    j = y_bin[k]

    if 0 <= i < grid_size - 1 and 0 <= j < grid_size - 1:
        entropy_ts[k] = entropy_grid[j, i]

valid_ts = np.isfinite(entropy_ts)

entropy_ts_norm = np.zeros_like(entropy_ts)
entropy_ts_norm[valid_ts] = normalize(entropy_ts[valid_ts])


# ------------------------------------------------------------
# Plot 1: entropy map
# ------------------------------------------------------------

print("Generating visualizations...")

fig, ax = plt.subplots(figsize=(10, 8))

img = ax.imshow(
    entropy_grid,
    extent=(x_edges.min(), x_edges.max(), y_edges.min(), y_edges.max()),
    origin="lower",
    aspect="auto",
    cmap="magma",
)

ax.scatter(
    x_mid[::20],
    y_mid[::20],
    c=janus[::20],
    s=0.3,
    cmap="viridis",
    alpha=0.35,
)

cbar = fig.colorbar(img, ax=ax)
cbar.set_label("local directional entropy")

ax.set_title("JANUS Local Flow Entropy Map")
ax.set_xlabel("x")
ax.set_ylabel("y")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_entropy_map.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 2: entropy vs JANUS
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(
    janus_values,
    entropy_values,
    s=6,
    alpha=0.45,
)

if len(janus_values) > 2:
    r = np.corrcoef(janus_values, entropy_values)[0, 1]
else:
    r = np.nan

ax.set_title(f"JANUS vs Local Flow Entropy\nPearson r = {r:.4f}")
ax.set_xlabel("mean JANUS coherence")
ax.set_ylabel("local directional entropy")
ax.grid(alpha=0.18)

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_entropy_vs_janus.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 3: timeseries
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 5))

step = max(1, len(t_mid) // 9000)

ax.plot(
    t_mid[::step],
    janus[::step],
    linewidth=0.8,
    label="JANUS coherence",
)

ax.plot(
    t_mid[::step],
    entropy_ts_norm[::step],
    linewidth=0.8,
    alpha=0.85,
    label="normalized local entropy",
)

ax.set_title("JANUS and Local Flow Entropy — Timeseries")
ax.set_xlabel("time")
ax.set_ylabel("normalized value")
ax.grid(alpha=0.18)
ax.legend()

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_entropy_timeseries.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 4: density
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

h = ax.hist2d(
    janus_values,
    entropy_values,
    bins=70,
    cmap="viridis",
)

fig.colorbar(h[3], ax=ax, label="density")

ax.set_title("JANUS–Entropy Joint Density")
ax.set_xlabel("mean JANUS coherence")
ax.set_ylabel("local directional entropy")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_entropy_density.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print()
print("=" * 48)
print("JANUS LOCAL FLOW ENTROPY ANALYSIS")
print("=" * 48)

print(f"samples: {len(janus)}")
print(f"valid entropy cells: {len(entropy_values)}")
print(f"mean JANUS: {np.mean(janus):.6f}")
print(f"mean entropy: {np.nanmean(entropy_values):.6f}")
print(f"correlation JANUS vs entropy: {r:.6f}")

low_j = janus_values <= np.quantile(janus_values, 0.08)
high_e = entropy_values >= np.quantile(entropy_values, 0.92)

overlap = np.mean(low_j & high_e)

print(f"low-JANUS / high-entropy overlap fraction: {overlap:.6f}")

print()
print("outputs saved to:")
print(OUTPUT_DIR)

print("=" * 48)
