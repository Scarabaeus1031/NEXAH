# ============================================================
# NEXAH — IEEE GATE DETECTION v42
# Orbit / Attractor Locking
# ============================================================
#
# PURPOSE:
# --------
# Measure whether the controlled trajectory remains locked to
# stable structural regions over time.
#
# Builds on:
# - v38: structure-aware control
# - v39: stable attractor memory
# - v41: ridge-aligned motion
#
# CORE QUESTION:
# --------------
# Does the system remain attached to stable attractor basins?
#
# OUTPUTS:
# --------
# v42_orbit_attractor_locking.png
# v42_locking_score_time.png
# v42_locking_scores.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control
from ieee_gate_detection_v39_attractor_memory import (
    stability_score,
    detect_stable_attractors,
    attractor_memory_field
)
from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control
from ieee_gate_detection_v38_control_layer import gradient_field, make_interpolator


# ------------------------------------------------------------
# Field lookup
# ------------------------------------------------------------

def lookup_field(field_interp, states):
    values = []
    for s in states:
        values.append(field_interp(np.array([s]))[0])
    return np.array(values)


# ------------------------------------------------------------
# Attractor locking score
# ------------------------------------------------------------

def compute_locking_score(states, A_interp, D_interp, P_interp):
    """
    Locking score:

    L(s) = A(s) * (1 - P(s)) * 1/(1 + D(s))

    High L:
    - near attractor memory
    - low instability probability
    - close to ridge structure
    """

    A_vals = lookup_field(A_interp, states)
    D_vals = lookup_field(D_interp, states)
    P_vals = lookup_field(P_interp, states)

    L = A_vals * (1.0 - P_vals) * (1.0 / (1.0 + D_vals))
    L = L / (np.max(L) + 1e-9)

    return L, A_vals, D_vals, P_vals


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

    # --- v38 base
    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([result["r"], result["theta"]])
    raw_controls = result["controls"]

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    # --- v39 attractor memory
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

    # --- v41 ridge alignment
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

    # --- interpolators
    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    # --- locking score
    L, A_vals, D_vals, P_vals = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --------------------------------------------------------
    # Plot 1: trajectory colored by locking score
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))
    sc = plt.scatter(
        aligned[:, 1],
        aligned[:, 0],
        c=L,
        s=4,
        alpha=0.8
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v42 — Orbit / Attractor Locking")
    plt.colorbar(sc, label="locking score L")
    plt.tight_layout()

    out_path_1 = os.path.join(
        OUT_DIR,
        "v42_orbit_attractor_locking.png"
    )

    plt.savefig(out_path_1, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot 2: locking score over time
    # --------------------------------------------------------

    plt.figure(figsize=(10, 4))
    plt.plot(t, L, linewidth=1.0)
    plt.xlabel("time")
    plt.ylabel("locking score L")
    plt.title("NEXAH v42 — Locking Score Over Time")
    plt.tight_layout()

    out_path_2 = os.path.join(
        OUT_DIR,
        "v42_locking_score_time.png"
    )

    plt.savefig(out_path_2, dpi=200)
    plt.close()

    # --- save arrays
    np.save(os.path.join(OUT_DIR, "v42_locking_scores.npy"), L)
    np.save(os.path.join(OUT_DIR, "v42_attractor_values.npy"), A_vals)
    np.save(os.path.join(OUT_DIR, "v42_ridge_distance_values.npy"), D_vals)
    np.save(os.path.join(OUT_DIR, "v42_iota_probability_values.npy"), P_vals)

    print("NEXAH v42 complete")
    print(f"Attractors detected: {len(attractors)}")
    print(f"Mean locking score: {np.mean(L):.4f}")
    print(f"Max locking score:  {np.max(L):.4f}")
    print(f"Saved: {out_path_1}")
    print(f"Saved: {out_path_2}")
