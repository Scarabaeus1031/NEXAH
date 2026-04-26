# ============================================================
# NEXAH — IEEE GATE DETECTION v59
# Control Core Extraction (Window-Based FIX)
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
# Transition detection (WINDOW-BASED)
# ------------------------------------------------------------

def detect_transitions(basin_ids, source, target, window=5):

    indices = []

    for i in range(len(basin_ids) - window):

        if basin_ids[i] != source:
            continue

        for j in range(1, window+1):
            if basin_ids[i+j] == target:
                indices.append(i)
                break

    return indices


# ------------------------------------------------------------
# Influence scoring
# ------------------------------------------------------------

def compute_influence(states, controls, basin_ids, centroids, source, target):

    controlled, active, mask = pattern_field_control(
        states, controls, basin_ids, centroids, source, target
    )

    # baseline transitions
    baseline_transitions = detect_transitions(basin_ids, source, target)
    full_count = len(baseline_transitions)

    active_indices = np.where(active)[0]
    influence = []

    for idx in active_indices:

        loss = 0

        for t in baseline_transitions:

            # if control point lies near transition region
            if abs(idx - t) < 6:
                loss += 1

        influence.append((idx, loss))

    influence.sort(key=lambda x: x[1], reverse=True)

    return influence, active_indices, controlled, active, full_count


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

    influence, active_indices, controlled, active, full_count = compute_influence(
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
        s=35,
        c="red",
        label="control core"
    )

    plt.title("NEXAH v59 — Control Core Extraction (Window-Based)")
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

        f.write("NEXAH v59 — Control Core Extraction (Window-Based)\n")
        f.write("=================================================\n\n")

        f.write(f"Detected transitions: {full_count}\n")
        f.write(f"Total active points: {len(active_indices)}\n")
        f.write(f"Top-k core points: {top_k}\n\n")

        f.write("Top influence points:\n")

        for idx, score in influence[:top_k]:
            f.write(f"  index {idx} → influence {score}\n")

    print("NEXAH v59 complete (window-based)")
    print(f"Transitions detected: {full_count}")
    print(f"Top-{top_k} core extracted")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
