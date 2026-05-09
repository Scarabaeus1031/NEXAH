# ============================================================
# EXP-21 — JANUS Aperture Gate Operator
# ============================================================
#
# Purpose:
# Investigate whether multiple transition indicators
# converge toward a localized "aperture gate" region.
#
# Hypothesis:
#
# Basin transfer geometry may compress toward a
# coherent transition nucleus where:
#
# - JANUS coherence decreases
# - shell crossings accumulate
# - spine compression increases
# - curvature rises
# - quadrant switching concentrates
#
# Status:
# Exploratory / geometric diagnostic
#
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# Lorenz System
# ============================================================

def lorenz(state, sigma=10.0, rho=28.0, beta=8/3):

    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz])

# ============================================================
# RK4 Integrator
# ============================================================

def rk4_step(f, state, dt):

    k1 = f(state)
    k2 = f(state + 0.5 * dt * k1)
    k3 = f(state + 0.5 * dt * k2)
    k4 = f(state + dt * k3)

    return state + (dt / 6.0) * (
        k1 + 2*k2 + 2*k3 + k4
    )

# ============================================================
# Simulate Lorenz
# ============================================================

dt = 0.01
steps = 14000

trajectory = np.zeros((steps, 3))

state = np.array([1.0, 1.0, 1.0])

for i in range(steps):

    state = rk4_step(lorenz, state, dt)
    trajectory[i] = state

# remove transient
trajectory = trajectory[2000:]

x = trajectory[:,0]
y = trajectory[:,1]
z = trajectory[:,2]

N = len(x)

# ============================================================
# Forward / Backward Fields
# ============================================================

forward = np.gradient(trajectory, axis=0)

backward = -forward[::-1]
backward = backward[::-1]

# ============================================================
# JANUS Coherence
# ============================================================

dot = np.sum(forward * backward, axis=1)

norm_f = np.linalg.norm(forward, axis=1)
norm_b = np.linalg.norm(backward, axis=1)

janus = np.abs(dot) / (norm_f * norm_b + 1e-8)

janus = gaussian_filter1d(janus, sigma=2)

# ============================================================
# Curvature Approximation
# ============================================================

velocity = np.gradient(trajectory, axis=0)
acceleration = np.gradient(velocity, axis=0)

cross = np.cross(velocity, acceleration)

curvature = (
    np.linalg.norm(cross, axis=1)
    /
    (np.linalg.norm(velocity, axis=1)**3 + 1e-8)
)

curvature = gaussian_filter1d(curvature, sigma=2)

# ============================================================
# Shell Structure
# ============================================================

shells = np.quantile(
    janus,
    [0.2, 0.4, 0.6, 0.8]
)

shell_index = np.digitize(janus, shells)

shell_crossing = np.abs(
    np.gradient(shell_index.astype(float))
)

# ============================================================
# Compression Measure
# ============================================================

radius = np.sqrt(x**2 + y**2)

compression = 1 / (radius + 1e-8)

compression = gaussian_filter1d(
    compression,
    sigma=4
)

# ============================================================
# Quadrant Mapping
# ============================================================

quadrant = np.zeros(N)

quadrant[(x >= 0) & (y >= 0)] = 0
quadrant[(x < 0) & (y >= 0)] = 1
quadrant[(x < 0) & (y < 0)] = 2
quadrant[(x >= 0) & (y < 0)] = 3

quadrant_change = np.abs(
    np.gradient(quadrant)
)

# ============================================================
# Aperture Score
# ============================================================

janus_low = 1 - janus

curv_norm = (
    curvature - curvature.min()
) / (
    curvature.max() - curvature.min() + 1e-8
)

comp_norm = (
    compression - compression.min()
) / (
    compression.max() - compression.min() + 1e-8
)

shell_norm = (
    shell_crossing - shell_crossing.min()
) / (
    shell_crossing.max() - shell_crossing.min() + 1e-8
)

quad_norm = (
    quadrant_change - quadrant_change.min()
) / (
    quadrant_change.max() - quadrant_change.min() + 1e-8
)

aperture_score = (
    0.30 * janus_low +
    0.25 * curv_norm +
    0.20 * comp_norm +
    0.15 * shell_norm +
    0.10 * quad_norm
)

aperture_score = gaussian_filter1d(
    aperture_score,
    sigma=2
)

# ============================================================
# Candidate Aperture Gates
# ============================================================

threshold = np.quantile(aperture_score, 0.995)

gate_mask = aperture_score >= threshold

gate_points = trajectory[gate_mask]

# ============================================================
# OUTPUT STATS
# ============================================================

print("\n==============================")
print("EXP-21 — JANUS Aperture Gates")
print("==============================\n")

print(f"samples: {N}")
print(f"gate candidates: {gate_points.shape[0]}")
print()

print(f"mean aperture score:")
print(f"{aperture_score.mean():.6f}")
print()

print(f"max aperture score:")
print(f"{aperture_score.max():.6f}")

# ============================================================
# 3D Aperture Gate Visualization
# ============================================================

fig = plt.figure(figsize=(10, 8))

ax = fig.add_subplot(111, projection='3d')

ax.plot(
    x,
    y,
    z,
    color='lightgray',
    linewidth=0.4,
    alpha=0.5
)

scatter = ax.scatter(
    gate_points[:,0],
    gate_points[:,1],
    gate_points[:,2],
    c=aperture_score[gate_mask],
    cmap='inferno',
    s=18
)

ax.set_title(
    "EXP-21 — JANUS Aperture Gate Candidates"
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.colorbar(
    scatter,
    label="Aperture Score"
)

plt.tight_layout()

plt.savefig(
    "outputs/janus_aperture_gate_candidates.png",
    dpi=300
)

# ============================================================
# Aperture Timeseries
# ============================================================

fig, ax = plt.subplots(
    figsize=(14, 5)
)

ax.plot(
    aperture_score,
    color='darkorange',
    linewidth=1
)

ax.axhline(
    threshold,
    color='red',
    linestyle='--',
    label='Gate Threshold'
)

ax.set_title(
    "EXP-21 — Aperture Score Timeseries"
)

ax.set_xlabel("Time")
ax.set_ylabel("Aperture Score")

ax.legend()

plt.tight_layout()

plt.savefig(
    "outputs/janus_aperture_score_timeseries.png",
    dpi=300
)

# ============================================================
# Quadrant Overlay
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 8)
)

scatter = ax.scatter(
    x,
    y,
    c=aperture_score,
    cmap='plasma',
    s=2
)

ax.scatter(
    gate_points[:,0],
    gate_points[:,1],
    color='white',
    s=20,
    edgecolors='black'
)

ax.set_title(
    "EXP-21 — Aperture Geometry Overlay"
)

ax.set_xlabel("X")
ax.set_ylabel("Y")

plt.colorbar(
    scatter,
    label='Aperture Score'
)

plt.tight_layout()

plt.savefig(
    "outputs/janus_aperture_geometry_overlay.png",
    dpi=300
)

# ============================================================
# Phase Quadrant Map
# ============================================================

fig, ax = plt.subplots(
    figsize=(10, 8)
)

scatter = ax.scatter(
    janus,
    np.gradient(radius),
    c=quadrant,
    cmap='tab10',
    s=4,
    alpha=0.7
)

ax.set_title(
    "EXP-21 — JANUS Phase Quadrant Map"
)

ax.set_xlabel("JANUS coherence")
ax.set_ylabel("breathing velocity")

plt.tight_layout()

plt.savefig(
    "outputs/janus_phase_quadrant_map_exp21.png",
    dpi=300
)

# ============================================================
# Aperture Density
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 6)
)

ax.hist(
    aperture_score,
    bins=80,
    color='darkred',
    alpha=0.8
)

ax.axvline(
    threshold,
    color='black',
    linestyle='--'
)

ax.set_title(
    "EXP-21 — Aperture Score Density"
)

ax.set_xlabel("Aperture Score")
ax.set_ylabel("Count")

plt.tight_layout()

plt.savefig(
    "outputs/janus_aperture_density.png",
    dpi=300
)

# ============================================================
# DONE
# ============================================================

print("\noutputs generated:\n")

print("outputs/janus_aperture_gate_candidates.png")
print("outputs/janus_aperture_score_timeseries.png")
print("outputs/janus_aperture_geometry_overlay.png")
print("outputs/janus_phase_quadrant_map_exp21.png")
print("outputs/janus_aperture_density.png")

print("\nEXP-21 complete.\n")
