# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v36_adaptive_target_navigation.py
#
# V36 — Adaptive Target Navigation (NEXAH)
#
# Goal:
# Move from fixed target steering to adaptive target selection.
#
# Core idea:
#   At each step:
#   1. estimate current risk P(IOTA)
#   2. search nearby low-risk basin
#   3. steer away from risk gradient
#   4. steer toward local adaptive target
#
# Output:
#   outputs/ieee_gates/v36_adaptive_target_field.png
#   outputs/ieee_gates/v36_adaptive_target_trajectory.png
#   outputs/ieee_gates/v36_risk_comparison.png

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

OUT_FIELD = os.path.join(OUTPUT_DIR, "v36_adaptive_target_field.png")
OUT_TRAJ = os.path.join(OUTPUT_DIR, "v36_adaptive_target_trajectory.png")
OUT_RISK = os.path.join(OUTPUT_DIR, "v36_risk_comparison.png")

BINS_THETA = 90
BINS_R = 60

IOTA_PERCENTILE = 98

STEER_START = TRANSITION_POINT
STEER_STRENGTH = 0.10
TARGET_STRENGTH = 0.14

LOCAL_THETA_RADIUS = 25.0
LOCAL_R_RADIUS = 0.8

RISK_SAFE_THRESHOLD = 0.25

# --------------------------------------------------
# SIGNAL / TEST DATA
# --------------------------------------------------

theta = np.linspace(0, 300, N)
r = 0.5 + 0.5 * np.sin(0.15 * theta)

noise = np.random.normal(0, 0.55, size=N)
r[TRANSITION_POINT:] += noise[TRANSITION_POINT:]

# --------------------------------------------------
# DERIVATIVES + IOTA EVENTS
# --------------------------------------------------

dr_dtheta = np.gradient(r) / (np.gradient(theta) + 1e-8)

iota_threshold = np.percentile(np.abs(dr_dtheta), IOTA_PERCENTILE)
iota_mask = np.abs(dr_dtheta) > iota_threshold
iota_idx = np.where(iota_mask)[0]

# --------------------------------------------------
# DENSITY FIELD
# --------------------------------------------------

H, theta_edges, r_edges = np.histogram2d(
    theta,
    r,
    bins=[BINS_THETA, BINS_R],
)

H_smooth = gaussian_filter(H, sigma=2)

theta_centers = (theta_edges[:-1] + theta_edges[1:]) / 2
r_centers = (r_edges[:-1] + r_edges[1:]) / 2

# --------------------------------------------------
# POINTWISE GREYSPACE
# --------------------------------------------------

def bin_index(th, rr):
    ti = np.searchsorted(theta_edges, th) - 1
    ri = np.searchsorted(r_edges, rr) - 1
    ti = np.clip(ti, 0, BINS_THETA - 1)
    ri = np.clip(ri, 0, BINS_R - 1)
    return ti, ri

density_vals = []
for th, rr in zip(theta, r):
    ti, ri = bin_index(th, rr)
    density_vals.append(H_smooth[ti, ri])

density_vals = np.array(density_vals)

density_norm = (density_vals - density_vals.min()) / (
    density_vals.max() - density_vals.min() + 1e-8
)

greyspace = 1.0 - density_norm

flow_score = np.abs(dr_dtheta)
flow_score = (flow_score - flow_score.min()) / (
    flow_score.max() - flow_score.min() + 1e-8
)

# --------------------------------------------------
# P(IOTA) GRID
# --------------------------------------------------

P_points = 0.55 * flow_score + 0.45 * greyspace
P_points = (P_points - P_points.min()) / (
    P_points.max() - P_points.min() + 1e-8
)

P_grid = np.zeros_like(H_smooth)
C_grid = np.zeros_like(H_smooth)

for th, rr, pp in zip(theta, r, P_points):
    ti, ri = bin_index(th, rr)
    P_grid[ti, ri] += pp
    C_grid[ti, ri] += 1

mask = C_grid > 0
P_grid[mask] /= C_grid[mask]

P_grid = gaussian_filter(P_grid, sigma=2)
P_grid = (P_grid - P_grid.min()) / (
    P_grid.max() - P_grid.min() + 1e-8
)

# --------------------------------------------------
# GRADIENT FIELD
# --------------------------------------------------

dP_dtheta, dP_dr = np.gradient(P_grid)

risk_interp = RegularGridInterpolator(
    (theta_centers, r_centers),
    P_grid,
    bounds_error=False,
    fill_value=1.0,
)

grad_theta_interp = RegularGridInterpolator(
    (theta_centers, r_centers),
    dP_dtheta,
    bounds_error=False,
    fill_value=0.0,
)

grad_r_interp = RegularGridInterpolator(
    (theta_centers, r_centers),
    dP_dr,
    bounds_error=False,
    fill_value=0.0,
)

# --------------------------------------------------
# ADAPTIVE TARGET SELECTION
# --------------------------------------------------

TT, RR = np.meshgrid(theta_centers, r_centers, indexing="ij")
grid_points = np.column_stack([TT.ravel(), RR.ravel()])
grid_risk = P_grid.ravel()

def adaptive_target(current_theta, current_r):
    dtheta = np.abs(grid_points[:, 0] - current_theta)
    dr = np.abs(grid_points[:, 1] - current_r)

    local_mask = (
        (dtheta <= LOCAL_THETA_RADIUS)
        &
        (dr <= LOCAL_R_RADIUS)
        &
        (grid_risk <= RISK_SAFE_THRESHOLD)
    )

    if np.any(local_mask):
        candidates = grid_points[local_mask]
        candidate_risk = grid_risk[local_mask]

        # prefer low risk and nearby points
        dist = np.sqrt(
            (candidates[:, 0] - current_theta) ** 2
            +
            (candidates[:, 1] - current_r) ** 2
        )

        score = candidate_risk + 0.02 * dist
        best = np.argmin(score)

        return candidates[best]

    # fallback: globally safest point
    best_global = np.argmin(grid_risk)
    return grid_points[best_global]

# --------------------------------------------------
# ADAPTIVE STEERING
# --------------------------------------------------

theta_s = theta.copy()
r_s = r.copy()

target_history = []
risk_original = []
risk_steered = []

for i in range(STEER_START, N - 1):
    current = np.array([theta_s[i], r_s[i]])

    risk_original.append(float(risk_interp([theta[i], r[i]])))
    risk_steered.append(float(risk_interp(current)))

    grad = np.array([
        float(grad_theta_interp(current)),
        float(grad_r_interp(current)),
    ])

    grad_norm = np.linalg.norm(grad) + 1e-8
    risk_avoid = -grad / grad_norm

    target = adaptive_target(current[0], current[1])
    target_history.append(target)

    to_target = target - current
    to_target_norm = np.linalg.norm(to_target) + 1e-8
    target_pull = to_target / to_target_norm

    # adaptive strength: stronger correction in high-risk zones
    current_risk = float(risk_interp(current))
    adaptive_gain = 0.5 + current_risk

    total_steer = adaptive_gain * (
        STEER_STRENGTH * risk_avoid
        +
        TARGET_STRENGTH * target_pull
    )

    # mostly steer radius; allow slight theta correction
    theta_s[i + 1] = theta_s[i + 1] + 0.15 * total_steer[0]
    r_s[i + 1] = r_s[i + 1] + total_steer[1]

    r_s[i + 1] = np.clip(r_s[i + 1], r_centers.min(), r_centers.max())

target_history = np.array(target_history)
risk_original = np.array(risk_original)
risk_steered = np.array(risk_steered)

# --------------------------------------------------
# VISUAL 1 — FIELD + ADAPTIVE TARGETS
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.imshow(
    P_grid.T,
    origin="lower",
    extent=[
        theta_centers.min(),
        theta_centers.max(),
        r_centers.min(),
        r_centers.max(),
    ],
    aspect="auto",
    cmap="viridis",
)

plt.colorbar(label="P(IOTA)")

plt.scatter(theta[iota_idx], r[iota_idx], c="red", s=60, label="IOTA")

if len(target_history) > 0:
    plt.scatter(
        target_history[:, 0],
        target_history[:, 1],
        c="white",
        s=10,
        alpha=0.65,
        label="adaptive targets",
    )

plt.axvline(theta[TRANSITION_POINT], linestyle="--", color="black", label="transition")

plt.title("V36 — Adaptive Target Field")
plt.xlabel("theta")
plt.ylabel("r")
plt.legend()
plt.grid(alpha=0.25)

plt.tight_layout()
plt.savefig(OUT_FIELD, dpi=150)
plt.close()

# --------------------------------------------------
# VISUAL 2 — TRAJECTORY
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(theta, r, color="grey", alpha=0.45, label="original")
plt.plot(theta_s, r_s, color="blue", linewidth=2.0, label="adaptive steered")

plt.scatter(theta[iota_idx], r[iota_idx], c="red", s=60, label="IOTA")

if len(target_history) > 0:
    plt.scatter(
        target_history[:, 0],
        target_history[:, 1],
        c="cyan",
        s=8,
        alpha=0.5,
        label="target trail",
    )

plt.axvline(theta[TRANSITION_POINT], linestyle="--", color="black", label="transition")

plt.title("V36 — Adaptive Target Navigation")
plt.xlabel("theta")
plt.ylabel("r")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_TRAJ, dpi=150)
plt.close()

# --------------------------------------------------
# VISUAL 3 — RISK COMPARISON
# --------------------------------------------------

plt.figure(figsize=(12, 5))

plt.plot(risk_original, color="red", linewidth=2, label="original risk")
plt.plot(risk_steered, color="blue", linewidth=2, label="adaptive steered risk")

plt.title("V36 — Original vs Adaptive-Steered Risk")
plt.xlabel("step after steering start")
plt.ylabel("P(IOTA)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(OUT_RISK, dpi=150)
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

mean_orig = float(np.mean(risk_original))
mean_steered = float(np.mean(risk_steered))
reduction = mean_orig - mean_steered
reduction_pct = 100 * reduction / (mean_orig + 1e-8)

print("\n--- V36 RESULTS ---")
print(f"IOTA events: {len(iota_idx)}")
print(f"Adaptive targets used: {len(target_history)}")
print(f"Mean original risk: {mean_orig:.4f}")
print(f"Mean steered risk:  {mean_steered:.4f}")
print(f"Risk reduction:     {reduction:.4f}")
print(f"Risk reduction %:   {reduction_pct:.2f}%")
print("")
print("Saved:")
print(OUT_FIELD)
print(OUT_TRAJ)
print(OUT_RISK)
