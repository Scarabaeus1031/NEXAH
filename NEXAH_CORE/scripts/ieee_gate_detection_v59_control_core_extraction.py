# ============================================================
# NEXAH v59 — Control Core Extraction (Subset-Based FINAL)
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v56_pattern_field_control import (
    build_pipeline,
    pattern_field_control
)

from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


# ------------------------------------------------------------
# Compute transition probability (FIXED BASELINE SPACE)
# ------------------------------------------------------------

def compute_P(basin_ids, source, target):

    _, probs, basin_list, _ = compute_transition_matrix_from_segments(basin_ids)

    if source not in basin_list:
        return 0.0

    i = basin_list.index(source)

    if target >= probs.shape[1]:
        return 0.0

    return probs[i, target]


# ------------------------------------------------------------
# Apply control only on subset
# ------------------------------------------------------------

def apply_subset_control(states, controls, basin_ids, centroids,
                         source, target, active_indices, subset):

    controlled = states.copy()

    target_c = centroids[target]

    for idx in subset:

        s = controlled[idx]
        u_base = controls[idx]

        dr = target_c[0] - s[0]
        dtheta = target_c[1] - s[1]

        norm = np.sqrt(dr**2 + dtheta**2)
        if norm > 1e-9:
            dr /= norm
            dtheta /= norm

        u = 0.55 * 0.02 * u_base + 0.065 * np.array([dr, dtheta])

        controlled[idx] = s + u

    return controlled


# ------------------------------------------------------------
# Influence scoring (REAL)
# ------------------------------------------------------------

def compute_influence(states, controls, basin_ids, centroids, source, target):

    # full control
    controlled_full, active, _ = pattern_field_control(
        states, controls, basin_ids, centroids, source, target
    )

    full_P = compute_P(basin_ids, source, target)

    active_indices = list(np.where(active)[0])

    influence = []

    for idx in active_indices:

        subset = [i for i in active_indices if i != idx]

        controlled = apply_subset_control(
            states, controls, basin_ids, centroids,
            source, target, active_indices, subset
        )

        # IMPORTANT: evaluate in ORIGINAL basin_ids space
        test_P = compute_P(basin_ids, source, target)

        delta = full_P - test_P

        influence.append((idx, delta))

    influence.sort(key=lambda x: x[1], reverse=True)

    return influence, active_indices, controlled_full, active, full_P


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

    influence, active_indices, controlled, active, full_P = compute_influence(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    top_k = 5
    core_indices = [i for i, _ in influence[:top_k]]

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
        alpha=0.5,
        label="controlled"
    )

    plt.scatter(
        controlled[active, 1],
        controlled[active, 0],
        s=10,
        alpha=0.5,
        label="pattern field"
    )

    plt.scatter(
        controlled[core_indices, 1],
        controlled[core_indices, 0],
        s=35,
        c="red",
        label="control core"
    )

    plt.title("NEXAH v59 — Control Core (Subset-Based)")
    plt.xlabel("theta")
    plt.ylabel("r")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v59_control_core_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v59_control_core_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w") as f:

        f.write("NEXAH v59 — Control Core (Subset-Based)\n")
        f.write("=======================================\n\n")

        f.write(f"Full P: {full_P:.4f}\n")
        f.write(f"Active points: {len(active_indices)}\n\n")

        f.write("Top influence points:\n")

        for idx, score in influence[:top_k]:
            f.write(f"  index {idx} → ΔP = {score:.6f}\n")

    print("NEXAH v59 complete (subset-based)")
    print(f"Full P: {full_P:.4f}")
