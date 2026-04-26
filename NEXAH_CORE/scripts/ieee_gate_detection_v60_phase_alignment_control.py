# ============================================================
# NEXAH v60 — Phase-Aligned Control Core Analysis
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v56_pattern_field_control import build_pipeline, pattern_field_control
from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


# ------------------------------------------------------------
# Phase Shift Test
# ------------------------------------------------------------

def test_phase_shift_effect(
    states,
    controls,
    basin_ids,
    centroids,
    source,
    target,
    core_indices,
    shifts=np.linspace(-0.5, 0.5, 25)
):

    results = []

    for shift in shifts:

        shifted_states = states.copy()

        # apply phase shift ONLY to core
        for idx in core_indices:
            shifted_states[idx, 1] = wrap_theta(
                shifted_states[idx, 1] + shift
            )

        controlled, active, _ = pattern_field_control(
            shifted_states,
            controls,
            basin_ids,
            centroids,
            source,
            target
        )

        _, probs, _, _ = compute_transition_matrix_from_segments(
            basin_ids
        )

        P = probs[source, target] if probs is not None else 0

        results.append((shift, P))

    return np.array(results)


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

    # --- use known active region (from v56) ---
    _, active, _ = pattern_field_control(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    active_indices = np.where(active)[0]

    # --- take small core (like v59) ---
    core_indices = active_indices[:5]

    results = test_phase_shift_effect(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target,
        core_indices
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(6,4))
    plt.plot(results[:,0], results[:,1], "-o")

    plt.xlabel("Phase shift Δθ")
    plt.ylabel("P(transition)")
    plt.title("NEXAH v60 — Phase Sensitivity of Control Core")

    plt.grid(True)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v60_phase_alignment_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v60_phase_alignment_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH v60 — Phase Alignment Analysis\n")
        f.write("===================================\n\n")
        f.write(f"Core points tested: {len(core_indices)}\n\n")

        for s, p in results:
            f.write(f"Δθ = {s:.3f} → P = {p:.4f}\n")

    print("NEXAH v60 complete")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
