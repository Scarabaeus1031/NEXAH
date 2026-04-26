# ============================================================
# NEXAH — IEEE GATE DETECTION v59
# Control Core Extraction (Trajectory-Based Influence)
# ============================================================

# FILE:
# ieee_gate_detection_v59_control_core_extraction.py

# PURPOSE:
# --------
# Identify which control points actually drive transitions
# WITHOUT re-clustering (fixed basin reference).
#
# METHOD:
# --------
# Measure influence based on local transition loss along trajectory.
#
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


# ------------------------------------------------------------
# Compute baseline transitions
# ------------------------------------------------------------

def get_transition_indices(basin_ids, source, target):

    transitions = []

    for i in range(len(basin_ids) - 1):
        if basin_ids[i] == source and basin_ids[i + 1] == target:
            transitions.append(i)

    return transitions


# ------------------------------------------------------------
# Influence scoring (NO re-clustering)
# ------------------------------------------------------------

def compute_influence_scores(states, controls, basin_ids, centroids, source, target):

    controlled, active, mask = pattern_field_control(
        states, controls, basin_ids, centroids, source, target
    )

    # baseline transitions (fixed reference)
    baseline_transitions = get_transition_indices(basin_ids, source, target)

    active_indices = np.where(active)[0]
    influence = []

    window = 3  # local neighborhood size

    for idx in active_indices:

        loss = 0

        for t in baseline_transitions:
            if abs(t - idx) <= window:
                loss += 1

        influence.append((idx, loss))

    influence.sort(key=lambda x: x[1], reverse=True)

    return influence, active_indices, controlled, active, baseline_transitions


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

    influence, active_indices, controlled, active, transitions = compute_influence_scores(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    # --------------------------------------------------------
    # Select core
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
        s=40,
        c="red",
        label="control core"
    )

    plt.title("NEXAH v59 — Control Core Extraction (Trajectory-Based)")
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

        f.write("NEXAH v59 — Control Core Extraction (Trajectory-Based)\n")
        f.write("======================================================\n\n")

        f.write(f"Total active points: {len(active_indices)}\n")
        f.write(f"Detected transitions: {len(transitions)}\n")
        f.write(f"Top-k core points: {top_k}\n\n")

        f.write("Top influence points:\n")

        for idx, score in influence[:top_k]:
            f.write(f"  index {idx} → influence {score}\n")

    print("NEXAH v59 complete (trajectory-based)")
    print(f"Transitions detected: {len(transitions)}")
    print(f"Top-{top_k} core extracted")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
