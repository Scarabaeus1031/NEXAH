# ============================================================
# NEXAH v62 — Directional Control Vector Analysis (Zoomed)
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
# Compute local vectors
# ------------------------------------------------------------

def compute_vectors(states, controls, centroids, indices, target):

    vectors = []

    target_c = centroids[target]

    for idx in indices:

        s = states[idx]
        u_base = controls[idx]

        # target direction
        dr = target_c[0] - s[0]
        dtheta = wrap_theta(target_c[1] - s[1])

        u_target = np.array([dr, dtheta])
        norm = np.linalg.norm(u_target)

        if norm > 1e-9:
            u_target = u_target / norm

        vectors.append((idx, s, u_base, u_target))

    return vectors


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

    controlled, active, _ = pattern_field_control(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target
    )

    active_indices = np.where(active)[0]

    # same core assumption as before
    core_indices = active_indices[:5]

    vectors = compute_vectors(
        data["aligned"],
        data["controls"],
        data["centroids"],
        core_indices,
        target
    )

    # --------------------------------------------------------
    # ZOOM REGION (auto around core)
    # --------------------------------------------------------

    core_points = data["aligned"][core_indices]

    r_min, r_max = core_points[:,0].min()-0.3, core_points[:,0].max()+0.3
    t_min, t_max = core_points[:,1].min()-0.3, core_points[:,1].max()+0.3

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(6,6))

    # background (light)
    plt.scatter(
        data["aligned"][:,1],
        data["aligned"][:,0],
        s=2,
        alpha=0.05
    )

    # zoomed core region points
    plt.scatter(
        data["aligned"][core_indices,1],
        data["aligned"][core_indices,0],
        c="red",
        s=40,
        label="control core"
    )

    # vectors
    for idx, s, u_base, u_target in vectors:

        theta = s[1]
        r = s[0]

        # base vector (blue)
        plt.arrow(
            theta, r,
            u_base[1]*0.1, u_base[0]*0.1,
            color='blue',
            head_width=0.03,
            length_includes_head=True
        )

        # target vector (green)
        plt.arrow(
            theta, r,
            u_target[1]*0.15, u_target[0]*0.15,
            color='green',
            head_width=0.03,
            length_includes_head=True
        )

    plt.xlim(t_min, t_max)
    plt.ylim(r_min, r_max)

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v62 — Local Control Vectors (Zoom)")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v62_directional_control_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v62_directional_control_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w") as f:

        f.write("NEXAH v62 — Directional Control Analysis\n")
        f.write("========================================\n\n")

        for idx, s, u_base, u_target in vectors:

            f.write(
                f"index {idx}\n"
                f"  u_base   = {u_base}\n"
                f"  u_target = {u_target}\n\n"
            )

    print("NEXAH v62 complete")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
