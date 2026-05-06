# ============================================================
# NEXAH — IEEE GATE DETECTION v52
# Pattern-Based Transition Control
# ============================================================
#
# PURPOSE:
# --------
# Test pulsed / patterned control instead of continuous control.
#
# v49:
#     control one transition continuously inside source basin
#
# v50/v51:
#     policy / adaptive edge control
#
# v52:
#     apply control only according to a temporal pattern:
#
#         1 = control ON
#         0 = control OFF / natural flow
#
# Example:
#
#     pattern = 110111
#
# means:
#
#     ON, ON, OFF, ON, ON, ON
#
# CORE IDEA:
# ----------
# Continuous control may oversteer or distort the basin graph.
# Patterned control tests whether pulsed intervention improves
# transition probability while preserving natural structure.
#
# DEFAULT:
# --------
# source = 0
# target = 1
# pattern = 110111
#
# OUTPUTS:
# --------
# v52_pattern_control_B{source}_to_B{target}_{pattern}.png
# v52_pattern_control_summary_B{source}_to_B{target}_{pattern}.txt
# v52_pattern_control_states_B{source}_to_B{target}_{pattern}.npy
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
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments
from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids


# ------------------------------------------------------------
# Pattern parsing
# ------------------------------------------------------------

def parse_pattern(pattern_string):
    """
    Parse string pattern like:
        "110111"

    into:
        np.array([1,1,0,1,1,1])
    """

    cleaned = pattern_string.replace(",", "").replace(" ", "")

    if len(cleaned) == 0:
        raise ValueError("Pattern must not be empty.")

    values = []

    for ch in cleaned:
        if ch not in ["0", "1"]:
            raise ValueError(
                f"Invalid pattern character '{ch}'. Use only 0 and 1."
            )

        values.append(int(ch))

    return np.array(values, dtype=int)


def pattern_is_on(pattern, local_index):
    """
    Return whether control is active at this local segment step.
    """

    return pattern[local_index % len(pattern)] == 1


# ------------------------------------------------------------
# Target attraction
# ------------------------------------------------------------

def target_attraction(s, target, gain=1.0):
    """
    Vector from state s to target basin centroid.
    theta is circular.
    """

    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])

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
    """

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

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

    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    counts, probs, basin_list, segments = compute_transition_matrix_from_segments(
        basin_ids
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
        "transition_counts": counts,
        "transition_probs": probs,
        "centroids": centroids,
    }


# ------------------------------------------------------------
# Segment helper
# ------------------------------------------------------------

def unpack_segment(seg):
    """
    Accept both segment formats:
    - dict: {"basin": b, "start": i, "end": j}
    - tuple/list: (b, i, j)
    """

    if isinstance(seg, dict):
        return int(seg["basin"]), int(seg["start"]), int(seg["end"])

    if isinstance(seg, (tuple, list)) and len(seg) == 3:
        return int(seg[0]), int(seg[1]), int(seg[2])

    raise ValueError(f"Unknown segment format: {seg}")


# ------------------------------------------------------------
# Pattern control
# ------------------------------------------------------------

def pattern_transition_control(
    aligned_states,
    raw_controls,
    segments,
    source_basin,
    target_basin,
    target_centroid,
    pattern,
    eta=0.02,
    control_gain=0.065,
    base_gain=0.55,
    max_step=0.055,
    smoothing=0.15
):
    """
    Apply transition-specific control only according to pattern.

    Control is only considered inside source_basin segments.

    If pattern step == 1:
        apply target attraction

    If pattern step == 0:
        preserve only weak base motion
    """

    controlled = aligned_states.copy()
    active_mask = np.zeros(len(aligned_states), dtype=bool)
    off_mask = np.zeros(len(aligned_states), dtype=bool)

    previous_step = np.zeros(2)

    for seg in segments:

        basin, start, end = unpack_segment(seg)

        if basin != source_basin:
            continue

        local_index = 0

        for t in range(start, end + 1):

            s = controlled[t]
            u_base = raw_controls[t]

            if pattern_is_on(pattern, local_index):
                u_target = target_attraction(
                    s,
                    target_centroid,
                    gain=control_gain
                )

                u = base_gain * eta * u_base + u_target
                active_mask[t] = True

            else:
                # natural relaxation / weak base flow
                u = base_gain * eta * u_base
                off_mask[t] = True

            step_norm = np.linalg.norm(u)
            if step_norm > max_step:
                u = u / step_norm * max_step

            u = (1.0 - smoothing) * u + smoothing * previous_step

            s_new = s + u
            s_new[1] = wrap_theta(s_new[1])

            controlled[t] = s_new
            previous_step = u
            local_index += 1

    return controlled, active_mask, off_mask


# ------------------------------------------------------------
# Controlled basin assignment
# ------------------------------------------------------------

def assign_nearest_basin(states, centroids):
    """
    Assign every state to nearest basin centroid.
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


def transition_probability(probs, basin_list, source, target):
    """
    Return P(source -> target).
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
        description="NEXAH v52 Pattern-Based Transition Control"
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
        "--pattern",
        type=str,
        default="110111",
        help="Binary control pattern. Example: 110111"
    )

    parser.add_argument(
        "--control-gain",
        type=float,
        default=0.065,
        help="Target attraction gain. Default: 0.065"
    )

    parser.add_argument(
        "--base-gain",
        type=float,
        default=0.55,
        help="Base flow gain. Default: 0.55"
    )

    args = parser.parse_args()

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    pattern = parse_pattern(args.pattern)

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

    controlled, active_mask, off_mask = pattern_transition_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        segments=data["segments"],
        source_basin=source,
        target_basin=target,
        target_centroid=target_centroid,
        pattern=pattern,
        eta=0.02,
        control_gain=args.control_gain,
        base_gain=args.base_gain,
        max_step=0.055,
        smoothing=0.15
    )

    controlled_basin_ids = assign_nearest_basin(
        controlled,
        data["centroids"]
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
        alpha=0.18,
        label="baseline v41"
    )

    plt.scatter(
        controlled[:, 1],
        controlled[:, 0],
        s=3,
        alpha=0.50,
        label="v52 pattern-controlled"
    )

    plt.scatter(
        controlled[active_mask, 1],
        controlled[active_mask, 0],
        s=9,
        alpha=0.85,
        label="pattern ON"
    )

    plt.scatter(
        controlled[off_mask, 1],
        controlled[off_mask, 0],
        s=9,
        alpha=0.55,
        label="pattern OFF / relax"
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
        f"NEXAH v52 — Pattern Control B{source}→B{target}\n"
        f"pattern={args.pattern} | P before={p_before:.3f}, "
        f"after={p_after:.3f}, Δ={delta_p:.3f}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    safe_name = f"B{source}_to_B{target}_{args.pattern}"

    out_path = os.path.join(
        OUT_DIR,
        f"v52_pattern_control_{safe_name}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(
            OUT_DIR,
            f"v52_pattern_control_states_{safe_name}.npy"
        ),
        controlled
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v52_pattern_control_basin_ids_{safe_name}.npy"
        ),
        controlled_basin_ids
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v52_pattern_control_transition_probs_{safe_name}.npy"
        ),
        controlled_probs
    )

    summary_path = os.path.join(
        OUT_DIR,
        f"v52_pattern_control_summary_{safe_name}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v52 — Pattern-Based Transition Control Summary\n")
        f.write("===================================================\n\n")
        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n")
        f.write(f"Pattern: {args.pattern}\n")
        f.write(f"Pattern array: {pattern.tolist()}\n\n")

        f.write(f"Control gain: {args.control_gain}\n")
        f.write(f"Base gain: {args.base_gain}\n\n")

        f.write(f"Pattern ON states: {int(np.sum(active_mask))}\n")
        f.write(f"Pattern OFF states: {int(np.sum(off_mask))}\n\n")

        f.write(f"P_before({source}->{target}): {p_before:.4f}\n")
        f.write(f"P_after({source}->{target}):  {p_after:.4f}\n")
        f.write(f"Delta P: {delta_p:.4f}\n\n")

        f.write("Baseline transition probs:\n")
        f.write(str(data["transition_probs"]))
        f.write("\n\nControlled transition probs:\n")
        f.write(str(controlled_probs))
        f.write("\n")

    print("NEXAH v52 complete")
    print(f"Transition controlled: {source} -> {target}")
    print(f"Pattern: {args.pattern}")
    print(f"Pattern ON states: {int(np.sum(active_mask))}")
    print(f"Pattern OFF states: {int(np.sum(off_mask))}")
    print(f"P before: {p_before:.4f}")
    print(f"P after:  {p_after:.4f}")
    print(f"Delta P:  {delta_p:.4f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
