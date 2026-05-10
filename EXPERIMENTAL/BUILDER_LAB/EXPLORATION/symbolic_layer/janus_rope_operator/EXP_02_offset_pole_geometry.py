# ============================================================
# EXP_02_offset_pole_geometry.py
# JANUS Rope Operator — Offset Pole Geometry
#
# Purpose:
# Test whether an off-centered transition pole
# generates directional transport geometry,
# asymmetric gates,
# and spiral routing structures.
#
# Author:
# Thomas Hofmann / NEXAH
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

T_MAX = 120
DT = 0.01

times = np.arange(0, T_MAX, DT)

# ------------------------------------------------------------
# OFFSET POLE
# ------------------------------------------------------------

# central reference
CENTER_X = 0.0
CENTER_Y = 0.0

# offset transition pole
POLE_X = 10.0
POLE_Y = 0.0

# ------------------------------------------------------------
# PRIME DRIFT SYSTEM
# ------------------------------------------------------------

freqs = [2, 3, 5, 7]

offsets = [
    np.pi,
    (1 + np.sqrt(5)) / 2,     # phi
    np.sqrt(2),
    np.pi / np.sqrt(2)
]

# ------------------------------------------------------------
# ROOT THREAD
# ------------------------------------------------------------

ROOT_FREQ = np.sqrt(2)
ROOT_PHASE = np.pi / 4

# ------------------------------------------------------------
# ROPE GENERATION
# ------------------------------------------------------------

ropes_x = []
ropes_y = []

for i, f in enumerate(freqs):

    phase = offsets[i]

    x = np.sin(f * times + phase)

    # offset deformation
    y = np.cos(
        f * times
        + phase
        + 0.12 * x
    )

    ropes_x.append(x)
    ropes_y.append(y)

# root regulator thread
root_x = np.sin(ROOT_FREQ * times + ROOT_PHASE)
root_y = np.cos(ROOT_FREQ * times + ROOT_PHASE)

# ------------------------------------------------------------
# TRANSITION GEOMETRY
# ------------------------------------------------------------

# build combined transport field

field_x = np.zeros_like(times)
field_y = np.zeros_like(times)

for i in range(len(freqs)):

    field_x += ropes_x[i]
    field_y += ropes_y[i]

# add root stabilization
field_x += 0.5 * root_x
field_y += 0.5 * root_y

# normalize
field_x /= (len(freqs) + 0.5)
field_y /= (len(freqs) + 0.5)

# ------------------------------------------------------------
# OFFSET POLE DEFORMATION
# ------------------------------------------------------------

# radial relation to pole

dx = field_x - (POLE_X / 10)
dy = field_y - (POLE_Y / 10)

radius = np.sqrt(dx**2 + dy**2)

# spiral transport modulation
theta = np.arctan2(dy, dx)

spiral_x = field_x + 0.25 * np.sin(2 * theta)
spiral_y = field_y + 0.25 * np.cos(3 * theta)

# ------------------------------------------------------------
# APERTURE SCORE
# ------------------------------------------------------------

aperture_score = np.abs(np.gradient(theta))

threshold = np.percentile(aperture_score, 95)

gate_mask = aperture_score > threshold

# ------------------------------------------------------------
# ROUTING ANGLES
# ------------------------------------------------------------

angles = np.degrees(theta) % 360

# ------------------------------------------------------------
# PRINT STATS
# ------------------------------------------------------------

print("\n===================================")
print("EXP_02 — OFFSET POLE GEOMETRY")
print("===================================")

print(f"\nSamples: {len(times)}")
print(f"Gate candidates: {np.sum(gate_mask)}")

print(f"\nMean aperture score: {np.mean(aperture_score):.6f}")
print(f"Max aperture score: {np.max(aperture_score):.6f}")

print(f"\nMean routing angle: {np.mean(angles):.3f}°")
print(f"Std routing angle: {np.std(angles):.3f}°")

# ------------------------------------------------------------
# PLOT 1 — OFFSET TRANSPORT FIELD
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

ax.plot(
    spiral_x,
    spiral_y,
    linewidth=0.4,
    alpha=0.8
)

# pole
ax.scatter(
    [POLE_X / 10],
    [POLE_Y / 10],
    s=200,
    marker="x",
    label="offset pole"
)

ax.set_title("EXP_02 — Offset Pole Transport Geometry")

ax.set_xlabel("x")
ax.set_ylabel("y")

ax.legend()

plt.tight_layout()
plt.savefig("exp02_offset_transport_geometry.png", dpi=300)

# ------------------------------------------------------------
# PLOT 2 — APERTURE GATES
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

ax.plot(
    spiral_x,
    spiral_y,
    linewidth=0.3,
    alpha=0.3
)

ax.scatter(
    spiral_x[gate_mask],
    spiral_y[gate_mask],
    c=aperture_score[gate_mask],
    s=10
)

ax.scatter(
    [POLE_X / 10],
    [POLE_Y / 10],
    s=150,
    marker="x",
    label="offset pole"
)

ax.set_title("EXP_02 — Aperture Gate Candidates")

ax.set_xlabel("x")
ax.set_ylabel("y")

ax.legend()

plt.tight_layout()
plt.savefig("exp02_aperture_gate_candidates.png", dpi=300)

# ------------------------------------------------------------
# PLOT 3 — ROUTING ANGLE HISTOGRAM
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 5))

ax.hist(
    angles,
    bins=72
)

ax.set_title("EXP_02 — Routing Angle Distribution")

ax.set_xlabel("routing angle (deg)")
ax.set_ylabel("count")

plt.tight_layout()
plt.savefig("exp02_routing_angle_distribution.png", dpi=300)

# ------------------------------------------------------------
# PLOT 4 — SPIRAL PHASE MAP
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 10))

scatter = ax.scatter(
    spiral_x,
    spiral_y,
    c=theta,
    s=1
)

ax.scatter(
    [POLE_X / 10],
    [POLE_Y / 10],
    s=150,
    marker="x"
)

ax.set_title("EXP_02 — Spiral Routing Phase Map")

ax.set_xlabel("x")
ax.set_ylabel("y")

plt.colorbar(scatter)

plt.tight_layout()
plt.savefig("exp02_spiral_phase_map.png", dpi=300)

# ------------------------------------------------------------
# PLOT 5 — ROOT THREAD OVERLAY
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

for i in range(len(freqs)):

    ax.plot(
        ropes_x[i],
        alpha=0.5
    )

ax.plot(
    root_x,
    linewidth=3,
    label="root thread"
)

ax.set_title("EXP_02 — Root Thread Stabilization")

ax.set_xlabel("time index")
ax.set_ylabel("amplitude")

ax.legend()

plt.tight_layout()
plt.savefig("exp02_root_thread_overlay.png", dpi=300)

# ------------------------------------------------------------
# FINAL
# ------------------------------------------------------------

print("\nGenerated visuals:")
print("-----------------------------------")

print("exp02_offset_transport_geometry.png")
print("exp02_aperture_gate_candidates.png")
print("exp02_routing_angle_distribution.png")
print("exp02_spiral_phase_map.png")
print("exp02_root_thread_overlay.png")

print("\nDONE.")
