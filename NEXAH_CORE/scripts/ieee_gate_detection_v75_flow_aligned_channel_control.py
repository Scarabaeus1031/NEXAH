# ============================================================
# NEXAH — IEEE GATE DETECTION v75
# Flow-Aligned Channel Control
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
# Estimate local flow direction from trajectory
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

    for _ in range(max_steps):

        if gate_index >= len(path) - 1:
            break

        current_gate = gates[(path[gate_index], path[gate_index + 1])]
        target = np.array([current_gate["r"], current_gate["theta"]])

        # 🔧 correct wrapped distance
        dr = traj[:, 0] - state[0]
        dtheta = np.array([wrap_theta(th - state[1]) for th in traj[:, 1]])
        dists = np.sqrt(dr**2 + dtheta**2)
        idx = np.argmin(dists)

        # flow + target
        flow_dir = estimate_flow_direction(traj, idx)
        target_dir = unit_vector_to_target(state, target)

        alpha = 0.85
        beta = 0.15

        u = alpha * flow_dir + beta * target_dir
        u = unit_vector(u)

        step_size = 0.02
        state = state + step_size * u
        state[1] = wrap_theta(state[1])

        controlled.append(state.copy())

        # gate reached
        if state_distance(state, target) < 0.1:
            gate_index += 1

    return np.array(controlled)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    # --------------------------------------------------------
    # Build trajectory via v38
    # --------------------------------------------------------

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    traj = np.column_stack([result["r"], result["theta"]])

    # --------------------------------------------------------
    # Gates (v68)
    # --------------------------------------------------------

    gates = {
        (0, 3): {"r": 1.1488, "theta": -0.1580},
        (3, 1): {"r": 1.4856, "theta": -1.5620},
    }

    path = [0, 3, 1]

    controlled = run_flow_control(traj, gates, path)

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 6))

    plt.scatter(traj[:, 1], traj[:, 0], s=1, alpha=0.25, label="field")

    plt.plot(
        controlled[:, 1],
        controlled[:, 0],
        color="red",
        linewidth=2,
        label="flow-aligned control"
    )

    for (a, b), g in gates.items():
        plt.scatter(g["theta"], g["r"], c="black", s=80)
        plt.text(g["theta"], g["r"], f"G{a}->{b}", fontsize=8)

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v75 — Flow-Aligned Channel Control")
    plt.legend()

   # --------------------------------------------------------
# Save instead of show (robust)
# --------------------------------------------------------

CORE_DIR = os.path.dirname(CURRENT_DIR)
OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
os.makedirs(OUT_DIR, exist_ok=True)

out_path = os.path.join(
    OUT_DIR,
    "v75_flow_aligned_channel_control.png"
)

# IMPORTANT: grab current figure explicitly
fig = plt.gcf()

fig.tight_layout()
fig.savefig(out_path, dpi=200, bbox_inches="tight")

print("NEXAH v75 complete")
print(f"Saved: {out_path}")

# Optional: keep or close depending on your workflow
plt.close(fig)
