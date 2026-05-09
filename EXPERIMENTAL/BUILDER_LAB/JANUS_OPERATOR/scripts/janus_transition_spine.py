#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 14
janus_transition_spine.py

Goal:
    Extract the dominant transition spine inside the Lorenz/JANUS field.

Idea:
    The "transition spine" is interpreted as the preferred geometric
    corridor through which basin transfers occur.

    We estimate this by:

    - detecting transfer events
    - extracting local neighborhoods around crossings
    - averaging aligned trajectories
    - building a statistical transition manifold

Outputs:
    outputs/janus_transition_spine_overlay.png
    outputs/janus_transition_spine_density.png
    outputs/janus_transition_spine_timeseries.png
    outputs/janus_transition_spine_phase.png
    outputs/janus_transition_spine_summary.txt
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import solve_ivp
from scipy.ndimage import gaussian_filter1d


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


def normalize(values):
    vmin = np.nanmin(values)
    vmax = np.nanmax(values)

    if vmax - vmin <= 0:
        return np.zeros_like(values)

    return (values - vmin) / (vmax - vmin)


# ------------------------------------------------------------
# Simulation
# ------------------------------------------------------------

print("Running Lorenz simulation...")

dt = 0.01

t_eval = np.arange(0.0, 140.0, dt)

sol = solve_ivp(
    lorenz,
    (0.0, 140.0),
    [1.0, 1.0, 1.0],
    t_eval=t_eval,
    method="DOP853",
)

if not sol.success:
    raise RuntimeError(sol.message)

states = sol.y.T
t = sol.t

# remove transient
states = states[2000:]
t = t[2000:]

x = states[:, 0]
y = states[:, 1]
z = states[:, 2]


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

janus = gaussian_filter1d(janus, sigma=2.0)

x_mid = x[1:-1]
y_mid = y[1:-1]
z_mid = z[1:-1]
t_mid = t[1:-1]


# ------------------------------------------------------------
# Basin transfer detection
# ------------------------------------------------------------

print("Detecting transfer events...")

basin = np.sign(x_mid)

transfer_idx = np.where(basin[1:] != basin[:-1])[0]

# remove duplicates
filtered = []

for idx in transfer_idx:
    if not filtered:
        filtered.append(idx)
    elif idx - filtered[-1] > 120:
        filtered.append(idx)

transfer_idx = np.array(filtered)

print(f"transfer events: {len(transfer_idx)}")


# ------------------------------------------------------------
# Extract local transition windows
# ------------------------------------------------------------

window = 80

segments_x = []
segments_y = []
segments_j = []

for idx in transfer_idx:

    if idx - window < 0:
        continue

    if idx + window >= len(x_mid):
        continue

    sx = x_mid[idx - window: idx + window + 1]
    sy = y_mid[idx - window: idx + window + 1]
    sj = janus[idx - window: idx + window + 1]

    # align direction
    if np.mean(sx[:20]) > 0:
        sx = -sx
        sy = -sy

    segments_x.append(sx)
    segments_y.append(sy)
    segments_j.append(sj)

segments_x = np.array(segments_x)
segments_y = np.array(segments_y)
segments_j = np.array(segments_j)

relative_time = np.arange(-window, window + 1)


# ------------------------------------------------------------
# Transition spine
# ------------------------------------------------------------

print("Computing transition spine...")

spine_x = np.mean(segments_x, axis=0)
spine_y = np.mean(segments_y, axis=0)
spine_j = np.mean(segments_j, axis=0)

spine_std_x = np.std(segments_x, axis=0)
spine_std_y = np.std(segments_y, axis=0)

radial_spread = np.sqrt(spine_std_x**2 + spine_std_y**2)

spine_speed = np.sqrt(
    np.diff(spine_x)**2 +
    np.diff(spine_y)**2
)

spine_speed = gaussian_filter1d(spine_speed, sigma=2)

peak_speed_idx = np.argmax(spine_speed)


# ------------------------------------------------------------
# Plot 1 — transition spine overlay
# ------------------------------------------------------------

print("Generating visualizations...")

fig, ax = plt.subplots(figsize=(10, 8))

# background field
ax.scatter(
    x_mid,
    y_mid,
    c=janus,
    s=0.5,
    cmap="viridis",
    alpha=0.15,
)

# transfer trajectories
for sx, sy in zip(segments_x, segments_y):

    ax.plot(
        sx,
        sy,
        linewidth=0.8,
        alpha=0.10,
        color="tab:blue",
    )

# spine
ax.plot(
    spine_x,
    spine_y,
    linewidth=4,
    color="black",
    label="transition spine",
)

# center point
ax.scatter(
    spine_x[window],
    spine_y[window],
    c="red",
    s=80,
    zorder=5,
    label="crossing center",
)

ax.set_title("JANUS Transition Spine Overlay")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(alpha=0.15)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "janus_transition_spine_overlay.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 2 — radial density / spread
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    relative_time,
    radial_spread,
    linewidth=2.5,
)

ax.axvline(
    0,
    linestyle="--",
    alpha=0.5,
)

ax.set_title("JANUS Transition Spine Spread")
ax.set_xlabel("relative transfer lag")
ax.set_ylabel("radial spread")
ax.grid(alpha=0.18)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "janus_transition_spine_density.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 3 — JANUS transfer timeseries
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 5))

for sj in segments_j:
    ax.plot(
        relative_time,
        sj,
        alpha=0.08,
        linewidth=1.0,
    )

ax.plot(
    relative_time,
    spine_j,
    linewidth=4,
    color="black",
    label="mean JANUS spine",
)

ax.axvline(
    0,
    linestyle="--",
    alpha=0.5,
)

ax.set_title("JANUS Transition Spine Timeseries")
ax.set_xlabel("relative transfer lag")
ax.set_ylabel("JANUS coherence")
ax.legend()
ax.grid(alpha=0.18)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "janus_transition_spine_timeseries.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 4 — phase structure
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

ax.scatter(
    spine_j[:-1],
    spine_j[1:],
    s=12,
    alpha=0.85,
)

ax.scatter(
    spine_j[peak_speed_idx],
    spine_j[peak_speed_idx + 1],
    c="red",
    s=80,
    label="max transition velocity",
)

ax.set_title("JANUS Transition Spine Phase Structure")
ax.set_xlabel("J(t)")
ax.set_ylabel("J(t+1)")
ax.legend()
ax.grid(alpha=0.18)

fig.tight_layout()

fig.savefig(
    OUTPUT_DIR / "janus_transition_spine_phase.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

summary = []

summary.append("JANUS transition spine analysis")
summary.append("================================")
summary.append("")

summary.append(f"samples: {len(janus)}")
summary.append(f"transfer events: {len(segments_x)}")
summary.append("")

summary.append(f"mean JANUS coherence: {np.mean(spine_j):.6f}")
summary.append(f"min JANUS coherence: {np.min(spine_j):.6f}")
summary.append(f"max JANUS coherence: {np.max(spine_j):.6f}")
summary.append("")

summary.append(f"max radial spread: {np.max(radial_spread):.6f}")
summary.append(f"min radial spread: {np.min(radial_spread):.6f}")
summary.append("")

summary.append(
    f"peak transition velocity index: "
    f"{peak_speed_idx - window}"
)

summary.append(
    f"peak transition velocity: "
    f"{np.max(spine_speed):.6f}"
)

summary.append("")

summary.append(
    "Interpretation:"
)

summary.append(
    "The transition spine estimates the dominant "
    "geometric corridor through which basin "
    "exchange occurs."
)

summary.append(
    "Low spread regions indicate stable "
    "transfer alignment."
)

summary.append(
    "High spread regions indicate transition "
    "decompression / branching."
)

summary_text = "\n".join(summary)

(
    OUTPUT_DIR /
    "janus_transition_spine_summary.txt"
).write_text(summary_text)

print()
print("=" * 52)
print("JANUS TRANSITION SPINE ANALYSIS")
print("=" * 52)

print(f"samples: {len(janus)}")
print(f"transfer events: {len(segments_x)}")
print(f"mean JANUS coherence: {np.mean(spine_j):.6f}")
print(f"peak transition velocity: {np.max(spine_speed):.6f}")
print(f"max radial spread: {np.max(radial_spread):.6f}")

print()
print("outputs saved to:")
print(OUTPUT_DIR)

print("=" * 52)
