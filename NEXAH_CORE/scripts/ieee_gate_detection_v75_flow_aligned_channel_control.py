# ============================================================
# NEXAH v75 — Flow-Aligned Channel Control (FINAL CLEAN)
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt


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
# Build field (same as earlier versions)
# ------------------------------------------------------------

def build_field():

    t = np.linspace(0, 80, 3000)

    x = np.sin(t) + 0.3 * np.sin(3*t)
    y = np.cos(t) + 0.2 * np.cos(5*t)

    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    return np.stack([r, theta], axis=1)


# ------------------------------------------------------------
# Estimate local flow
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
# Flow control
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

        # nearest trajectory point
        dists = np.linalg.norm(traj - state, axis=1)
        idx = np.argmin(dists)

        flow_dir = estimate_flow_direction(traj, idx)
        target_dir = unit_vector_to_target(state, target)

        # blend
        alpha = 0.85
        beta = 0.15

        u = alpha * flow_dir + beta * target_dir
        u = unit_vector(u)

        # step
        step_size = 0.02
        state = state + step_size * u
        state[1] = wrap_theta(state[1])

        controlled.append(state.copy())

        # gate reached?
        if state_distance(state, target) < 0.1:
            gate_index += 1

    return np.array(controlled)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    traj = build_field()

    gates = {
        (0, 3): {"r": 1.1488, "theta": -0.1580},
        (3, 1): {"r": 1.4856, "theta": -1.5620},
    }

    path = [0, 3, 1]

    controlled = run_flow_control(traj, gates, path)

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(traj[:, 1], traj[:, 0], s=1, alpha=0.3, label="field")

    ax.plot(
        controlled[:, 1],
        controlled[:, 0],
        color="red",
        linewidth=2,
        label="flow-aligned control"
    )

    for (a, b), g in gates.items():
        ax.scatter(g["theta"], g["r"], c="black", s=80)

    ax.set_xlabel("theta")
    ax.set_ylabel("r")
    ax.set_title("NEXAH v75 — Flow-Aligned Channel Control")
    ax.legend()

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
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
