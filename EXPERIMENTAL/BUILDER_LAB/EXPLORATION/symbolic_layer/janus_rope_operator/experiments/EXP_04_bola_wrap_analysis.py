# ============================================================
# EXP_04 — FORBIDDEN ANGLE / BOLA WRAP ANALYSIS
# JANUS ROPE OPERATOR
#
# Goal:
# Detect preferred vs forbidden wrapping angles
# around an offset pole ("bola mechanics")
#
# Hypothesis:
# Prime drift creates:
# - stable wrap corridors
# - forbidden angular gaps
# - asymmetric transport folds
#
# Outputs:
# 1. Forbidden angle density map
# 2. Wrap trajectory geometry
# 3. Angular persistence scan
# 4. Pole winding histogram
# 5. Stable corridor extraction
#
# Save path:
# EXPERIMENTAL/BUILDER_LAB/EXPLORATION/
# symbolic_layer/janus_rope_operator/outputs/
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from pathlib import Path

# ------------------------------------------------------------
# OUTPUT DIRECTORY
# ------------------------------------------------------------

OUTPUT_DIR = Path(
    "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/"
    "symbolic_layer/janus_rope_operator/outputs"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

N = 22000
t = np.linspace(0, 180*np.pi, N)

# prime drift frequencies
f1 = 2
f2 = 3
f3 = 5
f4 = 7

# symbolic constants
phi = (1 + np.sqrt(5)) / 2
root2 = np.sqrt(2)
pi = np.pi

# offset pole
pole_x = 1.0
pole_y = 0.0

# ------------------------------------------------------------
# ROPE SYSTEM
# ------------------------------------------------------------

x = (
    0.45*np.sin(f1*t)
    + 0.30*np.sin(f2*t/phi)
    + 0.22*np.sin(f3*t/pi)
    + 0.12*np.sin(f4*t/root2)
)

y = (
    -0.35
    + 0.30*np.cos(f2*t/pi)
    + 0.22*np.cos(f3*t/root2)
    + 0.12*np.cos(f4*t/phi)
)

# ------------------------------------------------------------
# ANGLE AROUND OFFSET POLE
# ------------------------------------------------------------

dx = x - pole_x
dy = y - pole_y

angles = np.degrees(np.arctan2(dy, dx))
angles = (angles + 360) % 360

# ------------------------------------------------------------
# ANGULAR VELOCITY
# ------------------------------------------------------------

dtheta = np.gradient(angles)

# unwrap for winding analysis
theta_unwrapped = np.unwrap(np.radians(angles))
winding = theta_unwrapped / (2*np.pi)

# ------------------------------------------------------------
# HISTOGRAM ANALYSIS
# ------------------------------------------------------------

bins = np.linspace(0, 360, 180)
hist, edges = np.histogram(angles, bins=bins, density=True)

smooth_hist = gaussian_filter1d(hist, sigma=2)

# forbidden zones = low density
threshold = np.percentile(smooth_hist, 18)

forbidden_mask = smooth_hist < threshold
stable_mask = smooth_hist > np.percentile(smooth_hist, 80)

centers = 0.5 * (edges[:-1] + edges[1:])

# ------------------------------------------------------------
# FIGURE 1
# Forbidden Angle Density
# ------------------------------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(centers, smooth_hist, lw=2)

plt.fill_between(
    centers,
    smooth_hist,
    where=forbidden_mask,
    alpha=0.35,
    label="forbidden angle zones"
)

plt.fill_between(
    centers,
    smooth_hist,
    where=stable_mask,
    alpha=0.35,
    label="stable corridors"
)

plt.xlabel("angle around offset pole (deg)")
plt.ylabel("density")
plt.title("EXP_04 — Forbidden Angle Corridors")
plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp04_forbidden_angle_corridors.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# FIGURE 2
# Wrap Geometry
# ------------------------------------------------------------

plt.figure(figsize=(10, 10))

sc = plt.scatter(
    x,
    y,
    c=angles,
    s=3,
    cmap="twilight"
)

plt.scatter(
    pole_x,
    pole_y,
    s=300,
    marker="x",
    linewidths=3,
    label="offset pole"
)

plt.colorbar(sc, label="wrap angle")

plt.axis("equal")
plt.title("EXP_04 — Bola Wrap Geometry")
plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp04_bola_wrap_geometry.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# FIGURE 3
# Angular Persistence
# ------------------------------------------------------------

window = 250

persistence = []

for i in range(N - window):
    local_std = np.std(angles[i:i+window])
    persistence.append(local_std)

persistence = np.array(persistence)

plt.figure(figsize=(14, 5))

plt.plot(persistence)

plt.xlabel("time index")
plt.ylabel("local angular std")
plt.title("EXP_04 — Angular Persistence Scan")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp04_angular_persistence_scan.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# FIGURE 4
# Winding Count
# ------------------------------------------------------------

plt.figure(figsize=(14, 5))

plt.plot(winding, lw=1.2)

plt.xlabel("time index")
plt.ylabel("pole winding count")

plt.title("EXP_04 — Pole Winding Evolution")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp04_pole_winding_evolution.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# FIGURE 5
# Stable Transport Corridors
# ------------------------------------------------------------

stable_points = stable_mask[
    np.digitize(angles, edges[:-1], right=True) - 1
]

plt.figure(figsize=(10, 10))

plt.scatter(
    x,
    y,
    s=1,
    alpha=0.08,
    color="gray"
)

plt.scatter(
    x[stable_points],
    y[stable_points],
    s=5,
    c=angles[stable_points],
    cmap="plasma"
)

plt.scatter(
    pole_x,
    pole_y,
    s=300,
    marker="x",
    linewidths=3
)

plt.axis("equal")

plt.title("EXP_04 — Stable Transport Corridors")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp04_stable_transport_corridors.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# CONSOLE OUTPUT
# ------------------------------------------------------------

print()
print("===================================")
print("EXP_04 — FORBIDDEN ANGLE ANALYSIS")
print("===================================")
print()

print(f"Samples: {N}")
print()

print(f"Mean angle: {np.mean(angles):.3f}°")
print(f"Std angle: {np.std(angles):.3f}°")
print()

print(f"Forbidden threshold: {threshold:.6f}")
print()

print("Generated visuals:")
print("-----------------------------------")

files = [
    "exp04_forbidden_angle_corridors.png",
    "exp04_bola_wrap_geometry.png",
    "exp04_angular_persistence_scan.png",
    "exp04_pole_winding_evolution.png",
    "exp04_stable_transport_corridors.png"
]

for f in files:
    print(f)

print()
print("DONE.")
print()
