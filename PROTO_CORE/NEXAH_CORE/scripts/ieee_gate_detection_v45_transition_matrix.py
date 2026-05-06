# ============================================================
# NEXAH — IEEE GATE DETECTION v45 (FIXED)
# Basin Transition Matrix (Segment-Based)
# ============================================================
#
# PURPOSE:
# --------
# Compute transitions between basins using SEGMENT logic:
#
#   Basin A → (Greyspace) → Basin B
#
# instead of incorrect stepwise transitions.
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
# SEGMENT-BASED TRANSITION MATRIX
# ------------------------------------------------------------

def compute_transition_matrix_from_segments(basin_ids):
    """
    Compute transitions between basins using segment logic.

    Transition:
        Basin_i → Basin_j
    where system leaves i, goes through greyspace, enters j.
    """

    segments = []
    current = None

    # --- extract basin segments
    for t, b in enumerate(basin_ids):
        if b >= 0:
            if current is None:
                current = [b, t, t]
            elif current[0] == b:
                current[2] = t
            else:
                segments.append(tuple(current))
                current = [b, t, t]
        else:
            if current is not None:
                segments.append(tuple(current))
                current = None

    if current is not None:
        segments.append(tuple(current))

    # --- basin IDs
    basin_list = sorted(list(set([s[0] for s in segments])))
    id_map = {b: i for i, b in enumerate(basin_list)}
    n = len(basin_list)

    counts = np.zeros((n, n))

    # --- transitions between segments
    for i in range(len(segments) - 1):
        b1 = segments[i][0]
        b2 = segments[i + 1][0]

        if b1 != b2:
            counts[id_map[b1], id_map[b2]] += 1

    # --- normalize to probabilities
    probs = np.zeros_like(counts)

    for i in range(n):
        s = counts[i].sum()
        if s > 0:
            probs[i] = counts[i] / s

    return counts, probs, basin_list, segments


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

    # --- v45 (FIXED)
    counts, probs, basin_list, segments = compute_transition_matrix_from_segments(basin_ids)

    # --------------------------------------------------------
    # Plot transition matrix
    # --------------------------------------------------------

    plt.figure(figsize=(6, 5))

    plt.imshow(probs, cmap="viridis", origin="lower")
    plt.colorbar(label="P(B_i → B_j)")

    plt.xlabel("to basin j")
    plt.ylabel("from basin i")
    plt.title("NEXAH v45 — Transition Matrix (Segment-Based)")

    ticks = np.arange(len(basin_list))
    labels = [str(b) for b in basin_list]

    plt.xticks(ticks, labels)
    plt.yticks(ticks, labels)

    plt.tight_layout()

    out_path = os.path.join(OUT_DIR, "v45_transition_matrix.png")
    plt.savefig(out_path, dpi=200)
    plt.close()

    # --- save arrays
    np.save(os.path.join(OUT_DIR, "v45_transition_counts.npy"), counts)
    np.save(os.path.join(OUT_DIR, "v45_transition_probs.npy"), probs)

    # --- print results
    print("NEXAH v45 complete (FIXED)")
    print(f"Basins: {len(basin_list)}")
    print(f"Segments detected: {len(segments)}")

    print("\nTransition counts:")
    print(counts)

    print("\nTransition probabilities:")
    print(probs)

    print(f"\nSaved: {out_path}")
