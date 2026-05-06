# ============================================================
# NEXAH v54 — Adjacency-Aware Pattern Control
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

from ieee_gate_detection_v49_transition_probability_control import (
    build_pipeline,
    transition_probability,
    assign_nearest_basin,
    extract_segments_from_ids
)

from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta

# ------------------------------------------------------------
# Adjacency extraction
# ------------------------------------------------------------

def build_adjacency(probs, basin_list, threshold=0.05):
    """
    Build adjacency list from transition matrix.
    """

    adjacency = {}

    for i, b_i in enumerate(basin_list):
        adjacency[b_i] = []

        for j, b_j in enumerate(basin_list):
            if probs[i, j] > threshold:
                adjacency[b_i].append(b_j)

    return adjacency


# ------------------------------------------------------------
# Phase pattern (reuse v53 logic)
# ------------------------------------------------------------

PHASE_MAP = {
    "engage":  [0,1,0,0],
    "lock":    [0,0,1,0],
    "release": [0,0,0,1],
    "next":    [1,0,0,0],
}

PHASE_SEQUENCE = ["engage", "lock", "release", "next"]


def generate_phase_mask(n):
    pattern = []
    for p in PHASE_SEQUENCE:
        pattern.extend(PHASE_MAP[p])

    pattern = np.array(pattern)
    mask = np.tile(pattern, int(np.ceil(n / len(pattern))))[:n]

    return mask.astype(bool)


# ------------------------------------------------------------
# Adjacency-aware control
# ------------------------------------------------------------

def adjacency_pattern_control(
    aligned_states,
    raw_controls,
    basin_ids,
    locking_score,
    centroids,
    adjacency,
    source_basin,
    target_basin,
    eta=0.02,
    gain=0.065,
    base_gain=0.55,
    max_step=0.055,
    smoothing=0.15
):

    n = len(aligned_states)

    controlled = aligned_states.copy()
    active_mask = np.zeros(n, dtype=bool)
    pattern_mask = generate_phase_mask(n)

    prev = np.zeros(2)

    for t in range(n):

        if not pattern_mask[t]:
            continue

        b = basin_ids[t]

        if b != source_basin:
            continue

        # 🔥 NEW: adjacency constraint
        if target_basin not in adjacency.get(b, []):
            continue

        s = controlled[t]
        target = centroids[target_basin]

        # --- distance
        dr = target[0] - s[0]
        dtheta = wrap_theta(target[1] - s[1])

        u_target = np.array([dr, dtheta])
        norm = np.linalg.norm(u_target)
        if norm > 1e-9:
            u_target /= norm

        u_base = raw_controls[t]

        u = base_gain * eta * u_base + gain * u_target

        # clamp
        nrm = np.linalg.norm(u)
        if nrm > max_step:
            u = u / nrm * max_step

        # smoothing
        u = (1 - smoothing) * u + smoothing * prev

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[t] = s_new
        active_mask[t] = True
        prev = u

    return controlled, active_mask, pattern_mask


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    source = 0
    target = 1

    adjacency = build_adjacency(
        data["transition_probs"],
        data["basin_list"],
        threshold=0.05
    )

    controlled, active, pattern = adjacency_pattern_control(
        aligned_states=data["aligned"],
        raw_controls=data["raw_controls"],
        basin_ids=data["basin_ids"],
        locking_score=data["L"],
        centroids=data["centroids"],
        adjacency=adjacency,
        source_basin=source,
        target_basin=target
    )

    # --------------------------------------------------------
    # Evaluate transitions
    # --------------------------------------------------------

    new_ids = assign_nearest_basin(controlled, data["centroids"])
    segments = extract_segments_from_ids(new_ids)

    _, probs2, basin_list2, _ = data["transition_counts"], data["transition_probs"], data["basin_list"], data["segments"]

    p_before = transition_probability(
        data["transition_probs"],
        data["basin_list"],
        source,
        target
    )

    p_after = transition_probability(
        probs2,
        basin_list2,
        source,
        target
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8,8))

    plt.scatter(
        data["aligned"][:,1],
        data["aligned"][:,0],
        s=2, alpha=0.2
    )

    plt.scatter(
        controlled[:,1],
        controlled[:,0],
        s=3, alpha=0.5
    )

    plt.scatter(
        controlled[active,1],
        controlled[active,0],
        s=10, label="active"
    )

    plt.title(
        f"v54 Adjacency Pattern Control P={p_before:.3f}→{p_after:.3f}"
    )

    plt.legend()
    plt.tight_layout()

    png_path = os.path.join(
        OUT_DIR,
        f"v54_adjacency_pattern_B{source}_to_B{target}.png"
    )

    plt.savefig(png_path, dpi=200)
    plt.close()

    print("NEXAH v54 complete")
    print(f"Adjacency: {adjacency}")
    print(f"P before: {p_before:.4f}")
    print(f"P after:  {p_after:.4f}")
    print(f"Saved: {png_path}")
