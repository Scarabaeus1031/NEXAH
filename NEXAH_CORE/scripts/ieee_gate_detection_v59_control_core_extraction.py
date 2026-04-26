# ============================================================
# NEXAH — IEEE GATE DETECTION v59
# Control Core Extraction (Influence Map)
# ============================================================

# FILE:
# ieee_gate_detection_v59_control_core_extraction.py

# PURPOSE:
# --------
# Identify which control points actually drive the transition.
#
# METHOD:
# --------
# Remove each control point individually and measure impact on P.
#
# OUTPUT:
# --------
# v59_control_core_B{source}_to_B{target}.png
# v59_control_core_summary_B{source}_to_B{target}.txt

# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v56_pattern_field_control import build_pipeline, pattern_field_control
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


# ------------------------------------------------------------
# Evaluate transition probability
# ------------------------------------------------------------

def evaluate_P(basin_ids, source, target):

    _, probs, basin_list, _ = compute_transition_matrix_from_segments(basin_ids)

    if source not in basin_list:
        return 0.0

    i = basin_list.index(source)

    if target >= probs.shape[1]:
        return 0.0

    return probs[i, target]


# ------------------------------------------------------------
# Influence scoring
# ------------------------------------------------------------

def compute_influence_scores(states, controls, basin_ids, centroids, source, target):

    controlled, active, mask = pattern_field_control(
        states, controls, basin_ids, centroids, source, target
    )

    baseline_P = evaluate_P(basin_ids, source, target)

    # recompute new basin ids
    new_basin_ids = basin_ids.copy()
    full_P = evaluate_P(new_basin_ids, source, target)

    active_indices = np.where(active)[0]

    influence = []

    for idx in active_indices:

        test_states = controlled.copy()

        # remove control effect at this point
        test_states[idx] = states[idx]

        test_basin_ids = new_basin_ids.copy()

        test_P = evaluate_P(test_basin_ids, source, target)

        drop = full_P - test_P

        influence.append((idx, drop))

    influence.sort(key=lambda x: x[1], reverse=True)

    return influence, active_indices, controlled, active


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

    influence, active_indices, controlled, active = compute_influence_scores(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    # --------------------------------------------------------
    # Select top core
    # --------------------------------------------------------

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
        s=30,
        c="red",
        label="control core"
    )

    plt.title("NEXAH v59 — Control Core Extraction")
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

        f.write("NEXAH v59 — Control Core Extraction\n")
        f.write("===================================\n\n")

        f.write(f"Total active points: {len(active_indices)}\n")
        f.write(f"Top-k core points: {top_k}\n\n")

        f.write("Top influence points:\n")

        for idx, score in influence[:top_k]:
            f.write(f"  index {idx} → influence {score:.4f}\n")

    print("NEXAH v59 complete")
    print(f"Top-{top_k} core extracted")
