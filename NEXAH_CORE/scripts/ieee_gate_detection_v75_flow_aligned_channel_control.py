# ============================================================
# NEXAH — IEEE GATE DETECTION v75
# Flow-Aligned Channel Control (CLEAN VERSION)
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


def unit_vector(v):
    n = np.linalg.norm(v)
    if n < 1e-9:
        return np.zeros_like(v)
    return v / n


def state_distance(a, b):
    return np.linalg.norm([
        a[0] - b[0],
        wrap_theta(a[1] - b[1])
    ])


def unit_vector_to_target(s, target):
    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])
    return unit_vector(np.array([dr, dtheta]))


# ------------------------------------------------------------
# Estimate local flow direction
# ------------------------------------------------------------

def estimate_flow_direction(traj, idx):

    if idx <= 1:
        return unit_vector(traj[1] - traj[0])

    if idx >= len(traj) - 1:
        return unit_vector(traj[-1] - traj[-2])

    forward = traj[idx + 1] - traj[idx]
    backward = traj[idx] - traj[idx - 1]

    flow = 0.5 * (forward + backward)
    flow[1] = wrap_theta(flow[1])

    return unit_vector(flow)


# ------------------------------------------------------------
# Flow-aligned control
# ------------------------------------------------------------

def run_flow_control(traj, gates, path, max_steps=300):

    state = traj[0].copy()
    controlled = [state.copy()]

    gate_index = 0

    for t in range(max_steps):

        if gate_index >= len(path) - 1:
            break

        current_gate = gates[(path[gate_index], path[gate_index + 1])]
        target = np.array([current_gate["r"], current_gate["theta"]])

        # nearest trajectory index
        dists = np.linalg.norm(traj - state, axis=1)
        idx = np.argmin(dists)

        # FLOW direction
        flow_dir = estimate_flow_direction(traj, idx)

        # TARGET direction (weak)
        target_dir = unit_vector_to_target(state, target)

        # BLEND
        alpha = 0.85
        beta = 0.15

        u = alpha * flow_dir + beta * target_dir
        u = unit_vector(u)

        # step
        step_size = 0.02
        state = state + step_size * u
        state[1] = wrap_theta(state[1])

        controlled.append(state.copy())

        # check gate reached
        if state_distance(state, target) < 0.1:
            gate_index += 1

    return np.array(controlled)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    # --------------------------------------------------------
    # Get trajectory (FIXED)
    # --------------------------------------------------------
    result = run_v38_control()

    # handle both return styles
    if isinstance(result, dict):
        traj = result["trajectory"]
    else:
        traj = result

    traj = np.array(traj)

    # --------------------------------------------------------
    # Gates (from v68)
    # --------------------------------------------------------

    gates = {
        (0, 3): {"r": 1.1488, "theta": -0.1580},
        (3, 1): {"r": 1.4856, "theta": -1.5620},
    }

    path = [0, 3, 1]

    controlled = run_flow_control(traj, gates, path)

    # --------------------------------------------------------
    # Plot + Save (stable)
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 6))

    # field
    ax.scatter(
        traj[:, 1], traj[:, 0],
        s=1, alpha=0.3, label="field"
    )

    # controlled path
    ax.plot(
        controlled[:, 1],
        controlled[:, 0],
        color="red",
        linewidth=2,
        label="flow-aligned control"
    )

    # gates
    for (a, b), g in gates.items():
        ax.scatter(
            g["theta"], g["r"],
            c="black", s=80
        )

    ax.set_xlabel("theta")
    ax.set_ylabel("r")
    ax.set_title("NEXAH v75 — Flow-Aligned Channel Control")
    ax.legend()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    out_path = os.path.join(
        OUT_DIR,
        "v75_flow_aligned_channel_control.png"
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)

    print("NEXAH v75 complete")
    print(f"Saved: {out_path}")

    plt.close(fig)


if __name__ == "__main__":
    main()
