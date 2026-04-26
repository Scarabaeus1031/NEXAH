# ============================================================
# NEXAH — IEEE GATE DETECTION v79
# Multi-Operator Control (π + φ + √2) — FIXED
# ============================================================
#
# FILE:
# ieee_gate_detection_v79_multi_operator_control.py
#
# PURPOSE:
# --------
# Extend v78 with:
#   π      → smooth rotation
#   φ      → radial drift (escape loops)
#   √2     → sheet transitions
#
# CRITICAL FIX:
# -------------
# v79 now uses SEQUENTIAL TARGETS:
#
#   Start → Gate1 → Gate2 → Target
#
# instead of jumping directly to target.
#
# OUTPUTS:
# --------
# v79_control.png
# v79_turning.png
# v79_sheet_profile.png
# v79_summary.txt
#
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

k_theta = 0.8
k_phi   = 0.7
k_sqrt  = 0.5

dt = 0.05
steps = 500

# TARGET (final)
theta_target = 0.8
r_target = 0.9

# INITIAL STATE
theta = -2.5
r = 1.1

# SHEETS
sheet_centers = np.array([0.54, 0.86, 1.20, 1.60, 1.99])

# GATES
gates = [
    (-1.3, 1.6),
    (0.8, 0.9)
]

gate_threshold = 0.18

# Build full path
targets = gates + [(theta_target, r_target)]
current_target_index = 0

# ------------------------------------------------------------
# LOGS
# ------------------------------------------------------------

theta_path = []
r_path = []
sheet_path = []
turning_profile = []
target_index_log = []

reached_gates = 0

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi

def get_sheet_index(r):
    return np.argmin(np.abs(sheet_centers - r))

def near_sheet_boundary(r):
    return np.min(np.abs(sheet_centers - r)) < 0.08

def dist(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------

for step in range(steps):

    # CURRENT TARGET
    t_theta, t_r = targets[current_target_index]

    # ANGLE ERROR
    dtheta = wrap_angle(t_theta - theta)

    # π CONTROL (rotation)
    u_pi = -k_theta * dtheta

    # φ CONTROL (radial drift)
    r_error = t_r - r
    u_phi = k_phi * np.sign(r_error) * np.sqrt(abs(r_error) + 1e-6)

    # √2 CONTROL (sheet transition)
    sheet_idx = get_sheet_index(r)
    next_sheet = min(sheet_idx + 1, len(sheet_centers)-1)
    r_sheet_next = sheet_centers[next_sheet]

    u_sheet = k_sqrt * (r_sheet_next - r)

    # --------------------------------------------------------
    # DYNAMIC WEIGHTS
    # --------------------------------------------------------

    w_phi = min(1.0, abs(r_error))
    w_sqrt = 1.0 if near_sheet_boundary(r) else 0.1
    w_pi = max(0.0, 1.0 - w_phi - w_sqrt)

    # normalize
    total = w_pi + w_phi + w_sqrt + 1e-8
    w_pi /= total
    w_phi /= total
    w_sqrt /= total

    # FINAL CONTROL
    u = w_pi * u_pi + w_phi * u_phi + w_sqrt * u_sheet

    # --------------------------------------------------------
    # UPDATE STATE
    # --------------------------------------------------------

    theta += u * dt
    r += u_phi * dt

    # --------------------------------------------------------
    # TARGET / GATE TRANSITION
    # --------------------------------------------------------

    if current_target_index < len(targets):
        if dist((theta, r), (t_theta, t_r)) < gate_threshold:
            current_target_index += 1
            reached_gates += 1

            if current_target_index >= len(targets):
                break

    # --------------------------------------------------------
    # LOGGING
    # --------------------------------------------------------

    theta_path.append(theta)
    r_path.append(r)
    sheet_path.append(get_sheet_index(r))
    turning_profile.append(u)
    target_index_log.append(current_target_index)

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

final_dist = dist((theta, r), (theta_target, r_target))

print("NEXAH v79 complete")
print(f"Reached gates: {reached_gates}/{len(gates)}")
print(f"Final distance: {final_dist:.6f}")

# ------------------------------------------------------------
# OUTPUT FOLDER
# ------------------------------------------------------------

OUT_DIR = "outputs/ieee_gates"
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# PLOT 1: TRAJECTORY
# ------------------------------------------------------------

plt.figure(figsize=(8,6))
plt.plot(theta_path, r_path, color="red", linewidth=2)

# plot gates
for gt, gr in gates:
    plt.scatter(gt, gr, color="black", s=80)

# target
plt.scatter(theta_target, r_target, color="blue", s=120)

plt.xlabel("theta")
plt.ylabel("r")
plt.title("NEXAH v79 — Multi-Operator Control")

plt.tight_layout()
plt.savefig(f"{OUT_DIR}/v79_control.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# PLOT 2: TURNING
# ------------------------------------------------------------

plt.figure(figsize=(8,4))
plt.plot(turning_profile)
plt.title("Turning Profile")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/v79_turning.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# PLOT 3: SHEETS
# ------------------------------------------------------------

plt.figure(figsize=(8,4))
plt.step(range(len(sheet_path)), sheet_path, where="post")
plt.title("Sheet Index")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/v79_sheet_profile.png", dpi=200)
plt.close()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

with open(f"{OUT_DIR}/v79_summary.txt", "w") as f:
    f.write("NEXAH v79 — Multi-Operator Control\n")
    f.write("=================================\n\n")
    f.write(f"Reached gates: {reached_gates}/{len(gates)}\n")
    f.write(f"Final distance: {final_dist:.6f}\n")

print("Saved outputs to:", OUT_DIR)
