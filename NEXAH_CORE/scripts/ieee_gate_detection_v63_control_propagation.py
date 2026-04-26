# ============================================================
# NEXAH — IEEE GATE DETECTION v63
# Control Propagation Test
# ============================================================
#
# FILE:
# ieee_gate_detection_v63_control_propagation.py
#
# PURPOSE:
# --------
# Test whether a single local control intervention propagates
# forward along the trajectory.
#
# BUILDS ON:
# ----------
# v56 pattern-field pipeline
#
# OUTPUTS:
# --------
# v63_control_propagation_B{source}_to_B{target}.png
# v63_control_propagation_deviation_B{source}_to_B{target}.png
# v63_control_propagation_summary_B{source}_to_B{target}.txt
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

from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta


# ------------------------------------------------------------
# Single-point control
# ------------------------------------------------------------

def apply_single_control(states, index, target_centroid, gain=0.08):
    controlled = states.copy()

    s = controlled[index]

    dr = target_centroid[0] - s[0]
    dtheta = wrap_theta(target_centroid[1] - s[1])

    u = np.array([dr, dtheta])
    norm = np.linalg.norm(u)

    if norm > 1e-9:
        u = u / norm

    controlled[index] = s + gain * u
    controlled[index, 1] = wrap_theta(controlled[index, 1])

    return controlled, u


# ------------------------------------------------------------
# Forward propagation model
# ------------------------------------------------------------

def forward_propagation(states, start_index, steps=120, alpha=0.035, decay=0.985):
    """
    Simple causal propagation model.

    The perturbation at start_index is propagated forward along
    the trajectory using local displacement continuity.
    """

    traj = states.copy()

    displacement = traj[start_index] - states[start_index]

    for k in range(start_index + 1, min(len(states), start_index + steps)):

        displacement = displacement * decay

        traj[k] = states[k] + alpha * displacement
        traj[k, 1] = wrap_theta(traj[k, 1])

    return traj


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    data = build_pipeline()

    states = data["aligned"]
    basin_ids = data["basin_ids"]
    centroids = data["centroids"]

    print("Available basins:", sorted(centroids.keys()))

    source = 0 if 0 in centroids else sorted(centroids.keys())[0]
    target = 1 if 1 in centroids else sorted(centroids.keys())[1]

    target_c = centroids[target]

    # Use v56 active region to select a valid control point.
    _, active, _ = pattern_field_control(
        states=states,
        controls=data["controls"],
        basin_ids=basin_ids,
        centroids=centroids,
        source=source,
        target=target
    )

    active_indices = np.where(active)[0]

    if len(active_indices) == 0:
        raise ValueError("No active control points found from v56 pattern field.")

    preferred_index = 67
    if preferred_index in active_indices:
        core_index = preferred_index
    else:
        core_index = int(active_indices[0])

    controlled_once, control_vector = apply_single_control(
        states,
        core_index,
        target_c,
        gain=0.08
    )

    propagated = forward_propagation(
        controlled_once,
        start_index=core_index,
        steps=160,
        alpha=0.035,
        decay=0.985
    )

    deviation = np.linalg.norm(propagated - states, axis=1)

    max_dev = float(np.max(deviation))
    mean_dev = float(np.mean(deviation))
    local_dev = float(deviation[core_index])

    tag = f"B{source}_to_B{target}"

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        states[:, 1],
        states[:, 0],
        s=2,
        alpha=0.18,
        label="baseline"
    )

    plt.scatter(
        propagated[:, 1],
        propagated[:, 0],
        s=3,
        alpha=0.55,
        label="propagated"
    )

    plt.scatter(
        states[core_index, 1],
        states[core_index, 0],
        color="red",
        s=70,
        label=f"control point {core_index}"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v63 — Single-Point Control Propagation")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v63_control_propagation_{tag}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot deviation profile
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))

    plt.plot(deviation, linewidth=1.2)
    plt.axvline(core_index, linestyle="--", label=f"control index {core_index}")

    plt.xlabel("trajectory index")
    plt.ylabel("deviation from baseline")
    plt.title("NEXAH v63 — Forward Deviation Profile")

    plt.legend(fontsize=8)
    plt.tight_layout()

    dev_path = os.path.join(
        OUT_DIR,
        f"v63_control_propagation_deviation_{tag}.png"
    )

    plt.savefig(dev_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v63_control_propagation_summary_{tag}.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v63 — Control Propagation Test\n")
        f.write("====================================\n\n")
        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n")
        f.write(f"Available basins: {sorted(centroids.keys())}\n\n")
        f.write(f"Control index: {core_index}\n")
        f.write(f"Control vector: {control_vector}\n\n")
        f.write(f"Local deviation: {local_dev:.6f}\n")
        f.write(f"Max deviation:   {max_dev:.6f}\n")
        f.write(f"Mean deviation:  {mean_dev:.6f}\n\n")
        f.write(f"Active v56 control points: {len(active_indices)}\n")

    print("NEXAH v63 complete")
    print(f"Source -> Target: {source} -> {target}")
    print(f"Control index: {core_index}")
    print(f"Max deviation:  {max_dev:.6f}")
    print(f"Mean deviation: {mean_dev:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {dev_path}")
    print(f"Saved: {summary_path}")
