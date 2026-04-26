# ============================================================
# NEXAH — IEEE GATE DETECTION v65
# Structure-Aware Learned Flow Field
# ============================================================
#
# FILE:
# ieee_gate_detection_v65_structure_aware_flow.py
#
# PURPOSE:
# --------
# Upgrade v64 learned average-flow dynamics by adding structure.
#
# v64:
#   f(s) = local mean flow
#
# v65:
#   f(s) =
#       local mean flow
#     + ridge attraction
#     + basin-centroid attraction
#     + control impulse
#
# GOAL:
# -----
# Test whether structure-aware dynamics amplify a local control
# intervention into a persistent trajectory deviation.
#
# OUTPUTS:
# --------
# v65_structure_aware_flow_trajectory.png
# v65_structure_aware_flow_deviation.png
# v65_structure_aware_flow_summary.txt
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control
from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v47_memory_guided_control import compute_basin_centroids
from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta


# ------------------------------------------------------------
# Build base trajectory
# ------------------------------------------------------------

def build_pipeline():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    L = np.ones(len(states)) * 0.5

    basin_ids, *_ = cluster_locked_basins(
        states,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    centroids = compute_basin_centroids(states, basin_ids)

    return states, basin_ids, centroids


# ------------------------------------------------------------
# Learned local flow
# ------------------------------------------------------------

def learn_local_flow(states, k=25):

    velocities = np.gradient(states, axis=0)

    def flow(s):

        dtheta = np.array([
            wrap_theta(p[1] - s[1]) for p in states
        ])

        dr = states[:, 0] - s[0]

        dists = np.sqrt(dr**2 + dtheta**2)

        idx = np.argsort(dists)[:k]

        return np.mean(velocities[idx], axis=0)

    return flow


# ------------------------------------------------------------
# Nearest basin centroid
# ------------------------------------------------------------

def nearest_centroid_vector(s, centroids):

    best = None
    best_dist = np.inf

    for bid, c in centroids.items():

        dr = c[0] - s[0]
        dtheta = wrap_theta(c[1] - s[1])

        dist = np.sqrt(dr**2 + dtheta**2)

        if dist < best_dist:
            best_dist = dist
            best = np.array([dr, dtheta])

    norm = np.linalg.norm(best)

    if norm > 1e-9:
        best = best / norm

    return best


# ------------------------------------------------------------
# Target centroid vector
# ------------------------------------------------------------

def target_vector(s, target_centroid):

    dr = target_centroid[0] - s[0]
    dtheta = wrap_theta(target_centroid[1] - s[1])

    u = np.array([dr, dtheta])

    norm = np.linalg.norm(u)

    if norm > 1e-9:
        u = u / norm

    return u


# ------------------------------------------------------------
# Structure-aware flow
# ------------------------------------------------------------

def structure_aware_flow(
    s,
    local_flow,
    centroids,
    target_centroid=None,
    ridge_gain=0.018,
    target_gain=0.000
):

    v = local_flow(s)

    # Pull gently toward nearest structural centroid.
    v += ridge_gain * nearest_centroid_vector(s, centroids)

    # Optional target bias.
    if target_centroid is not None and target_gain > 0:
        v += target_gain * target_vector(s, target_centroid)

    return v


# ------------------------------------------------------------
# Simulate dynamics
# ------------------------------------------------------------

def simulate(
    s0,
    local_flow,
    centroids,
    target_centroid=None,
    steps=300,
    dt=0.08,
    control_step=None,
    control_vector=None,
    control_gain=0.12,
    ridge_gain=0.018,
    target_gain=0.000
):

    traj = [s0.copy()]
    s = s0.copy()

    for step in range(steps):

        v = structure_aware_flow(
            s,
            local_flow,
            centroids,
            target_centroid=target_centroid,
            ridge_gain=ridge_gain,
            target_gain=target_gain
        )

        if control_step is not None and step == control_step:
            v = v + control_gain * control_vector

        s = s + dt * v
        s[1] = wrap_theta(s[1])

        traj.append(s.copy())

    return np.array(traj)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states, basin_ids, centroids = build_pipeline()

    print("Available basins:", sorted(centroids.keys()))

    source = 0 if 0 in centroids else sorted(centroids.keys())[0]
    target = 1 if 1 in centroids else sorted(centroids.keys())[1]

    target_centroid = centroids[target]

    local_flow = learn_local_flow(states, k=25)

    start_index = 67
    s0 = states[start_index].copy()

    # Same direction seen in v62: nearly pure negative theta rotation.
    control_vector = target_vector(s0, target_centroid)

    baseline = simulate(
        s0,
        local_flow,
        centroids,
        target_centroid=None,
        steps=300,
        dt=0.08,
        ridge_gain=0.018,
        target_gain=0.000
    )

    controlled = simulate(
        s0,
        local_flow,
        centroids,
        target_centroid=target_centroid,
        steps=300,
        dt=0.08,
        control_step=10,
        control_vector=control_vector,
        control_gain=0.12,
        ridge_gain=0.018,
        target_gain=0.004
    )

    deviation = np.linalg.norm(controlled - baseline, axis=1)

    final_dev = float(deviation[-1])
    max_dev = float(np.max(deviation))
    mean_dev = float(np.mean(deviation))

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        states[:, 1],
        states[:, 0],
        s=2,
        alpha=0.10,
        label="data field"
    )

    plt.plot(
        baseline[:, 1],
        baseline[:, 0],
        linewidth=2,
        label="baseline structure-flow"
    )

    plt.plot(
        controlled[:, 1],
        controlled[:, 0],
        linewidth=2,
        label="controlled structure-flow"
    )

    plt.scatter(
        s0[1],
        s0[0],
        color="red",
        s=70,
        label=f"start {start_index}"
    )

    plt.scatter(
        target_centroid[1],
        target_centroid[0],
        marker="x",
        s=90,
        label=f"target basin {target}"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v65 — Structure-Aware Learned Flow")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v65_structure_aware_flow_trajectory.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot deviation
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))

    plt.plot(deviation, linewidth=1.5)
    plt.axvline(10, linestyle="--", label="control step")

    plt.xlabel("simulation step")
    plt.ylabel("controlled - baseline deviation")
    plt.title("NEXAH v65 — Structure-Aware Flow Deviation")

    plt.legend(fontsize=8)
    plt.tight_layout()

    dev_path = os.path.join(
        OUT_DIR,
        "v65_structure_aware_flow_deviation.png"
    )

    plt.savefig(dev_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v65_structure_aware_flow_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:

        f.write("NEXAH v65 — Structure-Aware Learned Flow\n")
        f.write("========================================\n\n")

        f.write(f"Start index: {start_index}\n")
        f.write(f"Source basin: {source}\n")
        f.write(f"Target basin: {target}\n")
        f.write(f"Available basins: {sorted(centroids.keys())}\n\n")

        f.write(f"Control step: 10\n")
        f.write(f"Control vector: {control_vector}\n\n")

        f.write("Parameters:\n")
        f.write("  k neighbors: 25\n")
        f.write("  dt: 0.08\n")
        f.write("  ridge_gain: 0.018\n")
        f.write("  target_gain controlled: 0.004\n")
        f.write("  control_gain: 0.12\n\n")

        f.write(f"Final deviation: {final_dev:.6f}\n")
        f.write(f"Max deviation:   {max_dev:.6f}\n")
        f.write(f"Mean deviation:  {mean_dev:.6f}\n")

    print("NEXAH v65 complete")
    print(f"Source -> Target: {source} -> {target}")
    print(f"Final deviation: {final_dev:.6f}")
    print(f"Max deviation:   {max_dev:.6f}")
    print(f"Mean deviation:  {mean_dev:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {dev_path}")
    print(f"Saved: {summary_path}")
