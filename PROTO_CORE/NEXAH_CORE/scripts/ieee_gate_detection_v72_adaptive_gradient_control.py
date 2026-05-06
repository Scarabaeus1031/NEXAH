# ============================================================
# NEXAH — IEEE GATE DETECTION v72
# Adaptive Gradient Gate Control
# ============================================================
#
# FILE:
# ieee_gate_detection_v72_adaptive_gradient_control.py
#
# PURPOSE:
# --------
# Improve v71 by making control:
#
# 1. Gradient-aware  → reacts to field resistance
# 2. Barrier-aware   → only inject energy when needed
# 3. Self-damping    → shuts off after gate crossing
#
# CORE IDEA:
# ----------
# Minimal-energy transition across basins using:
#
# boost = f( barrier_height , gradient_magnitude )
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Utils
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


def unit_vector_to_target(s, target):
    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])

    u = np.array([dr, dtheta])
    n = np.linalg.norm(u)

    return u / n if n > 1e-9 else np.zeros(2)


# ------------------------------------------------------------
# Build field
# ------------------------------------------------------------

def build_field():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    states = np.column_stack([result["r"], result["theta"]])

    kde = gaussian_kde(states.T)
    rho = kde(states.T)

    V = -np.log(rho + 1e-12)

    # gradient (approx)
    dV_r = np.gradient(V, states[:, 0])
    dV_t = np.gradient(V, states[:, 1])

    grad_norm = np.sqrt(dV_r**2 + dV_t**2)

    return states, V, grad_norm


# ------------------------------------------------------------
# Gate path (from v69)
# ------------------------------------------------------------

def get_gate_path():

    # Hardcoded from v69 (can later auto-load)
    path = [0, 3, 1]

    gates = [
        (1.1488, -0.1580),   # B0 -> B3
        (1.4856, -1.5620)    # B3 -> B1
    ]

    return path, gates


# ------------------------------------------------------------
# Adaptive control
# ------------------------------------------------------------

def simulate(states, V, grad_norm, gates):

    traj = states.copy()

    index = 67  # start control index

    pos = traj[index].copy()

    trajectory = [pos.copy()]
    boost_log = []

    gate_id = 0
    reached = 0

    for step in range(300):

        if gate_id >= len(gates):
            boost = 0.0
            u = np.zeros(2)
        else:
            gate = np.array(gates[gate_id])

            # distance to gate
            dist = np.linalg.norm(pos - gate)

            # barrier term
            V_current = V[index]
            V_gate = V[np.argmin(np.linalg.norm(states - gate, axis=1))]
            dV = max(0.0, V_gate - V_current)

            # gradient term
            g = grad_norm[index]

            # adaptive boost
            boost = min(1.0, 0.6 * dV + 0.4 * g)

            # direction
            u = unit_vector_to_target(pos, gate)

            # gate reached?
            if dist < 0.1:
                gate_id += 1
                reached += 1

                # strong damping after crossing
                boost *= 0.2

        # apply control
        pos = pos + boost * 0.05 * u
        pos[1] = wrap_theta(pos[1])

        trajectory.append(pos.copy())
        boost_log.append(boost)

    return np.array(trajectory), boost_log, reached


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states, V, grad_norm = build_field()

    path, gates = get_gate_path()

    traj, boost, reached = simulate(states, V, grad_norm, gates)

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(states[:, 1], states[:, 0], s=2, alpha=0.1, label="field")

    plt.plot(traj[:, 1], traj[:, 0], color="orange", label="adaptive control")

    for g in gates:
        plt.scatter(g[1], g[0], color="red", s=80)

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v72 — Adaptive Gradient Gate Control")

    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(OUT_DIR, "v72_adaptive_control.png")
    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot boost
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))
    plt.plot(boost)
    plt.title("Adaptive Boost")
    plt.xlabel("step")
    plt.ylabel("boost")
    plt.tight_layout()

    out_path2 = os.path.join(OUT_DIR, "v72_boost.png")
    plt.savefig(out_path2, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(OUT_DIR, "v72_summary.txt")

    with open(summary_path, "w") as f:
        f.write("NEXAH v72 — Adaptive Gradient Control\n")
        f.write("====================================\n\n")
        f.write(f"Path: {path}\n")
        f.write(f"Gates reached: {reached}/{len(gates)}\n")
        f.write(f"Max boost: {np.max(boost):.4f}\n")
        f.write(f"Mean boost: {np.mean(boost):.4f}\n")

    print("NEXAH v72 complete")
    print(f"Gates reached: {reached}/{len(gates)}")
