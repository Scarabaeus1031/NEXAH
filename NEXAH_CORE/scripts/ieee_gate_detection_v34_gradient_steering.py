# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v34_gradient_steering.py
#
# V34 — NEXAH Gradient Steering
#
# Goal:
# Build first navigation layer:
#
#   P(IOTA | r, theta)  ->  gradient field  ->  steering vector
#
# Core idea:
#   Move away from high-risk IOTA regions.
#
# Output:
#   outputs/ieee_gates/v34_gradient_field.png
#   outputs/ieee_gates/v34_steered_trajectory.png

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

OUTPUT_DIR = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUT_FIELD = os.path.join(OUTPUT_DIR, "v34_gradient_field.png")
OUT_TRAJ = os.path.join(OUTPUT_DIR, "v34_steered_trajectory.png")

BINS_THETA = 90
BINS_R = 60

STEER_STRENGTH = 0.15
STEER_START = TRANSITION_POINT
IOTA_PERCENTILE = 98

# --------------------------------------------------
# SIGNAL / TEST DATA
# --------------------------------------------------

theta = np.linspace(0, 300, N)
r = 0.5 + 0.5 * np.sin(0.15 * theta)

noise = np.random.normal(0, 0.55, size=N)
r[TRANSITION_POINT:] += noise[TRANSITION_POINT:]

# --------------------------------------------------
# DERIVATIVES + IOTA DETECTION
# --------------------------------------------------

dr_dtheta = np.gradient(r) / (np.gradient(theta) + 1e-8)

threshold = np.percentile(np.abs(dr_dtheta), IOTA_PERCENTILE)
iota_indices = np.where(np.abs(dr_dtheta) > threshold)[0]

# --------------------------------------------------
# DENSITY FIELD → P(IOTA)
# --------------------------------------------------

H, theta_edges, r_edges = np.histogram2d(
    theta, r, bins=[BINS_THETA, BINS_R]
)

H_smooth = gaussian_filter(H, sigma=2)

theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2
r_centers = (r_edges[:-1] + r_edges[1:]) / 2

# density lookup
density_vals = []

for t, rr in zip(theta, r):
    xi = np.searchsorted(theta_edges, t) - 1
    yi = np.searchsorted(r_edges, rr) - 1

    if 0 <= xi < BINS_THETA and 0 <= yi < BINS_R:
        density_vals.append(H_smooth[xi, yi])
    else:
        density_vals.append(0)

density_vals = np.array(density_vals)

# inverse density → greyspace
P = 1 / (density_vals + 1e-3)

# normalize
P = (P - P.min()) / (P.max() - P.min() + 1e-8)

# --------------------------------------------------
# GRID VERSION OF P
# --------------------------------------------------

P_grid = gaussian_filter(H_smooth, sigma=2)
P_grid = 1 / (P_grid + 1e-3)
P_grid = (P_grid - P_grid.min()) / (P_grid.max() - P_grid.min() + 1e-8)

# --------------------------------------------------
# GRADIENT FIELD
# --------------------------------------------------

dP_dtheta, dP_dr = np.gradient(P_grid)

# interpolators
interp_P = RegularGridInterpolator(
    (theta_centers, r_centers), P_grid, bounds_error=False, fill_value=0
)

interp_dtheta = RegularGridInterpolator(
    (theta_centers, r_centers), dP_dtheta, bounds_error=False, fill_value=0
)

interp_dr = RegularGridInterpolator(
    (theta_centers, r_centers), dP_dr, bounds_error=False, fill_value=0
)

# --------------------------------------------------
# STEERING SIMULATION
# --------------------------------------------------

theta_s = theta.copy()
r_s = r.copy()

for i in range(STEER_START, N - 1):

    point = np.array([theta_s[i], r_s[i]])

    grad_theta = interp_dtheta(point)
    grad_r = interp_dr(point)

    grad = np.array([grad_theta, grad_r])

    # normalize
    norm = np.linalg.norm(grad) + 1e-8
    grad = grad / norm

    # steer opposite gradient (away from risk)
    r_s[i + 1] = r_s[i + 1] - STEER_STRENGTH * grad[1]

# --------------------------------------------------
# VISUAL 1 — GRADIENT FIELD
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.scatter(theta, r, c=P, cmap="viridis", s=10)
plt.colorbar(label="P(IOTA)")

plt.scatter(theta[iota_indices], r[iota_indices], c="red", s=80, label="IOTA")

plt.axvline(x=theta[TRANSITION_POINT], linestyle="--", color="black", label="transition")

plt.title("V34 — IOTA Probability Field")
plt.xlabel("theta")
plt.ylabel("r")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig(OUT_FIELD, dpi=150)
plt.close()

# --------------------------------------------------
# VISUAL 2 — STEERED TRAJECTORY
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(theta, r, color="grey", alpha=0.5, label="original")
plt.plot(theta_s, r_s, color="blue", linewidth=2, label="steered")

plt.scatter(theta[iota_indices], r[iota_indices], c="red", s=80)

plt.axvline(x=theta[TRANSITION_POINT], linestyle="--", color="black")

plt.title("V34 — Gradient Steering Trajectory")
plt.xlabel("theta")
plt.ylabel("r")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig(OUT_TRAJ, dpi=150)
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print("\n--- V34 RESULTS ---")
print(f"IOTA events: {len(iota_indices)}")
print(f"Steering strength: {STEER_STRENGTH}")
print(f"Steering start index: {STEER_START}")
