# ============================================================
# NEXAH — IEEE GATE DETECTION v43
# Basin Transitions / Attractor Switching Dynamics
# ============================================================
#
# PURPOSE:
# --------
# Detect and analyze transitions between stable attractor regions.
#
# Builds on:
# - v42: locking score L(s)
#
# CORE IDEA:
# ----------
# Identify:
# - when the system enters a stable basin
# - how long it stays
# - when it leaves
# - which basin it goes to next
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v42_orbit_attractor_locking import compute_locking_score
from ieee_gate_detection_v41_ridge_aligned_control import ridge_aligned_control
from ieee_gate_detection_v38_control_layer import run_v38_control, gradient_field, make_interpolator
from ieee_gate_detection_v39_attractor_memory import stability_score, detect_stable_attractors, attractor_memory_field


# ------------------------------------------------------------
# Basin detection
# ------------------------------------------------------------

def detect_basins(L, threshold=0.5):
    """
    Binary basin membership from locking score.
    """
    return L > threshold


def extract_segments(mask):
    """
    Extract contiguous True segments.
    """
    segments = []
    start = None

    for i, val in enumerate(mask):
        if val and start is None:
            start = i
        elif not val and start is not None:
            segments.append((start, i))
            start = None

    if start is not None:
        segments.append((start, len(mask)))

    return segments


# ------------------------------------------------------------
# Transition extraction
# ------------------------------------------------------------

def compute_transitions(segments):
    """
    Compute transitions between basin visits.
    """
    transitions = []

    for i in range(len(segments) - 1):
        exit_time = segments[i][1]
        entry_time = segments[i + 1][0]

        gap = entry_time - exit_time

        transitions.append({
            "from": i,
            "to": i + 1,
            "exit_t": exit_time,
            "entry_t": entry_time,
            "gap": gap
        })

    return transitions


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

    # --- interpolators
    A_interp = make_interpolator(A, r_grid, theta_grid)
    D_interp = make_interpolator(D, r_grid, theta_grid)
    P_interp = make_interpolator(P, r_grid, theta_grid)

    # --- v42
    L, *_ = compute_locking_score(
        aligned,
        A_interp,
        D_interp,
        P_interp
    )

    # --------------------------------------------------------
    # v43 analysis
    # --------------------------------------------------------

    basin_mask = detect_basins(L, threshold=0.5)
    segments = extract_segments(basin_mask)
    transitions = compute_transitions(segments)

    durations = [end - start for start, end in segments]
    gaps = [tr["gap"] for tr in transitions]

    # --------------------------------------------------------
    # Plot 1: basin segments over time
    # --------------------------------------------------------

    plt.figure(figsize=(10, 4))
    plt.plot(t, basin_mask.astype(int))
    plt.title("NEXAH v43 — Basin Membership")
    plt.xlabel("time")
    plt.ylabel("in basin (0/1)")
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "v43_basin_membership.png"), dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot 2: duration histogram
    # --------------------------------------------------------

    plt.figure(figsize=(6, 4))
    plt.hist(durations, bins=20)
    plt.title("NEXAH v43 — Basin Duration Distribution")
    plt.xlabel("duration (timesteps)")
    plt.ylabel("count")
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "v43_basin_duration_hist.png"), dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot 3: gap histogram
    # --------------------------------------------------------

    plt.figure(figsize=(6, 4))
    plt.hist(gaps, bins=20)
    plt.title("NEXAH v43 — Transition Gap Distribution")
    plt.xlabel("gap (timesteps)")
    plt.ylabel("count")
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "v43_transition_gaps.png"), dpi=200)
    plt.close()

    # --- save data
    np.save(os.path.join(OUT_DIR, "v43_durations.npy"), durations)
    np.save(os.path.join(OUT_DIR, "v43_gaps.npy"), gaps)

    print("NEXAH v43 complete")
    print(f"Basin segments: {len(segments)}")
    print(f"Transitions: {len(transitions)}")
    print(f"Mean duration: {np.mean(durations) if durations else 0:.2f}")
    print(f"Mean gap: {np.mean(gaps) if gaps else 0:.2f}")  
