# ============================================================
# NEXAH v61 — Local Flow Transformation Analysis
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

from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta


# ------------------------------------------------------------
# Compute dr/dθ
# ------------------------------------------------------------

def compute_flow(states):

    r = states[:, 0]
    theta = states[:, 1]

    dr = np.gradient(r)
    dtheta = np.gradient(theta)

    # avoid division by zero
    dtheta = np.where(np.abs(dtheta) < 1e-6, 1e-6, dtheta)

    flow = dr / dtheta

    return flow


# ------------------------------------------------------------
# Analyze flow change
# ------------------------------------------------------------

def analyze_flow_change(before, after, indices):

    flow_before = compute_flow(before)
    flow_after = compute_flow(after)

    delta_flow = flow_after - flow_before

    return flow_before, flow_after, delta_flow


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

    controlled, active, mask = pattern_field_control(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    active_indices = np.where(active)[0]

    # take small core (like v58/v59)
    core_indices = active_indices[:5]

    flow_before, flow_after, delta_flow = analyze_flow_change(
        data["aligned"],
        controlled,
        core_indices
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 6))

    plt.scatter(
        data["aligned"][:, 1],
        data["aligned"][:, 0],
        s=2,
        alpha=0.2,
        label="baseline"
    )

    # highlight flow-change points
    plt.scatter(
        controlled[core_indices, 1],
        controlled[core_indices, 0],
        c="red",
        s=40,
        label="control core"
    )

    # annotate Δflow
    for idx in core_indices:
        plt.text(
            controlled[idx, 1],
            controlled[idx, 0],
            f"{delta_flow[idx]:.2f}",
            fontsize=6
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v61 — Local Flow Change at Control Core")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v61_flow_transformation_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v61_flow_transformation_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w") as f:

        f.write("NEXAH v61 — Flow Transformation Analysis\n")
        f.write("========================================\n\n")

        for idx in core_indices:
            f.write(
                f"index {idx} → "
                f"before: {flow_before[idx]:.4f}, "
                f"after: {flow_after[idx]:.4f}, "
                f"Δ: {delta_flow[idx]:.4f}\n"
            )

    print("NEXAH v61 complete")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
