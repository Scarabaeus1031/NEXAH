# ============================================================
# NEXAH — IEEE GATE DETECTION v44
# Basin Identity / Stable Region Clustering
# ============================================================
#
# PURPOSE:
# --------
# Assign identities to stable locking regions.
#
# Builds on:
# - v42: locking score L(s)
# - v43: basin membership segments
#
# CORE QUESTION:
# --------------
# Which stable basin is the system in?
#
# v43 detected WHEN the system is locked.
# v44 detects WHERE it is locked and assigns basin IDs.
#
# METHOD:
# -------
# 1. Compute v42 locking score L
# 2. Keep states with L above threshold
# 3. Cluster locked states in (r, theta)
# 4. Assign basin IDs
# 5. Plot basin identity map
#
# OUTPUTS:
# --------
# v44_basin_identity_map.png
# v44_basin_id_time.png
# v44_basin_ids.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import (
    run_v38_control,
    gradient_field,
    make_interpolator
)

from ieee_gate_detection_v39_attractor_memory import (
    stability_score,
    detect_stable_attractors,
    attractor_memory_field
)

from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control

from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score


# ------------------------------------------------------------
# Basin identity clustering
# ------------------------------------------------------------

def cluster_locked_basins(states, locking_score, threshold=0.5, eps=0.12, min_samples=6):
    """
    Cluster locked states into basin identities.

    Returns:
    --------
    basin_ids : array length T
        -1 = not locked / no basin
         0,1,2,... = basin identity
    labels_locked : cluster labels only for locked points
    locked_states : states used for clustering
    """

    locked_mask = locking_score > threshold
    locked_states = states[locked_mask]

    basin_ids = np.full(len(states), -1, dtype=int)

    if len(locked_states) == 0:
        return basin_ids, np.array([]), locked_states, locked_mask

    # Scale r and theta to comparable ranges
    X = locked_states.copy()
    X[:, 0] = (X[:, 0] - X[:, 0].mean()) / (X[:, 0].std() + 1e-9)
    X[:, 1] = (X[:, 1] - X[:, 1].mean()) / (X[:, 1].std() + 1e-9)

    clustering = DBSCAN(
        eps=eps,
        min_samples=min_samples
    ).fit(X)

    labels_locked = clustering.labels_

    basin_ids[locked_mask] = labels_locked

    return basin_ids, labels_locked, locked_states, locked_mask


def basin_summary(states, locking_score, basin_ids):
    """
    Compute basic basin statistics.
    """
    summaries = []

    valid_ids = sorted([i for i in np.unique(basin_ids) if i >= 0])

    for bid in valid_ids:
        idx = basin_ids == bid

        summaries.append({
            "basin_id": int(bid),
            "count": int(np.sum(idx)),
            "mean_r": float(np.mean(states[idx, 0])),
            "mean_theta": float(np.mean(states[idx, 1])),
            "mean_locking": float(np.mean(locking_score[idx])),
            "max_locking": float(np.max(locking_score[idx])),
        })

    return summaries


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    # --- signal
    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    # --- v38
    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([result["r"], result["theta"]])
    raw_controls = result["controls"]

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    # --- v39
    S = stability_score(rho, P, D)

    attractors = detect_stable_attractors(
        S,
        r_grid,
        theta_grid,
        percentile=98
    )

    A = attractor_memory_field(
        attractors,
        r_grid,
        theta_grid
    )

    # --- v41
    grad_rho = gradient_field(rho, r_grid, theta_grid)

    grad_rho_interp = (
        make_interpolator(grad_rho[0], r_grid, theta_grid),
        make_interpolator(grad_rho[1], r_grid, theta_grid),
    )

    aligned = ridge_aligned_control(
        states,
        raw_controls,
        grad_rho_interp,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    # --- v42
    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, A_vals, D_vals, P_vals = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --- v44 basin identity
    basin_ids, labels_locked, locked_states, locked_mask = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    summaries = basin_summary(aligned, L, basin_ids)

    # --------------------------------------------------------
    # Plot 1: basin identity map
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        aligned[:, 1],
        aligned[:, 0],
        c="lightgray",
        s=2,
        alpha=0.35,
        label="unlocked / trajectory"
    )

    locked_idx = basin_ids >= 0

    sc = plt.scatter(
        aligned[locked_idx, 1],
        aligned[locked_idx, 0],
        c=basin_ids[locked_idx],
        s=10,
        alpha=0.85,
        cmap="tab10",
        label="basin identity"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v44 — Basin Identity Map")
    plt.colorbar(sc, label="basin id")
    plt.tight_layout()

    out_path_1 = os.path.join(
        OUT_DIR,
        "v44_basin_identity_map.png"
    )

    plt.savefig(out_path_1, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot 2: basin ID over time
    # --------------------------------------------------------

    plt.figure(figsize=(10, 4))
    plt.plot(t, basin_ids, linewidth=1.0)
    plt.xlabel("time")
    plt.ylabel("basin id")
    plt.title("NEXAH v44 — Basin Identity Over Time")
    plt.tight_layout()

    out_path_2 = os.path.join(
        OUT_DIR,
        "v44_basin_id_time.png"
    )

    plt.savefig(out_path_2, dpi=200)
    plt.close()

    # --- save arrays
    np.save(os.path.join(OUT_DIR, "v44_basin_ids.npy"), basin_ids)
    np.save(os.path.join(OUT_DIR, "v44_locking_scores.npy"), L)
    np.save(os.path.join(OUT_DIR, "v44_aligned_states.npy"), aligned)

    # --- save text summary
    summary_path = os.path.join(OUT_DIR, "v44_basin_summary.txt")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v44 — Basin Identity Summary\n")
        f.write("=================================\n\n")
        f.write(f"Total states: {len(aligned)}\n")
        f.write(f"Locked states: {int(np.sum(locked_mask))}\n")
        f.write(f"Basins detected: {len(summaries)}\n\n")

        for s in summaries:
            f.write(
                f"Basin {s['basin_id']}:\n"
                f"  count:        {s['count']}\n"
                f"  mean_r:       {s['mean_r']:.4f}\n"
                f"  mean_theta:   {s['mean_theta']:.4f}\n"
                f"  mean_locking: {s['mean_locking']:.4f}\n"
                f"  max_locking:  {s['max_locking']:.4f}\n\n"
            )

    print("NEXAH v44 complete")
    print(f"Locked states: {int(np.sum(locked_mask))}")
    print(f"Basins detected: {len(summaries)}")
    print(f"Saved: {out_path_1}")
    print(f"Saved: {out_path_2}")
    print(f"Saved: {summary_path}")

    for s in summaries:
        print(
            f"Basin {s['basin_id']}: "
            f"count={s['count']}, "
            f"mean_r={s['mean_r']:.3f}, "
            f"mean_theta={s['mean_theta']:.3f}, "
            f"mean_L={s['mean_locking']:.3f}"
        )
