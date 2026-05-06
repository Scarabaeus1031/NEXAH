# ============================================================
# NEXAH — IEEE GATE DETECTION v50
# Multi-Transition Policy Control
# ============================================================
#
# PURPOSE:
# --------
# Move from controlling a single transition to controlling
# a transition policy over the basin graph.
#
# v49:
#     control one edge:
#         B_source → B_target
#
# v50:
#     control multiple desired transitions:
#         B_i → B_j
#         B_k → B_l
#         ...
#
# CORE IDEA:
# ----------
# The system is now treated as a directed basin graph.
# Control acts on selected graph edges by applying local steering
# only when the trajectory is inside the source basin of a policy rule.
#
# DEFAULT POLICY:
# ---------------
# Strengthen the dominant natural loop:
#
#     2 → 0
#     0 → 1
#     1 → 2
#
# This tests whether NEXAH can reinforce a stable cyclic pathway.
#
# OUTPUTS:
# --------
# v50_policy_transition_control.png
# v50_policy_transition_summary.txt
# v50_policy_controlled_states.npy
# v50_policy_controlled_transition_probs.npy
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
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


# ------------------------------------------------------------
# Target attraction
# ------------------------------------------------------------

def target_attraction(s, target, gain=1.0):
    """
    Vector from state s to target basin centroid.
    theta is circular.
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
# Policy parser
# ------------------------------------------------------------

def parse_policy(policy_string):
    """
    Parse policy string like:

        "2:0,0:1,1:2"

    into list of tuples:

        [(2,0), (0,1), (1,2)]
    """

    rules = []

    for part in policy_string.split(","):
        part = part.strip()
        if not part:
            continue

        if ":" not in part:
            raise ValueError(
                f"Invalid policy rule '{part}'. Use format source:target."
            )

        source, target = part.split(":")
        rules.append((int(source), int(target)))

    return rules


# ------------------------------------------------------------
# Policy control
# ------------------------------------------------------------

def policy_transition_control(
    aligned_states,
    raw_controls,
    segments,
    policy_rules,
    centroids,
    eta=0.02,
    policy_gain=0.065,
    base_gain=0.55,
    max_step=0.055,
    smoothing=0.15
):
    """
    Apply multi-transition policy control.

    For each segment:
    - if its basin appears as a source in the policy,
      steer toward that rule's target basin.
    - otherwise leave it unchanged except for baseline continuity.
    """

    controlled = aligned_states.copy()
    active_mask = np.zeros(len(aligned_states), dtype=bool)
    target_by_state = np.full(len(aligned_states), -1, dtype=int)

    previous_step = np.zeros(2)

    policy_map = {source: target for source, target in policy_rules}

    for seg in segments:

        basin, start, end = unpack_segment(seg)

        if basin not in policy_map:
            continue

        target_basin = policy_map[basin]

        if target_basin not in centroids:
            continue

        target_centroid = centroids[target_basin]

        for t in range(start, end + 1):

            s = controlled[t]

            u_base = raw_controls[t]

            u_target = target_attraction(
                s,
                target_centroid,
                gain=policy_gain
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
            target_by_state[t] = target_basin
            previous_step = u

    return controlled, active_mask, target_by_state


# ------------------------------------------------------------
# Controlled basin reassignment
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


# ------------------------------------------------------------
# Probability lookup
# ------------------------------------------------------------

def transition_probability(probs, basin_list, source, target):
    """
    Return P(source -> target).
    """

    if source not in basin_list or target not in basin_list:
        return 0.0

    i = basin_list.index(source)
    j = basin_list.index(target)

    return float(probs[i, j])


def policy_score(probs, basin_list, policy_rules):
    """
    Mean probability of all requested policy edges.
    """

    vals = []

    for source, target in policy_rules:
        vals.append(transition_probability(probs, basin_list, source, target))

    if not vals:
        return 0.0

    return float(np.mean(vals))


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH v50 Multi-Transition Policy Control"
    )

    parser.add_argument(
        "--policy",
        type=str,
        default="2:0,0:1,1:2",
        help="Policy rules as source:target comma list. Default: 2:0,0:1,1:2"
    )

    parser.add_argument(
        "--policy-gain",
        type=float,
        default=0.065,
        help="Policy transition attraction gain. Default: 0.065"
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

    policy_rules = parse_policy(args.policy)

    data = build_pipeline()

    controlled, active_mask, target_by_state = policy_transition_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        segments=data["segments"],
        policy_rules=policy_rules,
        centroids=data["centroids"],
        eta=0.02,
        policy_gain=args.policy_gain,
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

    score_before = policy_score(
        data["transition_probs"],
        data["basin_list"],
        policy_rules
    )

    score_after = policy_score(
        controlled_probs,
        controlled_basin_list,
        policy_rules
    )

    delta_score = score_after - score_before

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
        alpha=0.55,
        label="v50 policy-controlled"
    )

    plt.scatter(
        controlled[active_mask, 1],
        controlled[active_mask, 0],
        s=8,
        alpha=0.85,
        label="active policy control"
    )

    for bid, c in data["centroids"].items():
        plt.scatter(
            c[1],
            c[0],
            s=90,
            marker="x",
            label=f"basin {bid}"
        )

    policy_label = ", ".join([f"{s}->{t}" for s, t in policy_rules])

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title(
        "NEXAH v50 — Multi-Transition Policy Control\n"
        f"Policy: {policy_label} | score before={score_before:.3f}, "
        f"after={score_after:.3f}, Δ={delta_score:.3f}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    safe_policy_name = args.policy.replace(":", "to").replace(",", "_")

    out_path = os.path.join(
        OUT_DIR,
        f"v50_policy_transition_control_{safe_policy_name}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(
            OUT_DIR,
            f"v50_policy_controlled_states_{safe_policy_name}.npy"
        ),
        controlled
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v50_policy_controlled_basin_ids_{safe_policy_name}.npy"
        ),
        controlled_basin_ids
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v50_policy_controlled_transition_probs_{safe_policy_name}.npy"
        ),
        controlled_probs
    )

    summary_path = os.path.join(
        OUT_DIR,
        f"v50_policy_transition_summary_{safe_policy_name}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v50 — Multi-Transition Policy Control Summary\n")
        f.write("==================================================\n\n")
        f.write(f"Policy rules: {policy_rules}\n")
        f.write(f"Policy gain: {args.policy_gain}\n")
        f.write(f"Base gain: {args.base_gain}\n\n")
        f.write(f"Active controlled states: {int(np.sum(active_mask))}\n\n")

        f.write(f"Policy score before: {score_before:.4f}\n")
        f.write(f"Policy score after:  {score_after:.4f}\n")
        f.write(f"Delta score:         {delta_score:.4f}\n\n")

        f.write("Policy edge probabilities:\n")
        for source, target in policy_rules:
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
            f.write(
                f"  {source}->{target}: "
                f"before={p_before:.4f}, "
                f"after={p_after:.4f}, "
                f"delta={p_after - p_before:.4f}\n"
            )

        f.write("\nBaseline transition probs:\n")
        f.write(str(data["transition_probs"]))
        f.write("\n\nControlled transition probs:\n")
        f.write(str(controlled_probs))
        f.write("\n")

    print("NEXAH v50 complete")
    print(f"Policy: {policy_rules}")
    print(f"Active controlled states: {int(np.sum(active_mask))}")
    print(f"Policy score before: {score_before:.4f}")
    print(f"Policy score after:  {score_after:.4f}")
    print(f"Delta score:         {delta_score:.4f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
