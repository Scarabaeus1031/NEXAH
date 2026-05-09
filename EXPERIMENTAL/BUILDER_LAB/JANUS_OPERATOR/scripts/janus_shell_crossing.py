#!/usr/bin/env python3
"""
JANUS_OPERATOR / Experiment 13
janus_shell_crossing.py

Goal:
    Analyze whether JANUS basin-transfer dynamics can be interpreted
    as shell-crossing behavior between coherence regimes.

Core idea:
    - compute JANUS coherence on Lorenz trajectory
    - define coherence shells by quantile bands
    - detect shell transitions / crossings
    - compare shell crossings with basin-transfer events
    - visualize shell occupation, crossing density, and phase structure

Outputs:
    outputs/janus_shell_crossing_overlay.png
    outputs/janus_shell_crossing_timeseries.png
    outputs/janus_shell_crossing_density.png
    outputs/janus_shell_crossing_phase.png
    outputs/janus_shell_crossing_summary.txt
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


def normalize(values: np.ndarray) -> np.ndarray:
    v_min = np.nanmin(values)
    v_max = np.nanmax(values)
    scale = v_max - v_min

    if scale <= 0:
        return np.zeros_like(values)

    return (values - v_min) / scale


# ------------------------------------------------------------
# Simulation
# ------------------------------------------------------------

print("Running Lorenz simulation...")

dt = 0.01
t_eval = np.arange(0.0, 120.0, dt)

sol = solve_ivp(
    lorenz,
    (0.0, 120.0),
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

janus_smooth = gaussian_filter1d(janus, sigma=2.5)

x_mid = x[1:-1]
y_mid = y[1:-1]
z_mid = z[1:-1]
t_mid = t[1:-1]


# ------------------------------------------------------------
# Basin transfer events
# ------------------------------------------------------------

print("Detecting basin transfer events...")

basin = np.sign(x_mid)

transfer_idx = np.where(basin[1:] != basin[:-1])[0]

# remove immediate duplicates
if len(transfer_idx) > 0:
    keep = [transfer_idx[0]]

    for idx in transfer_idx[1:]:
        if idx - keep[-1] > 80:
            keep.append(idx)

    transfer_idx = np.array(keep, dtype=int)


# ------------------------------------------------------------
# Coherence shell definition
# ------------------------------------------------------------

print("Computing coherence shells...")

shell_edges = np.quantile(
    janus_smooth,
    [0.0, 0.20, 0.40, 0.60, 0.80, 1.0],
)

shell_id = np.digitize(
    janus_smooth,
    shell_edges[1:-1],
    right=True,
)

n_shells = len(shell_edges) - 1

shell_crossings = np.where(shell_id[1:] != shell_id[:-1])[0]

crossing_strength = np.abs(np.diff(janus_smooth))
crossing_strength_at_crossing = crossing_strength[shell_crossings]

strong_threshold = np.quantile(crossing_strength_at_crossing, 0.90)
strong_crossings = shell_crossings[
    crossing_strength_at_crossing >= strong_threshold
]


# ------------------------------------------------------------
# Transfer / shell overlap
# ------------------------------------------------------------

window = 25

transfer_near_shell = []

for tr in transfer_idx:
    near = np.any(np.abs(shell_crossings - tr) <= window)
    transfer_near_shell.append(near)

transfer_near_shell = np.array(transfer_near_shell)

strong_transfer_near_shell = []

for tr in transfer_idx:
    near = np.any(np.abs(strong_crossings - tr) <= window)
    strong_transfer_near_shell.append(near)

strong_transfer_near_shell = np.array(strong_transfer_near_shell)


# ------------------------------------------------------------
# Plot 1: phase overlay
# ------------------------------------------------------------

print("Generating visualizations...")

fig, ax = plt.subplots(figsize=(10, 8))

sc = ax.scatter(
    x_mid,
    y_mid,
    c=shell_id,
    s=0.7,
    cmap="viridis",
    alpha=0.65,
)

ax.scatter(
    x_mid[shell_crossings],
    y_mid[shell_crossings],
    c="black",
    s=2,
    alpha=0.35,
    label="shell crossings",
)

ax.scatter(
    x_mid[strong_crossings],
    y_mid[strong_crossings],
    c="red",
    s=10,
    alpha=0.85,
    label="strong shell crossings",
)

ax.scatter(
    x_mid[transfer_idx],
    y_mid[transfer_idx],
    c="white",
    edgecolors="black",
    s=36,
    linewidths=0.8,
    label="basin transfers",
)

cbar = fig.colorbar(sc, ax=ax)
cbar.set_label("JANUS coherence shell")

ax.set_title("JANUS Shell Crossing Overlay")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc="upper right")
ax.grid(alpha=0.15)

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_shell_crossing_overlay.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 2: timeseries shell occupation
# ------------------------------------------------------------

fig, ax1 = plt.subplots(figsize=(15, 5))

ax1.plot(
    t_mid,
    janus_smooth,
    linewidth=0.8,
    label="JANUS coherence",
)

for edge in shell_edges[1:-1]:
    ax1.axhline(edge, linestyle="--", alpha=0.35)

ax1.scatter(
    t_mid[strong_crossings],
    janus_smooth[strong_crossings],
    s=12,
    c="red",
    label="strong shell crossings",
)

ax1.scatter(
    t_mid[transfer_idx],
    janus_smooth[transfer_idx],
    s=28,
    c="white",
    edgecolors="black",
    linewidths=0.8,
    label="basin transfers",
)

ax1.set_title("JANUS Shell Crossing Timeseries")
ax1.set_xlabel("time")
ax1.set_ylabel("JANUS coherence")
ax1.grid(alpha=0.18)
ax1.legend(loc="upper right")

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_shell_crossing_timeseries.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 3: shell-crossing density
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 6))

bins = np.arange(n_shells + 1) - 0.5

ax.hist(
    shell_id,
    bins=bins,
    density=True,
    alpha=0.65,
    label="shell occupation",
)

ax.hist(
    shell_id[shell_crossings],
    bins=bins,
    density=True,
    alpha=0.65,
    label="shell-crossing locations",
)

ax.set_xticks(range(n_shells))
ax.set_title("JANUS Shell Occupation vs Crossing Density")
ax.set_xlabel("shell id")
ax.set_ylabel("density")
ax.legend()
ax.grid(alpha=0.18)

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_shell_crossing_density.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Plot 4: shell phase map
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

ax.scatter(
    janus_smooth[:-1],
    janus_smooth[1:],
    c=shell_id[:-1],
    s=0.7,
    cmap="viridis",
    alpha=0.65,
)

ax.scatter(
    janus_smooth[strong_crossings],
    janus_smooth[strong_crossings + 1],
    c="red",
    s=10,
    alpha=0.85,
    label="strong crossings",
)

ax.set_title("JANUS Shell Crossing Phase Map")
ax.set_xlabel("J(t)")
ax.set_ylabel("J(t+1)")
ax.legend()
ax.grid(alpha=0.18)

fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "janus_shell_crossing_phase.png",
    dpi=220,
)

plt.close()


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

summary = []
summary.append("JANUS shell crossing experiment")
summary.append("==============================")
summary.append("")
summary.append(f"samples: {len(janus_smooth)}")
summary.append(f"shells: {n_shells}")
summary.append("")
summary.append("shell edges:")
for i, edge in enumerate(shell_edges):
    summary.append(f"edge {i}: {edge:.6f}")
summary.append("")
summary.append(f"shell crossings: {len(shell_crossings)}")
summary.append(f"strong shell crossings: {len(strong_crossings)}")
summary.append(f"basin transfers: {len(transfer_idx)}")
summary.append("")
summary.append(
    f"transfer near any shell crossing "
    f"(±{window} samples): {np.mean(transfer_near_shell):.6f}"
)
summary.append(
    f"transfer near strong shell crossing "
    f"(±{window} samples): {np.mean(strong_transfer_near_shell):.6f}"
)
summary.append("")
summary.append("shell occupation counts:")
for sid in range(n_shells):
    summary.append(f"shell {sid}: {np.sum(shell_id == sid)}")

(OUTPUT_DIR / "janus_shell_crossing_summary.txt").write_text(
    "\n".join(summary)
)

print()
print("=" * 48)
print("JANUS SHELL CROSSING ANALYSIS")
print("=" * 48)

print(f"samples: {len(janus_smooth)}")
print(f"shell crossings: {len(shell_crossings)}")
print(f"strong shell crossings: {len(strong_crossings)}")
print(f"basin transfers: {len(transfer_idx)}")
print(
    f"transfer near shell crossing: "
    f"{np.mean(transfer_near_shell):.6f}"
)
print(
    f"transfer near strong crossing: "
    f"{np.mean(strong_transfer_near_shell):.6f}"
)

print()
print("shell edges:")
for i, edge in enumerate(shell_edges):
    print(f"edge {i}: {edge:.6f}")

print()
print("outputs saved to:")
print(OUTPUT_DIR)

print("=" * 48)
