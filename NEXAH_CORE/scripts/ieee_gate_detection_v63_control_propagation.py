# ============================================================
# NEXAH — IEEE GATE DETECTION v63
# Control Propagation Test (Forward Influence)
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control
from ieee_gate_detection_v41_ridge_aligned_control import (
    ridge_aligned_control,
    wrap_theta
)
from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids


# ------------------------------------------------------------
# Build pipeline
# ------------------------------------------------------------

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([result["r"], result["theta"]])

    aligned = ridge_aligned_control(
        states,
        result["controls"],
        None,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    L = np.ones(len(aligned)) * 0.5

    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    centroids = compute_basin_centroids(aligned, basin_ids)

    return aligned, basin_ids, centroids


# ------------------------------------------------------------
# Apply single-point control
# ------------------------------------------------------------

def apply_single_control(states, index, target, gain=0.08):

    controlled = states.copy()

    s = controlled[index]

    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])

    u = np.array([dr, dtheta])
    norm = np.linalg.norm(u)

    if norm > 1e-9:
        u = u / norm

    controlled[index] = s + gain * u
    controlled[index][1] = wrap_theta(controlled[index][1])

    return controlled


# ------------------------------------------------------------
# Forward propagation (simulate trajectory drift)
# ------------------------------------------------------------

def forward_propagation(states, steps=50):

    traj = states.copy()

    for _ in range(steps):

        dr = np.gradient(traj[:, 0])
        dtheta = np.gradient(traj[:, 1])

        traj[:, 0] += 0.01 * dr
        traj[:, 1] += 0.01 * dtheta
        traj[:, 1] = np.array([wrap_theta(t) for t in traj[:, 1]])

    return traj


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states, basin_ids, centroids = build_pipeline()

    source = 0
    target = 1

    target_c = centroids[target]

    # pick one core point manually (from v59)
    core_index = 67

    controlled_once = apply_single_control(states, core_index, target_c)

    propagated = forward_propagation(controlled_once, steps=80)

    # --------------------------------------------------------
    # Measure deviation
    # --------------------------------------------------------

    deviation = np.linalg.norm(propagated - states, axis=1)

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(states[:, 1], states[:, 0], s=2, alpha=0.2, label="baseline")

    plt.scatter(
        propagated[:, 1],
        propagated[:, 0],
        s=3,
        alpha=0.6,
        label="propagated"
    )

    plt.scatter(
        states[core_index, 1],
        states[core_index, 0],
        color="red",
        s=60,
        label="control point"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v63 — Control Propagation Test")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        f"v63_control_propagation_B{source}_to_B{target}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v63_control_propagation_summary_B{source}_to_B{target}.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH v63 — Control Propagation Test\n")
        f.write("====================================\n\n")
        f.write(f"Control index: {core_index}\n")
        f.write(f"Max deviation: {np.max(deviation):.6f}\n")
        f.write(f"Mean deviation: {np.mean(deviation):.6f}\n")

    print("NEXAH v63 complete")
    print(f"Max deviation: {np.max(deviation):.6f}")
    print(f"Saved: {out_path}")
