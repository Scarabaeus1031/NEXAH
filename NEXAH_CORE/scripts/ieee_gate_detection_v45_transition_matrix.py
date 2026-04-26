# ============================================================
# NEXAH — IEEE GATE DETECTION v45
# Transition Matrix / Basin Dynamics Model
# ============================================================
#
# PURPOSE:
# --------
# Learn transition probabilities between stable basins.
#
# Builds on:
# - v44: basin identities (basin_ids over time)
#
# CORE IDEA:
# ----------
# Construct empirical transition matrix:
#
#     P(B_i → B_j)
#
# describing how the system moves between basins.
#
# OUTPUTS:
# --------
# v45_transition_matrix.png
# v45_transition_matrix.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v44_basin_identity import cluster_locked_basins
from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score
from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control
from ieee_gate_detection_v38_control_layer import run_v38_control, gradient_field, make_interpolator
from ieee_gate_detection_v39_attractor_memory import stability_score, detect_stable_attractors, attractor_memory_field


# ------------------------------------------------------------
# Transition matrix computation
# ------------------------------------------------------------

def compute_transition_matrix(basin_ids):
    """
    Compute transition counts and probabilities between basins.

    Only considers transitions where:
    basin_ids[t] != basin_ids[t+1]
    and both are valid (>= 0)
    """

    valid_ids = sorted([i for i in np.unique(basin_ids) if i >= 0])

    if len(valid_ids) == 0:
        return None, None

    id_map = {bid: i for i, bid in enumerate(valid_ids)}
    n = len(valid_ids)

    counts = np.zeros((n, n))

    for t in range(len(basin_ids) - 1):
        i = basin_ids[t]
        j = basin_ids[t + 1]

        if i >= 0 and j >= 0 and i != j:
            counts[id_map[i], id_map[j]] += 1

    # normalize rows → probabilities
    probs = np.zeros_like(counts)

    for i in range(n):
        row_sum = np.sum(counts[i])
        if row_sum > 0:
            probs[i] = counts[i] / row_sum

    return counts, probs, valid_ids


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

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
        grad_rho_interp
    )

    # --- v42
    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --- v44
    basin_ids, *_ = cluster_locked_basins(
        aligned,
        L,
        threshold=0.5,
        eps=0.18,
        min_samples=6
    )

    # --- v45 transition matrix
    counts, probs, valid_ids = compute_transition_matrix(basin_ids)

    if counts is None:
        print("No valid basins detected.")
        exit()

    # --------------------------------------------------------
    # Plot: transition matrix
    # --------------------------------------------------------

    plt.figure(figsize=(6, 5))

    plt.imshow(probs, cmap="viridis", origin="lower")
    plt.colorbar(label="P(B_i → B_j)")

    plt.xlabel("to basin j")
    plt.ylabel("from basin i")
    plt.title("NEXAH v45 — Transition Matrix")

    ticks = np.arange(len(valid_ids))
    labels = [str(b) for b in valid_ids]

    plt.xticks(ticks, labels)
    plt.yticks(ticks, labels)

    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v45_transition_matrix.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --- save arrays
    np.save(os.path.join(OUT_DIR, "v45_transition_counts.npy"), counts)
    np.save(os.path.join(OUT_DIR, "v45_transition_probs.npy"), probs)

    print("NEXAH v45 complete")
    print(f"Basins: {len(valid_ids)}")
    print("Transition matrix (counts):")
    print(counts)
    print("Transition matrix (probabilities):")
    print(probs)
    print(f"Saved: {out_path}")
