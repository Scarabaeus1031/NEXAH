# ============================================================
# EXP_05 — SPLINTER APERTURE PHASE SCAN
# JANUS Rope Operator / Forbidden Corridor Analysis
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from pathlib import Path

# ------------------------------------------------------------
# OUTPUT SETUP
# ------------------------------------------------------------

OUTPUT_DIR = Path(
    "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/"
    "symbolic_layer/janus_rope_operator/outputs/EXP_05"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

N = 26000

pole_x = 1.0
pole_y = 0.0

theta = np.linspace(0, 220*np.pi, N)

# prime offsets
p1 = 2
p2 = 3
p3 = 5
p4 = 7

# ------------------------------------------------------------
# JANUS FIELD
# ------------------------------------------------------------

x = (
    0.62*np.sin(theta/p1)
    + 0.21*np.sin(theta/p2 + np.pi/4)
    + 0.11*np.cos(theta/p3)
)

y = (
    -0.38
    + 0.44*np.cos(theta/p2)
    - 0.28*np.sin(theta/p4)
    - 0.18*np.cos(theta/p1 + np.pi/6)
)

# mild compression
x *= (0.95 - 0.15*np.sin(theta/180))
y *= (0.92 - 0.12*np.cos(theta/160))

# ------------------------------------------------------------
# ANGLE AROUND OFFSET POLE
# ------------------------------------------------------------

dx = x - pole_x
dy = y - pole_y

angles = np.degrees(np.arctan2(dy, dx))
angles = (angles + 360) % 360

# ------------------------------------------------------------
# ANGULAR DENSITY
# ------------------------------------------------------------

bins = np.linspace(0, 360, 721)

hist, edges = np.histogram(
    angles,
    bins=bins,
    density=True
)

hist_smooth = gaussian_filter1d(hist, sigma=4)

bin_centers = 0.5*(edges[:-1] + edges[1:])

# ------------------------------------------------------------
# LOW DENSITY SPLINTERS
# ------------------------------------------------------------

threshold = np.percentile(hist_smooth, 12)

splinter_mask = hist_smooth < threshold

splinter_angles = bin_centers[splinter_mask]

# ------------------------------------------------------------
# FIND SPLINTER CENTERS
# ------------------------------------------------------------

inverse_density = np.max(hist_smooth) - hist_smooth

peaks, _ = find_peaks(
    inverse_density,
    distance=20
)

peak_angles = bin_centers[peaks]
peak_scores = inverse_density[peaks]

# keep strongest
idx = np.argsort(peak_scores)[-8:]

peak_angles = peak_angles[idx]
peak_scores = peak_scores[idx]

# ------------------------------------------------------------
# TRAJECTORY SPLINTER MASK
# ------------------------------------------------------------

traj_mask = np.zeros_like(angles, dtype=bool)

for pa in peak_angles:
    traj_mask |= np.abs(angles - pa) < 4

# ------------------------------------------------------------
# LOCAL ANGULAR DRIFT
# ------------------------------------------------------------

local_std = []

window = 200

for i in range(len(angles)-window):

    seg = angles[i:i+window]

    s = np.std(seg)

    local_std.append(s)

local_std = np.array(local_std)

# ------------------------------------------------------------
# VISUAL 1
# SPLINTER FIELD
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,10))

ax.scatter(
    x,
    y,
    s=1,
    c="lightgrey",
    alpha=0.18
)

sc = ax.scatter(
    x[traj_mask],
    y[traj_mask],
    c=angles[traj_mask],
    s=4,
    cmap="plasma"
)

ax.scatter(
    pole_x,
    pole_y,
    marker="x",
    s=320,
    linewidths=4
)

ax.set_title(
    "EXP_05 — Splinter Aperture Field",
    fontsize=18
)

ax.set_xlabel("x")
ax.set_ylabel("y")

plt.colorbar(sc, label="wrap angle")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp05_splinter_field.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# VISUAL 2
# FORBIDDEN ANGLE DENSITY
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14,6))

ax.plot(
    bin_centers,
    hist_smooth,
    linewidth=3
)

for pa in peak_angles:

    ax.axvline(
        pa,
        linestyle="--",
        alpha=0.7
    )

ax.fill_between(
    bin_centers,
    hist_smooth,
    where=splinter_mask,
    alpha=0.35
)

ax.set_xlim(0,360)

ax.set_title(
    "EXP_05 — Forbidden Splinter Corridors",
    fontsize=18
)

ax.set_xlabel("angle around offset pole")
ax.set_ylabel("density")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp05_forbidden_splinter_density.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# VISUAL 3
# PERSISTENCE / SNAP SCAN
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(15,5))

ax.plot(
    local_std,
    linewidth=1.5
)

ax.set_title(
    "EXP_05 — Angular Snap Persistence",
    fontsize=18
)

ax.set_xlabel("time index")
ax.set_ylabel("local angular std")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp05_snap_persistence_scan.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# VISUAL 4
# SPLINTER OVERLAY
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,10))

sc = ax.scatter(
    x,
    y,
    c=angles,
    s=2,
    cmap="twilight"
)

for pa in peak_angles:

    mask = np.abs(angles - pa) < 2

    ax.scatter(
        x[mask],
        y[mask],
        s=12,
        c="white",
        edgecolors="black",
        linewidths=0.3
    )

ax.scatter(
    pole_x,
    pole_y,
    marker="x",
    s=320,
    linewidths=4
)

ax.set_title(
    "EXP_05 — Splinter Gate Overlay",
    fontsize=18
)

plt.colorbar(sc, label="angle")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp05_splinter_gate_overlay.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# VISUAL 5
# ANGLE HISTOGRAM
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14,6))

ax.hist(
    angles,
    bins=120,
    density=True,
    alpha=0.65
)

for pa in peak_angles:

    ax.axvline(
        pa,
        linestyle="--",
        alpha=0.8
    )

ax.set_xlim(0,360)

ax.set_title(
    "EXP_05 — Angle Distribution + Splinter Gaps",
    fontsize=18
)

ax.set_xlabel("angle")
ax.set_ylabel("density")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "exp05_angle_distribution.png",
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print("\n===================================")
print("EXP_05 — SPLINTER APERTURE SCAN")
print("===================================\n")

print(f"Samples: {N}")
print(f"Detected splinter corridors: {len(peak_angles)}\n")

print("Detected low-density angles:")
print("-----------------------------------")

for pa in np.sort(peak_angles):

    print(f"{pa:.2f}°")

print("\nGenerated visuals:")
print("-----------------------------------")

for f in sorted(OUTPUT_DIR.glob("*.png")):
    print(f.name)

print("\nDONE.\n")
