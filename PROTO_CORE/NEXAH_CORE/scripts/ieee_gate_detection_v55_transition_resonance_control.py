# ============================================================
# NEXAH v55 — Transition Resonance Control
# Count-Level / Path-Distribution Steering
# ============================================================
#
# PURPOSE:
# --------
# Move beyond direct state-pushing.
#
# v49/v53:
#     force a transition by pulling toward a target basin.
#
# v54:
#     respect adjacency / natural neighbor structure.
#
# v55:
#     steer transition COUNTS by mixing target attraction with
#     the system's natural transition distribution.
#
# CORE IDEA:
# ----------
# Instead of only asking:
#
#     "Can we force B_source -> B_target?"
#
# v55 asks:
#
#     "Can we reshape the transition distribution of B_source?"
#
# Example:
#     baseline from B0:
#         0 -> 1 : 5 counts
#         0 -> 3 : 3 counts
#
# Goal:
#     increase target edge while preserving graph structure.
#
# OUTPUTS:
# --------
# v55_transition_resonance_B{source}_to_B{target}.png
# v55_transition_resonance_summary_B{source}_to_B{target}.txt
# v55_transition_resonance_states_B{source}_to_B{target}.npy
#
# ============================================================

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v49_transition_probability_control import (
    build_pipeline,
    assign_nearest_basin,
    extract_segments_from_ids,
    transition_probability
)

from ieee_gate_detection_v45_transition_matrix import (
    compute_transition_matrix_from_segments
)

from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta


# ------------------------------------------------------------
# Vector helpers
# ------------------------------------------------------------

def normalized(v):
    n = np.linalg.norm(v)
    if n < 1e-9:
        return np.zeros_like(v)
    return v / n


def direction_to_centroid(s, centroid):
    dr = centroid[0] - s[0]
    dtheta = wrap_theta(centroid[1] - s[1])
    return normalized(np.array([dr, dtheta]))


# ------------------------------------------------------------
# Natural transition weights
# ------------------------------------------------------------

def outgoing_distribution(probs, basin_list, source):
    """
    Return outgoing natural transition distribution for source basin.
    """

    if source not in basin_list:
        return {}

    i = basin_list.index(source)

    dist = {}
    for j, b in enumerate(basin_list):
        if probs[i, j] > 0:
            dist[b] = probs[i, j]

    return dist


# ------------------------------------------------------------
# Resonance control
# ------------------------------------------------------------

def transition_resonance_control(
    aligned_states,
    raw_controls,
    basin_ids,
    segments,
    centroids,
    transition_probs,
    basin_list,
    source_basin,
    target_basin,
    eta=0.02,
    resonance_gain=0.065,
    base_gain=0.55,
    natural_mix=0.35,
    target_mix=0.65,
    max_step=0.055,
    smoothing=0.15
):
    """
    Count-level transition steering.

    For source basin states:
    - construct natural outgoing direction from baseline transition distribution
    - construct target direction toward desired basin
    - mix them:
          u_resonance =
              target_mix  * target_direction
            + natural_mix * natural_distribution_direction

    This avoids purely forcing one edge and keeps control aligned
    with the observed transition graph.
    """

    controlled = aligned_states.copy()
    active_mask = np.zeros(len(aligned_states), dtype=bool)

    prev = np.zeros(2)

    outgoing = outgoing_distribution(
        transition_probs,
        basin_list,
        source_basin
    )

    if target_basin not in centroids:
        raise ValueError(f"Target basin {target_basin} has no centroid.")

    target_centroid = centroids[target_basin]

    for seg in segments:

        # segment can be tuple (b,start,end) or dict
        if isinstance(seg, dict):
            b = int(seg["basin"])
            start = int(seg["start"])
            end = int(seg["end"])
        else:
            b, start, end = int(seg[0]), int(seg[1]), int(seg[2])

        if b != source_basin:
            continue

        for t in range(start, end + 1):

            s = controlled[t]

            # target direction
            u_target = direction_to_centroid(s, target_centroid)

            # natural outgoing direction
            u_nat = np.zeros(2)

            for nb, w in outgoing.items():
                if nb not in centroids:
                    continue
                u_nat += w * direction_to_centroid(s, centroids[nb])

            u_nat = normalized(u_nat)

            # mixed resonance direction
            u_res = normalized(
                target_mix * u_target +
                natural_mix * u_nat
            )

            u_base = raw_controls[t]

            u = base_gain * eta * u_base + resonance_gain * u_res

            # step clamp
            nrm = np.linalg.norm(u)
            if nrm > max_step:
                u = u / nrm * max_step

            # smoothing
            u = (1.0 - smoothing) * u + smoothing * prev

            s_new = s + u
            s_new[1] = wrap_theta(s_new[1])

            controlled[t] = s_new
            active_mask[t] = True
            prev = u

    return controlled, active_mask, outgoing


# ------------------------------------------------------------
# Matrix formatting
# ------------------------------------------------------------

def safe_policy_name(source, target):
    return f"B{source}_to_B{target}"


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="NEXAH v55 Transition Resonance Control"
    )

    parser.add_argument("--source", type=int, default=0)
    parser.add_argument("--target", type=int, default=1)

    parser.add_argument(
        "--resonance-gain",
        type=float,
        default=0.065
    )

    parser.add_argument(
        "--target-mix",
        type=float,
        default=0.65,
        help="Weight of target edge direction."
    )

    parser.add_argument(
        "--natural-mix",
        type=float,
        default=0.35,
        help="Weight of natural outgoing distribution."
    )

    parser.add_argument(
        "--base-gain",
        type=float,
        default=0.55
    )

    args = parser.parse_args()

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    source = args.source
    target = args.target

    controlled, active_mask, outgoing = transition_resonance_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        basin_ids=data["basin_ids"],
        segments=data["segments"],
        centroids=data["centroids"],
        transition_probs=data["transition_probs"],
        basin_list=data["basin_list"],
        source_basin=source,
        target_basin=target,
        eta=0.02,
        resonance_gain=args.resonance_gain,
        base_gain=args.base_gain,
        natural_mix=args.natural_mix,
        target_mix=args.target_mix,
        max_step=0.055,
        smoothing=0.15
    )

    # --------------------------------------------------------
    # Reclassify and evaluate
    # --------------------------------------------------------

    controlled_ids = assign_nearest_basin(
        controlled,
        data["centroids"]
    )

    controlled_counts, controlled_probs, controlled_basin_list, _ = (
        compute_transition_matrix_from_segments(controlled_ids)
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
        alpha=0.55,
        label="v55 resonance-controlled"
    )

    plt.scatter(
        controlled[active_mask, 1],
        controlled[active_mask, 0],
        s=9,
        alpha=0.85,
        label="active resonance control"
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
        f"NEXAH v55 — Transition Resonance B{source}→B{target}\n"
        f"P before={p_before:.3f}, after={p_after:.3f}, Δ={delta_p:.3f}"
    )

    plt.legend(fontsize=7)
    plt.tight_layout()

    tag = safe_policy_name(source, target)

    png_path = os.path.join(
        OUT_DIR,
        f"v55_transition_resonance_{tag}.png"
    )

    plt.savefig(png_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Save outputs
    # --------------------------------------------------------

    np.save(
        os.path.join(
            OUT_DIR,
            f"v55_transition_resonance_states_{tag}.npy"
        ),
        controlled
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v55_transition_resonance_basin_ids_{tag}.npy"
        ),
        controlled_ids
    )

    np.save(
        os.path.join(
            OUT_DIR,
            f"v55_transition_resonance_probs_{tag}.npy"
        ),
        controlled_probs
    )

    txt_path = os.path.join(
        OUT_DIR,
        f"v55_transition_resonance_summary_{tag}.txt"
    )

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v55 — Transition Resonance Control Summary\n")
        f.write("===============================================\n\n")

        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n\n")

        f.write(f"Resonance gain: {args.resonance_gain}\n")
        f.write(f"Base gain: {args.base_gain}\n")
        f.write(f"Target mix: {args.target_mix}\n")
        f.write(f"Natural mix: {args.natural_mix}\n\n")

        f.write(f"Active controlled states: {int(np.sum(active_mask))}\n\n")

        f.write("Natural outgoing distribution from source:\n")
        for k, v in outgoing.items():
            f.write(f"  {source}->{k}: {v:.4f}\n")

        f.write("\n")
        f.write(f"P_before({source}->{target}): {p_before:.4f}\n")
        f.write(f"P_after({source}->{target}):  {p_after:.4f}\n")
        f.write(f"Delta P: {delta_p:.4f}\n\n")

        f.write("Baseline transition probs:\n")
        f.write(str(data["transition_probs"]))
        f.write("\n\nControlled transition probs:\n")
        f.write(str(controlled_probs))
        f.write("\n\nControlled transition counts:\n")
        f.write(str(controlled_counts))
        f.write("\n")

    print("NEXAH v55 complete")
    print(f"Transition resonance: {source} -> {target}")
    print(f"Natural outgoing distribution: {outgoing}")
    print(f"Active controlled states: {int(np.sum(active_mask))}")
    print(f"P before: {p_before:.4f}")
    print(f"P after:  {p_after:.4f}")
    print(f"Delta P:  {delta_p:.4f}")
    print(f"Saved: {png_path}")
    print(f"Saved: {txt_path}")
