# ============================================================
# NEXAH — IEEE GATE DETECTION v57
# Clustered Pattern Field Control (Discrete Control Nodes)
# ============================================================
#
# FILE:
# ieee_gate_detection_v57_clustered_pattern_control.py
#
# CORE IDEA:
# ----------
# v56:
#     pattern = continuous region
#
# v57:
#     pattern → clusters → discrete control nodes
#
# Only specific clusters are activated → not full region
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# --- imports reused from v56 pipeline ---
from ieee_gate_detection_v56_pattern_field_control import (
    build_pipeline,
    pattern_field_mask,
    assign_nearest_basin,
    transition_probability
)

from ieee_gate_detection_v41_ridge_aligned_control import wrap_theta
from ieee_gate_detection_v45_transition_matrix import compute_transition_matrix_from_segments


# ------------------------------------------------------------
# CLUSTERING
# ------------------------------------------------------------

def cluster_pattern(states, mask, eps=0.12, min_samples=4):

    points = states[mask]

    if len(points) == 0:
        return np.array([]), {}

    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = clustering.labels_

    cluster_map = {}

    for idx, lbl in zip(np.where(mask)[0], labels):
        if lbl == -1:
            continue
        cluster_map.setdefault(lbl, []).append(idx)

    return labels, cluster_map


# ------------------------------------------------------------
# SELECT BEST CLUSTER
# ------------------------------------------------------------

def select_best_cluster(cluster_map, states, centroids, target):

    if len(cluster_map) == 0:
        return []

    target_c = centroids[target]

    best_cluster = None
    best_score = np.inf

    for cid, indices in cluster_map.items():

        pts = states[indices]

        # distance to target centroid
        d = np.mean([
            np.sqrt(
                (p[0] - target_c[0])**2 +
                wrap_theta(p[1] - target_c[1])**2
            )
            for p in pts
        ])

        if d < best_score:
            best_score = d
            best_cluster = cid

    return cluster_map.get(best_cluster, [])


# ------------------------------------------------------------
# CONTROL
# ------------------------------------------------------------

def clustered_pattern_control(
    states,
    controls,
    basin_ids,
    centroids,
    source,
    target,
    active_indices,
    eta=0.02,
    gain=0.065,
    base_gain=0.55,
    max_step=0.055
):

    controlled = states.copy()
    active = np.zeros(len(states), dtype=bool)

    target_c = centroids[target]

    for i in active_indices:

        if basin_ids[i] != source:
            continue

        s = controlled[i]

        u_base = controls[i]

        dr = target_c[0] - s[0]
        dtheta = wrap_theta(target_c[1] - s[1])

        u_target = np.array([dr, dtheta])
        norm = np.linalg.norm(u_target)

        if norm > 1e-9:
            u_target = u_target / norm

        u = base_gain * eta * u_base + gain * u_target

        nrm = np.linalg.norm(u)
        if nrm > max_step:
            u = u / nrm * max_step

        s_new = s + u
        s_new[1] = wrap_theta(s_new[1])

        controlled[i] = s_new
        active[i] = True

    return controlled, active


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

    # --- v56 mask ---
    mask = pattern_field_mask(
        data["aligned"],
        data["basin_ids"],
        data["centroids"],
        source
    )

    # --- cluster ---
    labels, cluster_map = cluster_pattern(
        data["aligned"],
        mask
    )

    selected_indices = select_best_cluster(
        cluster_map,
        data["aligned"],
        data["centroids"],
        target
    )

    # --- control ---
    controlled, active = clustered_pattern_control(
        data["aligned"],
        data["controls"],
        data["basin_ids"],
        data["centroids"],
        source,
        target,
        selected_indices
    )

    # --- transitions ---
    controlled_ids = assign_nearest_basin(
        controlled,
        data["centroids"]
    )

    counts, probs, basin_list, _ = compute_transition_matrix_from_segments(
        controlled_ids
    )

    p_before = transition_probability(
        data["transition_probs"],
        data["basin_list"],
        source,
        target
    )

    p_after = transition_probability(
        probs,
        basin_list,
        source,
        target
    )

    # --------------------------------------------------------
    # PLOT
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
        alpha=0.6,
        label="v57 controlled"
    )

    plt.scatter(
        controlled[mask, 1],
        controlled[mask, 0],
        s=8,
        alpha=0.4,
        label="pattern field"
    )

    plt.scatter(
        controlled[active, 1],
        controlled[active, 0],
        s=16,
        color="red",
        label="selected cluster"
    )

    plt.title(
        f"NEXAH v57 — Clustered Pattern Control\n"
        f"P {p_before:.3f} → {p_after:.3f}"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.legend(fontsize=7)
    plt.tight_layout()

    tag = f"B{source}_to_B{target}"

    out_path = os.path.join(
        OUT_DIR,
        f"v57_clustered_pattern_{tag}.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        f"v57_clustered_pattern_summary_{tag}.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH v57 — Clustered Pattern Control\n")
        f.write("====================================\n\n")
        f.write(f"Clusters detected: {len(cluster_map)}\n")
        f.write(f"Selected cluster size: {len(selected_indices)}\n\n")
        f.write(f"P_before: {p_before:.4f}\n")
        f.write(f"P_after:  {p_after:.4f}\n")

    print("NEXAH v57 complete")
    print(f"Clusters: {len(cluster_map)}")
    print(f"Selected cluster size: {len(selected_indices)}")
    print(f"P: {p_before:.3f} → {p_after:.3f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
