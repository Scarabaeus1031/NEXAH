# ============================================================
# NEXAH — IEEE GATE DETECTION v56
# Pattern-Field Control (State-Structured Activation)
# ============================================================
#
# FILE:
# ieee_gate_detection_v56_pattern_field_control.py
#
# PURPOSE:
# --------
# Move from time-based control patterns to state-space patterns.
#
# v52–v53:
#     pattern(t)
#
# v56:
#     pattern(r, θ, basin, structure)
#
# CORE IDEA:
# ----------
# Control is activated in specific geometric regions of state space.
#
# Control follows:
#     - basin structure
#     - distance to centroid
#     - angular bands
#
# RESULT:
# -------
# Control becomes aligned with system geometry instead of time.
#
# OUTPUTS:
# --------
# v56_pattern_field_B{source}_to_B{target}.png
# v56_pattern_field_summary_B{source}_to_B{target}.txt
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control
from ieee_gate_detection_v41_ridge_aligned_control import (
    ridge_aligned_control,
    wrap_theta
)
from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score
from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments
from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids


# ------------------------------------------------------------
# Build baseline pipeline
# ------------------------------------------------------------

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([result["r"], result["theta"]])

    aligned = ridge_aligned_control(
        states,
        result["controls"],
        None,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    L = np.ones(len(aligned)) * 0.5  # fallback if no field used

    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    centroids = compute_basin_centroids(aligned, basin_ids)

    counts, probs, basin_list, segments = compute_transition_matrix_from_segments(
        basin_ids
    )

    return {
        "aligned": aligned,
        "controls": result["controls"],
        "basin_ids": basin_ids,
        "centroids": centroids,
        "transition_probs": probs,
        "basin_list": basin_list,
    }


# ------------------------------------------------------------
# Pattern Field Definition
# ------------------------------------------------------------

def pattern_field_mask(states, basin_ids, centroids, source):

    mask = np.zeros(len(states), dtype=bool)

    c = centroids[source]

    for i, s in enumerate(states):

        if basin_ids[i] != source:
            continue

        r, theta = s

        # --- distance to centroid ---
        dr = r - c[0]
        dtheta = wrap_theta(theta - c[1])
        dist = np.sqrt(dr**2 + dtheta**2)

        # --- angular band (structure pattern) ---
        theta_band = abs(dtheta) < 1.2

        # --- radial shell ---
        radial_band = 0.2 < dist < 1.0

        # --- combined pattern ---
        if theta_band and radial_band:
            mask[i] = True

    return mask


# ------------------------------------------------------------
# Control
# ------------------------------------------------------------

def pattern_field_control(
    states,
    controls,
    basin_ids,
    centroids,
    source,
    target,
    eta=0.02,
    gain=0.065,
    base_gain=0.55,
    max_step=0.055
):

    controlled = states.copy()
    mask = pattern_field_mask(states, basin_ids, centroids, source)

    target_c = centroids[target]

    active = np.zeros(len(states), dtype=bool)

    for i in range(len(states)):

        if not mask[i]:
            continue

        if basin_ids[i] != source:
            continue

        s = controlled[i]

        # base
        u_base = controls[i]

        # target vector
        dr = target_c[0] - s[0]
        dtheta = wrap_theta(target_c[1] - s[1])

        u_target = np.array([dr, dtheta])
        norm = np.linalg.norm(u_target)

        if norm > 1e-9:
            u_target = u_target / norm

        # combined
        u = base_gain * eta * u_base + gain * u_target

        # clamp
        nrm = np.linalg.norm(u)
        if nrm > max_step:
            u = u / nrm * max_step

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[i] = s_new
        active[i] = True

    return controlled, active, mask


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    source = 0
    target = 1

    controlled, active, mask = pattern_field_control(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        data["aligned"][:, 1],
        data["aligned"][:, 0],
        s=2,
        alpha=0.2,
        label="baseline"
    )

    plt.scatter(
        controlled[:, 1],
        controlled[:, 0],
        s=3,
        alpha=0.6,
        label="v56 controlled"
    )

    plt.scatter(
        controlled[active, 1],
        controlled[active, 0],
        s=10,
        alpha=0.9,
        label="pattern active"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v56 — Pattern Field Control")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v56_pattern_field_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v56_pattern_field_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH v56 — Pattern Field Control\n")
        f.write("=================================\n\n")
        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n\n")
        f.write(f"Pattern active states: {np.sum(active)}\n")

    print("NEXAH v56 complete")
    print(f"Active states: {np.sum(active)}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
