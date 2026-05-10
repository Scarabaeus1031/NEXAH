# ============================================================
# EXP_03 — Dual Layer Mirror Routing
# JANUS Rope Operator
#
# Goal:
# Explore the dual-band transport structure:
#
#   1. golden carrier band
#   2. dark return crescent
#
# with:
# - offset pole routing
# - prime drift
# - mirrored transport layers
# - phase hysteresis
#
# Output:
# - dual transport geometry
# - mirror return flow
# - hysteresis routing map
# - transport density map
# - layer synchronization scan
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

N = 18000
t = np.linspace(0, 240*np.pi, N)

# prime drift frequencies
p1 = 7
p2 = 11
p3 = 13
p4 = 17

# irrational regulators
phi = (1 + np.sqrt(5)) / 2
root2 = np.sqrt(2)
pi = np.pi

# offset pole
pole_x = 1.0
pole_y = 0.0

# ------------------------------------------------------------
# ROPE THREADS
# ------------------------------------------------------------

r1 = np.sin(t * p1 / phi)
r2 = np.cos(t * p2 / pi)

r3 = np.sin(t * p3 / root2)
r4 = np.cos(t * p4 / phi)

# root thread
root_thread = (
    0.55 * np.sin(t / phi)
    + 0.35 * np.cos(t / root2)
    + 0.20 * np.sin(t / pi)
)

# ------------------------------------------------------------
# PRIMARY TRANSPORT FIELD
# ------------------------------------------------------------

x_main = (
    0.45 * r1
    + 0.35 * r2
    + 0.15 * root_thread
)

y_main = (
    0.45 * r3
    + 0.35 * r4
    - 0.25
)

# ------------------------------------------------------------
# OFFSET ROUTING
# ------------------------------------------------------------

dx = x_main - pole_x
dy = y_main - pole_y

theta = np.arctan2(dy, dx)
radius = np.sqrt(dx**2 + dy**2)

# ------------------------------------------------------------
# MIRROR RETURN LAYER
# ------------------------------------------------------------

mirror_x = (
    x_main
    - 0.28 * np.cos(2 * theta)
)

mirror_y = (
    -y_main
    - 0.18 * np.sin(3 * theta)
)

# ------------------------------------------------------------
# HYSTERESIS ROUTING
# ------------------------------------------------------------

memory_shift = np.roll(theta, 120)

transport_x = (
    x_main
    + 0.18 * np.sin(memory_shift)
)

transport_y = (
    y_main
    + 0.18 * np.cos(memory_shift)
)

# ------------------------------------------------------------
# DENSITY ESTIMATION
# ------------------------------------------------------------

density = (
    np.sin(2 * theta)
    + np.cos(3 * radius)
)

# ------------------------------------------------------------
# SYNC ANALYSIS
# ------------------------------------------------------------

sync_score = (
    np.abs(r1*r3)
    + np.abs(r2*r4)
)

# ------------------------------------------------------------
# VISUAL 1
# Dual Layer Transport
# ------------------------------------------------------------

plt.figure(figsize=(10,10))

plt.scatter(
    x_main,
    y_main,
    c=theta,
    cmap="viridis",
    s=2,
    alpha=0.75,
    label="carrier layer"
)

plt.scatter(
    mirror_x,
    mirror_y,
    c=theta,
    cmap="magma",
    s=2,
    alpha=0.35,
    label="mirror return"
)

plt.scatter(
    pole_x,
    pole_y,
    marker="x",
    s=250,
    linewidths=3,
    label="offset pole"
)

plt.title("EXP_03 — Dual Layer Mirror Routing")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.legend()

plt.savefig(
    "exp03_dual_layer_transport.png",
    dpi=300,
    bbox_inches="tight"
)

# ------------------------------------------------------------
# VISUAL 2
# Hysteresis Routing
# ------------------------------------------------------------

plt.figure(figsize=(10,10))

plt.scatter(
    transport_x,
    transport_y,
    c=memory_shift,
    cmap="twilight",
    s=2,
    alpha=0.8
)

plt.scatter(
    pole_x,
    pole_y,
    marker="x",
    s=220,
    linewidths=3
)

plt.title("EXP_03 — Hysteresis Routing Map")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")

plt.savefig(
    "exp03_hysteresis_routing.png",
    dpi=300,
    bbox_inches="tight"
)

# ------------------------------------------------------------
# VISUAL 3
# Transport Density
# ------------------------------------------------------------

plt.figure(figsize=(10,10))

plt.scatter(
    transport_x,
    transport_y,
    c=density,
    cmap="plasma",
    s=2,
    alpha=0.85
)

plt.title("EXP_03 — Transport Density Field")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")

plt.savefig(
    "exp03_transport_density.png",
    dpi=300,
    bbox_inches="tight"
)

# ------------------------------------------------------------
# VISUAL 4
# Layer Synchronization
# ------------------------------------------------------------

plt.figure(figsize=(14,5))

plt.plot(sync_score, linewidth=1.2)

plt.title("EXP_03 — Layer Synchronization Scan")
plt.xlabel("time index")
plt.ylabel("sync score")

plt.savefig(
    "exp03_layer_sync_scan.png",
    dpi=300,
    bbox_inches="tight"
)

# ------------------------------------------------------------
# VISUAL 5
# Return Crescent Isolation
# ------------------------------------------------------------

mask = mirror_y < -0.1

plt.figure(figsize=(10,10))

plt.scatter(
    mirror_x[mask],
    mirror_y[mask],
    c=theta[mask],
    cmap="inferno",
    s=3,
    alpha=0.85
)

plt.scatter(
    pole_x,
    pole_y,
    marker="x",
    s=220,
    linewidths=3
)

plt.title("EXP_03 — Return Crescent Structure")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")

plt.savefig(
    "exp03_return_crescent.png",
    dpi=300,
    bbox_inches="tight"
)

# ------------------------------------------------------------
# TERMINAL OUTPUT
# ------------------------------------------------------------

print("\n===================================")
print("EXP_03 — DUAL LAYER MIRROR ROUTING")
print("===================================\n")

print(f"Samples: {N}")
print(f"Mean routing angle: {np.mean(np.degrees(theta)):.3f}°")
print(f"Std routing angle: {np.std(np.degrees(theta)):.3f}°")

print(f"\nMean density: {np.mean(density):.6f}")
print(f"Max density: {np.max(density):.6f}")

print(f"\nMean sync score: {np.mean(sync_score):.6f}")
print(f"Max sync score: {np.max(sync_score):.6f}")

print("\nGenerated visuals:")
print("-----------------------------------")
print("exp03_dual_layer_transport.png")
print("exp03_hysteresis_routing.png")
print("exp03_transport_density.png")
print("exp03_layer_sync_scan.png")
print("exp03_return_crescent.png")

print("\nDONE.")
