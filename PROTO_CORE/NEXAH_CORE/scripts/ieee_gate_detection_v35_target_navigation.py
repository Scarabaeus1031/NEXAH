# NEXAH_CORE/scripts/ieee_gate_detection_v35_target_navigation.py
#
# V35 — Target-Based Navigation (NEXAH)
#
# Goal:
# Move from "avoid risk" → "seek stability"
#
# Core idea:
#   steering = -∇P(IOTA)  +  attraction_to_target
#
# Output:
#   outputs/ieee_gates/v35_target_field.png
#   outputs/ieee_gates/v35_target_trajectory.png

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.interpolate import RegularGridInterpolator

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

np.random.seed(42)

N = 1000
TRANSITION_POINT = 600

OUTPUT_DIR = "NEXAH_CORE/outputs/ieee_gates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUT_FIELD = os.path.join(OUTPUT_DIR, "v35_target_field.png")
OUT_TRAJ = os.path.join(OUTPUT_DIR, "v35_target_trajectory.png")

BINS_THETA = 90
BINS_R = 60

STEER_STRENGTH = 0.12
TARGET_STRENGTH = 0.08

STEER_START = TRANSITION_POINT
IOTA_PERCENTILE = 98

# --------------------------------------------------
# SIGNAL (Test / Replace with real data)
# --------------------------------------------------

theta = np.linspace(0, 300, N)
r = 0.5 + 0.5 * np.sin(0.15 * theta)

noise = np.random.normal(0, 0.55, size=N)
r[TRANSITION_POINT:] += noise[TRANSITION_POINT:]

# --------------------------------------------------
# DERIVATIVES
# --------------------------------------------------

dr_dtheta = np.gradient(r) / (np.gradient(theta) + 1e-8)

# --------------------------------------------------
# DENSITY FIELD
# --------------------------------------------------

H, theta_edges, r_edges = np.histogram2d(theta, r, bins=[BINS_THETA, BINS_R])
H_smooth = gaussian_filter(H, sigma=2)

theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2
r_centers = (r_edges[:-1] + r_edges[1:]) / 2

# --------------------------------------------------
# POINT DENSITY → GREYSPACE
# --------------------------------------------------

density_vals = []
for t, rv in zip(theta, r):
    xi = np.searchsorted(theta_edges, t) - 1
    yi = np.searchsorted(r_edges, rv) - 1
    if 0 <= xi < BINS_THETA and 0 <= yi < BINS_R:
        density_vals.append(H_smooth[xi, yi])
    else:
        density_vals.append(0)

density_vals = np.array(density_vals)

greyspace = 1 / (density_vals + 1e-3)
greyspace = (greyspace - greyspace.min()) / (greyspace.max() - greyspace.min())

# --------------------------------------------------
# IOTA PROBABILITY FIELD
# --------------------------------------------------

threshold = np.percentile(np.abs(dr_dtheta), IOTA_PERCENTILE)
iota_mask = np.abs(dr_dtheta) > threshold

# build field
P_field = np.zeros_like(H_smooth)

for t, rv, m in zip(theta, r, iota_mask):
    if m:
        xi = np.searchsorted(theta_edges, t) - 1
        yi = np.searchsorted(r_edges, rv) - 1
        if 0 <= xi < BINS_THETA and 0 <= yi < BINS_R:
            P_field[xi, yi] += 1

P_field = gaussian_filter(P_field, sigma=2)
P_field = P_field / (P_field.max() + 1e-8)

# --------------------------------------------------
# GRADIENT FIELD
# --------------------------------------------------

grad_theta, grad_r = np.gradient(P_field)

interp_grad_theta = RegularGridInterpolator(
    (theta_centers, r_centers), grad_theta, bounds_error=False, fill_value=0
)
interp_grad_r = RegularGridInterpolator(
    (theta_centers, r_centers), grad_r, bounds_error=False, fill_value=0
)

# --------------------------------------------------
# TARGET REGION (NEW 🔥)
# --------------------------------------------------

# define stable basin = low risk + moderate r
target_mask = (P_field < 0.2)

target_coords = []
for i in range(len(theta_centers)):
    for j in range(len(r_centers)):
        if target_mask[i, j]:
            target_coords.append([theta_centers[i], r_centers[j]])

target_coords = np.array(target_coords)

target_center = np.mean(target_coords, axis=0)

# --------------------------------------------------
# STEERING
# --------------------------------------------------

r_s = r.copy()

for i in range(STEER_START, N - 1):

    point = np.array([theta[i], r_s[i]])

    grad = np.array([
        float(interp_grad_theta(point)),
        float(interp_grad_r(point))
    ])

    # repel from risk
    steer_risk = -grad

    # attract to target
    direction_to_target = target_center - point
    steer_target = direction_to_target / (np.linalg.norm(direction_to_target) + 1e-8)

    # combined steering
    total_steer = STEER_STRENGTH * steer_risk + TARGET_STRENGTH * steer_target

    r_s[i + 1] = r_s[i + 1] + total_steer[1]

# --------------------------------------------------
# VISUAL 1 — FIELD
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.imshow(
    P_field.T,
    origin="lower",
    extent=[theta_centers.min(), theta_centers.max(), r_centers.min(), r_centers.max()],
    aspect="auto",
    cmap="viridis"
)

plt.scatter(theta[iota_mask], r[iota_mask], c="red", s=60, label="IOTA")

plt.scatter(target_center[0], target_center[1], c="white", s=120, label="target")

plt.axvline(x=theta[TRANSITION_POINT], linestyle="--", color="black")

plt.colorbar(label="P(IOTA)")
plt.legend()
plt.title("V35 — Target Field")

plt.tight_layout()
plt.savefig(OUT_FIELD, dpi=150)

# --------------------------------------------------
# VISUAL 2 — TRAJECTORY
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(theta, r, color="grey", alpha=0.5, label="original")
plt.plot(theta, r_s, color="blue", linewidth=2, label="steered")

plt.scatter(theta[iota_mask], r[iota_mask], c="red", s=60)

plt.axvline(x=theta[TRANSITION_POINT], linestyle="--", color="black")

plt.legend()
plt.title("V35 — Target Navigation")

plt.tight_layout()
plt.savefig(OUT_TRAJ, dpi=150)

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print("\n--- V35 RESULTS ---")
print(f"IOTA events: {np.sum(iota_mask)}")
print(f"Target center: theta={target_center[0]:.2f}, r={target_center[1]:.2f}")
print(f"Steering: risk + target")
