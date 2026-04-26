# ============================================================
# NEXAH — IEEE GATE DETECTION v74
# Smooth Gate Transition Control
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Utils
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


def state_distance(a, b):
    return np.linalg.norm([
        a[0] - b[0],
        wrap_theta(a[1] - b[1])
    ])


def unit_vector_to_target(s, target):
    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])

    u = np.array([dr, dtheta])
    n = np.linalg.norm(u)

    return u / n if n > 1e-9 else np.zeros(2)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# ------------------------------------------------------------
# Field
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

    return states


# ------------------------------------------------------------
# Structure (v68/v69)
# ------------------------------------------------------------

def load_structure():

    basins = {
        0: np.array([0.8715, 0.6494]),
        1: np.array([0.9310, -2.3343]),
        3: np.array([1.6242, -1.3514]),
    }

    gates = [
        np.array([1.1488, -0.1580]),  # 0->3
        np.array([1.4856, -1.5620]),  # 3->1
    ]

    return basins, gates


# ------------------------------------------------------------
# Smooth control
# ------------------------------------------------------------

def simulate_smooth_control(states, s0, gates, target):

    s = s0.copy()
    traj = [s.copy()]
    alpha_log = []

    for step in range(300):

        g1 = gates[0]
        g2 = gates[1]

        d1 = state_distance(s, g1)
        d2 = state_distance(s, g2)

        # Smooth blending
        alpha = sigmoid((d1 - d2) * 4.0)

        blended_target = (1 - alpha) * g1 + alpha * g2

        u = unit_vector_to_target(s, blended_target)

        # moderate control strength
        boost = 0.25

        s = s + 0.06 * boost * u
        s[1] = wrap_theta(s[1])

        traj.append(s.copy())
        alpha_log.append(alpha)

        if state_distance(s, target) < 0.25:
            break

    return np.array(traj), np.array(alpha_log)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states = build_field()

    basins, gates = load_structure()

    s0 = basins[0]
    target = basins[1]

    traj, alpha = simulate_smooth_control(states, s0, gates, target)

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(9, 8))

    plt.scatter(
        states[:, 1],
        states[:, 0],
        s=2,
        alpha=0.08,
        label="state field"
    )

    plt.plot(
        traj[:, 1],
        traj[:, 0],
        linewidth=2.5,
        label="smooth control"
    )

    for b, pos in basins.items():
        plt.scatter(pos[1], pos[0], s=80)
        plt.text(pos[1], pos[0], f"B{b}")

    for i, g in enumerate(gates):
        plt.scatter(g[1], g[0], color="red", marker="x", s=120)
        plt.text(g[1], g[0], f"G{i}")

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v74 — Smooth Gate Transition Control")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "v74_smooth_control.png"), dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Alpha plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))
    plt.plot(alpha)
    plt.title("Gate Blending (alpha)")
    plt.xlabel("step")
    plt.ylabel("alpha")
    plt.tight_layout()

    plt.savefig(os.path.join(OUT_DIR, "v74_alpha.png"), dpi=200)
    plt.close()

    print("NEXAH v74 complete")
