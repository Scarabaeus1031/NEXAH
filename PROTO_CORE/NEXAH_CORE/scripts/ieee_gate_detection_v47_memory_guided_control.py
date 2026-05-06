# ============================================================
# NEXAH — IEEE GATE DETECTION v47
# Memory-Guided Basin Control
# ============================================================
#
# PURPOSE:
# --------
# Move from prediction to control.
#
# Builds on:
# - v41: ridge-aligned motion
# - v44: basin identities
# - v46.2: memory-based basin prediction
#
# CORE IDEA:
# ----------
# If the system has transition memory:
#
#     P(next | previous basin, current basin)
#
# then control should not only follow local geometry,
# but bias motion toward the most likely or desired next basin.
#
# v47 introduces:
#
#     memory-guided target basin attraction
#
# CONTROL OBJECTIVE:
# ------------------
# Given:
#     previous basin B_prev
#     current basin B_curr
#
# Predict:
#     target basin B_target
#
# Then steer the trajectory toward the centroid of B_target
# while preserving ridge-aligned control.
#
# OUTPUTS:
# --------
# v47_memory_guided_control.png
# v47_memory_guided_states.npy
# v47_target_basins.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import (
    run_v38_control,
    gradient_field,
    make_interpolator
)

from ieee_gate_detection_v39_attractor_memory import (
    stability_score,
    detect_stable_attractors,
    attractor_memory_field
)

from ieee_gate_detection_v41_ridge_aligned_control import (
    ridge_aligned_control,
    wrap_theta
)

from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score

from ieee_gate_detection_v44_basin_identity import cluster_locked_basins

from ieee_gate_detection_v46_basin_prediction import extract_basin_segments

from ieee_gate_detection_v46_2_memory_basin_prediction import (
    compute_memory_transition_tensor,
    compute_first_order_probs,
    predict_next_with_memory
)


# ------------------------------------------------------------
# Basin centroids
# ------------------------------------------------------------

def compute_basin_centroids(states, basin_ids):
    """
    Compute centroid for each detected basin.

    Returns:
    --------
    centroids : dict
        basin_id -> np.array([mean_r, mean_theta])
    """

    centroids = {}

    valid_ids = sorted([int(b) for b in np.unique(basin_ids) if b >= 0])

    for bid in valid_ids:
        idx = basin_ids == bid

        if np.sum(idx) == 0:
            continue

        mean_r = np.mean(states[idx, 0])

        # circular mean for theta
        theta = states[idx, 1]
        mean_theta = np.arctan2(
            np.mean(np.sin(theta)),
            np.mean(np.cos(theta))
        )

        centroids[bid] = np.array([mean_r, mean_theta])

    return centroids


# ------------------------------------------------------------
# Basin target attraction
# ------------------------------------------------------------

def target_attraction(s, target, gain=1.0):
    """
    Compute vector from current state to target basin centroid.

    Handles theta as circular coordinate.
    """

    dr = target[0] - s[0]

    dtheta = target[1] - s[1]
    dtheta = wrap_theta(dtheta)

    u = np.array([dr, dtheta])

    norm = np.linalg.norm(u)
    if norm > 1e-9:
        u = u / norm

    return gain * u


# ------------------------------------------------------------
# Memory-guided control
# ------------------------------------------------------------

def memory_guided_control(
    aligned_states,
    raw_controls,
    basin_ids,
    segments,
    memory_probs,
    fallback_probs,
    basin_list,
    centroids,
    eta=0.02,
    target_gain=0.035,
    base_gain=0.65,
    max_step=0.045,
):
    """
    Apply memory-guided control.

    For each basin segment:
    - use previous basin + current basin
    - predict target next basin
    - attract the states inside current segment toward target centroid
    - retain ridge-aligned/base motion component
    """

    controlled = aligned_states.copy()
    target_basins = np.full(len(aligned_states), -1, dtype=int)

    previous_step = np.zeros(2)

    for i in range(1, len(segments) - 1):

        previous_basin = segments[i - 1]["basin"]
        current_basin = segments[i]["basin"]

        target_basin, confidence, mode = predict_next_with_memory(
            previous_basin,
            current_basin,
            memory_probs,
            fallback_probs,
            basin_list
        )

        if target_basin < 0 or target_basin not in centroids:
            continue

        target = centroids[target_basin]

        start = segments[i]["start"]
        end = segments[i]["end"]

        for t in range(start, end + 1):

            s = controlled[t]

            u_base = raw_controls[t]
            u_target = target_attraction(
                s,
                target,
                gain=target_gain * confidence
            )

            u = base_gain * eta * u_base + u_target

            step_norm = np.linalg.norm(u)
            if step_norm > max_step:
                u = u / step_norm * max_step

            # mild smoothing
            u = 0.85 * u + 0.15 * previous_step

            s_new = s + u
            s_new[1] = wrap_theta(s_new[1])

            controlled[t] = s_new
            target_basins[t] = target_basin
            previous_step = u

    return controlled, target_basins


# ------------------------------------------------------------
# Build full pipeline
# ------------------------------------------------------------

def build_pipeline():
    """
    Build v38 → v46.2 pipeline and return all needed objects.
    """

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    # --- v38
    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    raw_controls = result["controls"]

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    # --- v39
    S = stability_score(rho, P, D)

    attractors = detect_stable_attractors(
        S,
        r_grid,
        theta_grid,
        percentile=98
    )

    A = attractor_memory_field(
        attractors,
        r_grid,
        theta_grid
    )

    # --- v41
    grad_rho = gradient_field(rho, r_grid, theta_grid)

    grad_rho_interp = (
        make_interpolator(grad_rho[0], r_grid, theta_grid),
        make_interpolator(grad_rho[1], r_grid, theta_grid),
    )

    aligned = ridge_aligned_control(
        states,
        raw_controls,
        grad_rho_interp,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    # --- v42
    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --- v44
    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    # --- segments
    segments = extract_basin_segments(basin_ids)

    basin_list = sorted([int(b) for b in np.unique(basin_ids) if b >= 0])

    # --- v46.2 memory
    memory_counts, memory_probs = compute_memory_transition_tensor(
        segments,
        basin_list
    )

    fallback_counts, fallback_probs = compute_first_order_probs(
        segments,
        basin_list
    )

    centroids = compute_basin_centroids(aligned, basin_ids)

    return {
        "t": t,
        "states": states,
        "aligned": aligned,
        "raw_controls": raw_controls,
        "basin_ids": basin_ids,
        "segments": segments,
        "basin_list": basin_list,
        "memory_probs": memory_probs,
        "fallback_probs": fallback_probs,
        "centroids": centroids,
        "L": L,
    }


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    controlled, target_basins = memory_guided_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        basin_ids=data["basin_ids"],
        segments=data["segments"],
        memory_probs=data["memory_probs"],
        fallback_probs=data["fallback_probs"],
        basin_list=data["basin_list"],
        centroids=data["centroids"],
        eta=0.02,
        target_gain=0.035,
        base_gain=0.65,
        max_step=0.045,
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        data["aligned"][:, 1],
        data["aligned"][:, 0],
        s=2,
        alpha=0.25,
        label="v41 ridge-aligned"
    )

    plt.scatter(
        controlled[:, 1],
        controlled[:, 0],
        s=3,
        alpha=0.55,
        label="v47 memory-guided"
    )

    # basin centroids
    for bid, c in data["centroids"].items():
        plt.scatter(
            c[1],
            c[0],
            s=80,
            marker="x",
            label=f"basin {bid} centroid"
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v47 — Memory-Guided Basin Control")
    plt.legend(fontsize=8)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v47_memory_guided_control.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(OUT_DIR, "v47_memory_guided_states.npy"),
        controlled
    )

    np.save(
        os.path.join(OUT_DIR, "v47_target_basins.npy"),
        target_basins
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    used_targets = target_basins[target_basins >= 0]

    summary_path = os.path.join(
        OUT_DIR,
        "v47_memory_guided_control_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v47 — Memory-Guided Basin Control Summary\n")
        f.write("==============================================\n\n")
        f.write(f"Basins: {data['basin_list']}\n")
        f.write(f"Segments: {len(data['segments'])}\n")
        f.write(f"Controlled states: {len(used_targets)}\n\n")

        if len(used_targets) > 0:
            unique, counts = np.unique(used_targets, return_counts=True)
            f.write("Target basin counts:\n")
            for u, c in zip(unique, counts):
                f.write(f"  basin {int(u)}: {int(c)}\n")

        f.write("\nBasin centroids:\n")
        for bid, c in data["centroids"].items():
            f.write(
                f"  basin {bid}: r={c[0]:.4f}, theta={c[1]:.4f}\n"
            )

    print("NEXAH v47 complete")
    print(f"Basins: {data['basin_list']}")
    print(f"Segments: {len(data['segments'])}")
    print(f"Controlled states: {len(used_targets)}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
