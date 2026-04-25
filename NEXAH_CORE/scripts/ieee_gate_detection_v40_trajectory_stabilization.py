# ============================================================
# NEXAH — IEEE GATE DETECTION v40
# Trajectory Stabilization / Path Coherence
# ============================================================
#
# PURPOSE:
# --------
# Extend control from local state steering (v38–v39)
# to trajectory-level stabilization.
#
# Core idea:
# The system should not only move to stable regions,
# but follow smooth, coherent paths aligned with structure.
#
# WHAT THIS SCRIPT DOES:
# ---------------------
# - Uses v38 control (structure-aware)
# - Adds trajectory smoothing (velocity + curvature damping)
# - Reduces oscillatory / noisy control behavior
# - Produces stable, physically plausible trajectories
#
# CORE ADDITION:
# --------------
# Control is no longer:
#     s(t+1) = s(t) + u(t)
#
# But:
#     s(t+1) = s(t) + u(t)
#                          - velocity damping
#                          - curvature penalty
#
# RESULT:
# -------
# Smooth trajectories that:
# - stay on structure
# - avoid instability
# - minimize sharp turns
#
# ============================================================

import numpy as np
import os
import matplotlib.pyplot as plt

# --- import v38 control
from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Trajectory Stabilization
# ------------------------------------------------------------

def stabilize_trajectory(states, controls,
                        lambda_vel=0.3,
                        lambda_curv=0.2):
    """
    Apply trajectory-level smoothing.

    Parameters:
    -----------
    states   : (T, 2)
    controls : (T, 2)

    Returns:
    --------
    stabilized_states : (T, 2)
    """

    stabilized = [states[0]]

    prev_velocity = np.zeros(2)

    for t in range(1, len(states)):

        current = stabilized[-1]
        raw_u = controls[t]

        # --- velocity damping (smooth movement)
        velocity = raw_u
        velocity_smooth = (1 - lambda_vel) * velocity + lambda_vel * prev_velocity

        # --- curvature penalty (avoid sharp turns)
        curvature = velocity - prev_velocity
        curvature_penalty = lambda_curv * curvature

        u_stable = velocity_smooth - curvature_penalty

        next_state = current + u_stable

        stabilized.append(next_state)

        prev_velocity = velocity_smooth

    return np.array(stabilized)


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":

    # --- paths
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
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

    # --- run v38 control
    result = run_v38_control(x, dt=t[1] - t[0])

    states = np.column_stack([result["r"], result["theta"]])
    controls = result["controls"]

    # --- apply v40 stabilization
    stabilized = stabilize_trajectory(states, controls)

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        result["theta"],
        result["r"],
        s=2,
        alpha=0.25,
        label="original"
    )

    plt.scatter(
        result["controlled"][:, 1],
        result["controlled"][:, 0],
        s=2,
        alpha=0.25,
        label="v38 controlled"
    )

    plt.scatter(
        stabilized[:, 1],
        stabilized[:, 0],
        s=2,
        alpha=0.35,
        label="v40 stabilized"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.legend()
    plt.title("NEXAH v40 — Trajectory Stabilization")

    plt.tight_layout()

    out_path = os.path.join(OUT_DIR, "v40_trajectory_stabilization.png")
    plt.savefig(out_path, dpi=200)

    plt.show()

    # --- save arrays
    np.save(os.path.join(OUT_DIR, "v40_stabilized.npy"), stabilized)

    print("NEXAH v40 complete")
    print(f"Saved: {out_path}")
