# ============================================================
# NEXAH — IEEE GATE DETECTION v48
# Target Basin Control
# ============================================================
#
# PURPOSE:
# --------
# Move from memory-predicted control to explicit target control.
#
# v47:
#     steer toward memory-predicted next basin
#
# v48:
#     steer toward a USER-DEFINED target basin
#
# CORE IDEA:
# ----------
# The system should be able to bias motion toward one selected
# stable basin while preserving structure-aligned movement.
#
# CONTROL OBJECTIVE:
# ------------------
# Given target basin B_target:
#
#     u = ridge-aligned base motion
#       + attraction toward target basin centroid
#
# OUTPUTS:
# --------
# v48_target_basin_control.png
# v48_target_basin_states.npy
# v48_target_basin_summary.txt
#
# ============================================================

import os
import sys
import argparse
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

from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids


# ------------------------------------------------------------
# Target attraction
# ------------------------------------------------------------

def target_attraction(s, target, gain=1.0):
    """
    Vector from state s to target basin centroid.

    theta is treated as circular.
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
# Distance to target basin
# ------------------------------------------------------------

def target_distance(states, target):
    """
    Distance from states to target centroid with circular theta.
    """

    dr = states[:, 0] - target[0]
    dtheta = np.array([wrap_theta(x - target[1]) for x in states[:, 1]])

    return np.sqrt(dr**2 + dtheta**2)


# ------------------------------------------------------------
# Target basin control
# ------------------------------------------------------------

def target_basin_control(
    aligned_states,
    raw_controls,
    target_centroid,
    eta=0.02,
    target_gain=0.045,
    base_gain=0.55,
    max_step=0.05,
    smoothing=0.15
):
    """
    Apply explicit target basin attraction while retaining
    structure-aligned base control.
    """

    controlled = aligned_states.copy()
    previous_step = np.zeros(2)

    for t in range(len(controlled)):

        s = controlled[t]

        u_base = raw_controls[t]
        u_target = target_attraction(
            s,
            target_centroid,
            gain=target_gain
        )

        u = base_gain * eta * u_base + u_target

        # clip step
        step_norm = np.linalg.norm(u)
        if step_norm > max_step:
            u = u / step_norm * max_step

        # smooth step
        u = (1.0 - smoothing) * u + smoothing * previous_step

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[t] = s_new
        previous_step = u

    return controlled


# ------------------------------------------------------------
# Build base pipeline
# ------------------------------------------------------------

def build_pipeline():
    """
    Build v38 → v44 pipeline and return aligned states,
    basin identities, basin centroids, and raw controls.
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

    # --- v44 basin identities
    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    centroids = compute_basin_centroids(aligned, basin_ids)

    return {
        "t": t,
        "states": states,
        "aligned": aligned,
        "raw_controls": raw_controls,
        "basin_ids": basin_ids,
        "centroids": centroids,
        "L": L,
    }


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH v48 Target Basin Control"
    )

    parser.add_argument(
        "--target",
        type=int,
        default=0,
        help="Target basin id. Default: 0"
    )

    parser.add_argument(
        "--target-gain",
        type=float,
        default=0.045,
        help="Target attraction gain. Default: 0.045"
    )

    parser.add_argument(
        "--base-gain",
        type=float,
        default=0.55,
        help="Base ridge-control gain. Default: 0.55"
    )

    args = parser.parse_args()

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    target_basin = args.target

    if target_basin not in data["centroids"]:
        print(f"Target basin {target_basin} not found.")
        print(f"Available basins: {sorted(data['centroids'].keys())}")
        sys.exit(1)

    target_centroid = data["centroids"][target_basin]

    controlled = target_basin_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        target_centroid=target_centroid,
        eta=0.02,
        target_gain=args.target_gain,
        base_gain=args.base_gain,
        max_step=0.05,
        smoothing=0.15
    )

    # --- metrics
    dist_before = target_distance(data["aligned"], target_centroid)
    dist_after = target_distance(controlled, target_centroid)

    improvement = np.mean(dist_before) - np.mean(dist_after)

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
        label=f"v48 target basin {target_basin}"
    )

    # plot all centroids
    for bid, c in data["centroids"].items():
        marker_size = 120 if bid == target_basin else 70
        plt.scatter(
            c[1],
            c[0],
            s=marker_size,
            marker="x",
            label=f"basin {bid} centroid"
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title(f"NEXAH v48 — Target Basin Control B{target_basin}")
    plt.legend(fontsize=8)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v48_target_basin_{target_basin}_control.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(
            OUT_DIR,
            f"v48_target_basin_{target_basin}_states.npy"
        ),
        controlled
    )

    summary_path = os.path.join(
        OUT_DIR,
        f"v48_target_basin_{target_basin}_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v48 — Target Basin Control Summary\n")
        f.write("=======================================\n\n")
        f.write(f"Target basin: {target_basin}\n")
        f.write(
            f"Target centroid: "
            f"r={target_centroid[0]:.4f}, "
            f"theta={target_centroid[1]:.4f}\n\n"
        )
        f.write(f"Target gain: {args.target_gain}\n")
        f.write(f"Base gain: {args.base_gain}\n\n")
        f.write(f"Mean distance before: {np.mean(dist_before):.4f}\n")
        f.write(f"Mean distance after:  {np.mean(dist_after):.4f}\n")
        f.write(f"Distance improvement: {improvement:.4f}\n")
        f.write(f"Median distance before: {np.median(dist_before):.4f}\n")
        f.write(f"Median distance after:  {np.median(dist_after):.4f}\n")

    print("NEXAH v48 complete")
    print(f"Target basin: {target_basin}")
    print(f"Target centroid: r={target_centroid[0]:.4f}, theta={target_centroid[1]:.4f}")
    print(f"Mean distance before: {np.mean(dist_before):.4f}")
    print(f"Mean distance after:  {np.mean(dist_after):.4f}")
    print(f"Distance improvement: {improvement:.4f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
