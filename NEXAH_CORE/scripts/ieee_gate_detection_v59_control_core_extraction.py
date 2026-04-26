# ============================================================
# NEXAH v59 — Control Core Extraction (ΔP-based FINAL)
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
from ieee_gate_detection_v44_basin_identity import cluster_locked_basins


# ------------------------------------------------------------
# Compute transition probability
# ------------------------------------------------------------

def compute_P(basin_ids, source, target):

    counts, probs, basin_list, _ = compute_transition_matrix_from_segments(basin_ids)

    if source not in basin_list:
        return 0.0

    i = basin_list.index(source)

    if target >= probs.shape[1]:
        return 0.0

    return probs[i, target]


# ------------------------------------------------------------
# Influence scoring (CORRECT)
# ------------------------------------------------------------

def compute_influence(states, controls, basin_ids, centroids, source, target):

    # full controlled system
    controlled, active, mask = pattern_field_control(
        states, controls, basin_ids, centroids, source, target
    )

    controlled_ids, *_ = cluster_locked_basins(
        controlled,
        np.ones(len(controlled)) * 0.5,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    full_P = compute_P(controlled_ids, source, target)

    active_indices = np.where(active)[0]
    influence = []

    for idx in active_indices:

        test_states = controlled.copy()
        test_states[idx] = states[idx]

        test_ids, *_ = cluster_locked_basins(
            test_states,
            np.ones(len(test_states)) * 0.5,
            threshold=0.5,
            eps=0.18,
            min_samples=6
        )

        test_P = compute_P(test_ids, source, target)

        delta = full_P - test_P

        influence.append((idx, delta))

    influence.sort(key=lambda x: x[1], reverse=True)

    return influence, active_indices, controlled, active, full_P


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

    plt.title("NEXAH v59 — Control Core Extraction (ΔP)")
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

        f.write("NEXAH v59 — Control Core Extraction (ΔP-based)\n")
        f.write("==============================================\n\n")

        f.write(f"Full P: {full_P:.4f}\n")
        f.write(f"Active points: {len(active_indices)}\n\n")

        f.write("Top influence points:\n")

        for idx, score in influence[:top_k]:
            f.write(f"  index {idx} → ΔP = {score:.6f}\n")

    print("NEXAH v59 complete (ΔP-based)")
    print(f"Full P: {full_P:.4f}")
    print(f"Top-{top_k} core extracted")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
