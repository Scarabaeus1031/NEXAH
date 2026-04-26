# ============================================================
# NEXAH — IEEE GATE DETECTION v49
# Transition Probability Control / Closed-Loop Basin Steering
# ============================================================
#
# PURPOSE:
# --------
# Move from target-position control to transition-probability control.
#
# v48:
#     steer toward a target basin centroid
#
# v49:
#     alter the probability of a specific basin transition:
#
#         B_source → B_target
#
# CORE IDEA:
# ----------
# In a cyclic basin system, the correct control object is not
# only "where is the trajectory now?", but:
#
#     which transition should become more likely?
#
# CONTROL OBJECTIVE:
# ------------------
# If the system is in source basin B_source,
# apply a control bias toward B_target.
#
# Otherwise, preserve ridge-aligned motion.
#
# OUTPUTS:
# --------
# v49_transition_control_B{source}_to_B{target}.png
# v49_transition_control_summary_B{source}_to_B{target}.txt
# v49_transition_control_states_B{source}_to_B{target}.npy
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

from ieee_gate_detection_v46_basin_prediction import extract_basin_segments

from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids

from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


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
# Build base pipeline
# ------------------------------------------------------------

def build_pipeline():
    """
    Build v38 → v45 baseline pipeline.

    Returns all objects needed for transition-probability control.
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

    # --- v45 baseline transition matrix
    counts, probs, basin_list, segments = compute_transition_matrix_from_segments(
        basin_ids
    )

    centroids = compute_basin_centroids(aligned, basin_ids)

    return {
        "t": t,
        "states": states,
        "aligned": aligned,
        "raw_controls": raw_controls,
        "rho": rho,
        "P": P,
        "D": D,
        "A": A,
        "r_grid": r_grid,
        "theta_grid": theta_grid,
        "L": L,
        "basin_ids": basin_ids,
        "segments": segments,
        "basin_list": basin_list,
        "transition_counts": counts,
        "transition_probs": probs,
        "centroids": centroids,
    }


# ------------------------------------------------------------
# Transition-control steering
# ------------------------------------------------------------

def transition_probability_control(
    aligned_states,
    raw_controls,
    basin_ids,
    segments,
    source_basin,
    target_basin,
    target_centroid,
    eta=0.02,
    transition_gain=0.065,
    base_gain=0.55,
    max_step=0.055,
    smoothing=0.15
):
    """
    Apply transition-specific control.

    Control is active only when the trajectory is inside source_basin.
    During source basin segments, states are biased toward target_basin.
    Elsewhere, only weak base motion is preserved.
    """

    controlled = aligned_states.copy()
    active_mask = np.zeros(len(aligned_states), dtype=bool)
    previous_step = np.zeros(2)

    for seg in segments:

        b = seg["basin"]
        start = seg["start"]
        end = seg["end"]

        if b != source_basin:
            continue

        for t in range(start, end + 1):

            s = controlled[t]

            u_base = raw_controls[t]
            u_target = target_attraction(
                s,
                target_centroid,
                gain=transition_gain
            )

            u = base_gain * eta * u_base + u_target

            step_norm = np.linalg.norm(u)
            if step_norm > max_step:
                u = u / step_norm * max_step

            u = (1.0 - smoothing) * u + smoothing * previous_step

            s_new = s + u
            s_new[1] = wrap_theta(s_new[1])

            controlled[t] = s_new
            active_mask[t] = True
            previous_step = u

    return controlled, active_mask


# ------------------------------------------------------------
# Reclassify controlled states by nearest original basin centroid
# ------------------------------------------------------------

def assign_nearest_basin(states, centroids):
    """
    Assign every state to nearest basin centroid.

    This creates an approximate controlled basin sequence
    for measuring transition changes.
    """

    basin_ids = np.full(len(states), -1, dtype=int)

    basin_list = sorted(centroids.keys())

    for i, s in enumerate(states):

        best_basin = -1
        best_dist = np.inf

        for bid in basin_list:
            c = centroids[bid]

            dr = s[0] - c[0]
            dtheta = wrap_theta(s[1] - c[1])

            dist = np.sqrt(dr**2 + dtheta**2)

            if dist < best_dist:
                best_dist = dist
                best_basin = bid

        basin_ids[i] = best_basin

    return basin_ids


# ------------------------------------------------------------
# Segment extraction from assigned basins
# ------------------------------------------------------------

def extract_segments_from_ids(basin_ids):
    """
    Extract contiguous basin segments from basin id sequence.
    """

    segments = []
    current = None

    for t, b in enumerate(basin_ids):
        if b >= 0:
            if current is None:
                current = {
                    "basin": int(b),
                    "start": t,
                    "end": t
                }
            elif current["basin"] == int(b):
                current["end"] = t
            else:
                segments.append(current)
                current = {
                    "basin": int(b),
                    "start": t,
                    "end": t
                }

    if current is not None:
        segments.append(current)

    return segments


# ------------------------------------------------------------
# Transition probability lookup
# ------------------------------------------------------------

def transition_probability(probs, basin_list, source, target):
    """
    Return P(source -> target) from probability matrix.
    """

    if source not in basin_list or target not in basin_list:
        return 0.0

    i = basin_list.index(source)
    j = basin_list.index(target)

    return float(probs[i, j])


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH v49 Transition Probability Control"
    )

    parser.add_argument(
        "--source",
        type=int,
        default=0,
        help="Source basin id. Default: 0"
    )

    parser.add_argument(
        "--target",
        type=int,
        default=1,
        help="Target basin id. Default: 1"
    )

    parser.add_argument(
        "--transition-gain",
        type=float,
        default=0.065,
        help="Transition attraction gain. Default: 0.065"
    )

    parser.add_argument(
        "--base-gain",
        type=float,
        default=0.55,
        help="Base control gain. Default: 0.55"
    )

    args = parser.parse_args()

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    source = args.source
    target = args.target

    if source not in data["centroids"]:
        print(f"Source basin {source} not found.")
        print(f"Available basins: {sorted(data['centroids'].keys())}")
        sys.exit(1)

    if target not in data["centroids"]:
        print(f"Target basin {target} not found.")
        print(f"Available basins: {sorted(data['centroids'].keys())}")
        sys.exit(1)

    target_centroid = data["centroids"][target]

    controlled, active_mask = transition_probability_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        basin_ids=data["basin_ids"],
        segments=data["segments"],
        source_basin=source,
        target_basin=target,
        target_centroid=target_centroid,
        eta=0.02,
        transition_gain=args.transition_gain,
        base_gain=args.base_gain,
        max_step=0.055,
        smoothing=0.15
    )

    # --------------------------------------------------------
    # Estimate controlled transition probabilities
    # --------------------------------------------------------

    controlled_basin_ids = assign_nearest_basin(
        controlled,
        data["centroids"]
    )

    controlled_segments = extract_segments_from_ids(
        controlled_basin_ids
    )

    controlled_counts, controlled_probs, controlled_basin_list, _ = (
        compute_transition_matrix_from_segments(controlled_basin_ids)
    )

    p_before = transition_probability(
        data["transition_probs"],
        data["basin_list"],
        source,
        target
    )

    p_after = transition_probability(
        controlled_probs,
        controlled_basin_list,
        source,
        target
    )

    delta_p = p_after - p_before

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        data["aligned"][:, 1],
        data["aligned"][:, 0],
        s=2,
        alpha=0.2,
        label="baseline v41"
    )

    plt.scatter(
        controlled[:, 1],
        controlled[:, 0],
        s=3,
        alpha=0.55,
        label=f"v49 control {source}→{target}"
    )

    plt.scatter(
        controlled[active_mask, 1],
        controlled[active_mask, 0],
        s=8,
        alpha=0.85,
        label="active control region"
    )

    for bid, c in data["centroids"].items():
        plt.scatter(
            c[1],
            c[0],
            s=90,
            marker="x",
            label=f"basin {bid}"
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title(
        f"NEXAH v49 — Transition Control B{source}→B{target}\n"
        f"P before={p_before:.3f}, after={p_after:.3f}, Δ={delta_p:.3f}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v49_transition_control_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(
            OUT_DIR,
            f"v49_transition_control_states_B{source}_to_B{target}.npy"
        ),
        controlled
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v49_controlled_basin_ids_B{source}_to_B{target}.npy"
        ),
        controlled_basin_ids
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v49_controlled_transition_probs_B{source}_to_B{target}.npy"
        ),
        controlled_probs
    )

    summary_path = os.path.join(
        OUT_DIR,
        f"v49_transition_control_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v49 — Transition Probability Control Summary\n")
        f.write("=================================================\n\n")
        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n\n")
        f.write(f"Transition gain: {args.transition_gain}\n")
        f.write(f"Base gain: {args.base_gain}\n\n")
        f.write(f"Active controlled states: {int(np.sum(active_mask))}\n\n")
        f.write(f"P_before({source}->{target}): {p_before:.4f}\n")
        f.write(f"P_after({source}->{target}):  {p_after:.4f}\n")
        f.write(f"Delta P: {delta_p:.4f}\n\n")

        f.write("Baseline transition probs:\n")
        f.write(str(data["transition_probs"]))
        f.write("\n\nControlled transition probs:\n")
        f.write(str(controlled_probs))
        f.write("\n")

    print("NEXAH v49 complete")
    print(f"Transition controlled: {source} -> {target}")
    print(f"Active controlled states: {int(np.sum(active_mask))}")
    print(f"P before: {p_before:.4f}")
    print(f"P after:  {p_after:.4f}")
    print(f"Delta P:  {delta_p:.4f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
