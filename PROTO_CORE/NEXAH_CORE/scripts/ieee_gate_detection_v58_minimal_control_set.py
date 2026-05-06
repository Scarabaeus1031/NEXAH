# ============================================================
# NEXAH — IEEE GATE DETECTION v58
# Minimal Control Set (Cluster Reduction Study)
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v57_clustered_pattern_control import (
    build_pipeline,
    pattern_field_mask,
    cluster_pattern,
    select_best_cluster,
    clustered_pattern_control
)

from ieee_gate_detection_v56_pattern_field_control import (
    assign_nearest_basin,
    transition_probability
)

from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


# ------------------------------------------------------------
# RUN EXPERIMENT
# ------------------------------------------------------------

def evaluate_subset(data, subset_indices, source, target):

    controlled, active = clustered_pattern_control(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target,
        subset_indices
    )

    controlled_ids = assign_nearest_basin(
        controlled,
        data["centroids"]
    )

    counts, probs, basin_list, _ = compute_transition_matrix_from_segments(
        controlled_ids
    )

    return transition_probability(
        probs,
        basin_list,
        source,
        target
    )


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

    # --- v57 cluster ---
    mask = pattern_field_mask(
        data["aligned"],
        data["basin_ids"],
        data["centroids"],
        source
    )

    _, cluster_map = cluster_pattern(
        data["aligned"],
        mask
    )

    full_cluster = select_best_cluster(
        cluster_map,
        data["aligned"],
        data["centroids"],
        target
    )

    full_cluster = np.array(full_cluster)

    # --------------------------------------------------------
    # reduction levels
    # --------------------------------------------------------

    fractions = [1.0, 0.75, 0.5, 0.25, 0.1, 0.05]

    results = []

    for f in fractions:

        k = max(1, int(len(full_cluster) * f))

        # random subset
        subset = np.random.choice(full_cluster, size=k, replace=False)

        p = evaluate_subset(data, subset, source, target)

        results.append((k, p))

    # --- single point test
    best_single = None
    best_p = 0

    for idx in full_cluster:

        p = evaluate_subset(data, [idx], source, target)

        if p > best_p:
            best_p = p
            best_single = idx

    results.append((1, best_p))

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    tag = f"B{source}_to_B{target}"

    summary_path = os.path.join(
        OUT_DIR,
        f"v58_minimal_control_summary_{tag}.txt"
    )

    with open(summary_path, "w") as f:

        f.write("NEXAH v58 — Minimal Control Set\n")
        f.write("================================\n\n")

        f.write(f"Original cluster size: {len(full_cluster)}\n\n")

        for k, p in results:
            f.write(f"Points: {k:3d} → P: {p:.4f}\n")

    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    ks = [r[0] for r in results]
    ps = [r[1] for r in results]

    plt.figure(figsize=(6, 4))
    plt.plot(ks, ps, marker="o")

    plt.xlabel("Number of control points")
    plt.ylabel("Transition probability P(B0→B1)")
    plt.title("NEXAH v58 — Minimal Control Set")

    plt.grid(True)
    plt.tight_layout()

    plot_path = os.path.join(
        OUT_DIR,
        f"v58_minimal_control_curve_{tag}.png"
    )

    plt.savefig(plot_path, dpi=200)
    plt.close()

    print("NEXAH v58 complete")
    print(f"Saved: {summary_path}")
    print(f"Saved: {plot_path}")
