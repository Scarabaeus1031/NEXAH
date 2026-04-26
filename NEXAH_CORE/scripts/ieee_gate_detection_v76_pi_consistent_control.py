# ============================================================
# NEXAH — IEEE GATE DETECTION v76
# π-Consistent Control
# ============================================================
#
# FILE:
# ieee_gate_detection_v76_pi_consistent_control.py
#
# PURPOSE:
# --------
# Upgrade v75 flow-aligned control by enforcing smooth turning.
#
# v75:
#   follow local flow + weak gate pull
#
# v76:
#   follow local flow + weak gate pull
#   BUT constrain directional change continuously.
#
# CORE IDEA:
# ----------
# π-consistent motion means:
#
#   no hard angular snapping
#   no staircase movement
#   no 0°/90° jumps
#
# Instead:
#
#   direction changes smoothly over time.
#
# OUTPUT:
# -------
# v76_pi_consistent_control.png
# v76_pi_turning_profile.png
# v76_pi_control_summary.txt
#
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
    if n < 1e-12:
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


def angle_of(v):
    return np.arctan2(v[0], v[1])


def smooth_direction(prev_u, desired_u, smoothness=0.92):
    """
    π-consistent direction update:
    prevents hard direction jumps by mixing previous direction
    with the desired direction.
    """

    if np.linalg.norm(prev_u) < 1e-12:
        return unit_vector(desired_u)

    u = smoothness * prev_u + (1.0 - smoothness) * desired_u
    return unit_vector(u)


# ------------------------------------------------------------
# Build trajectory field using v38-compatible call
# ------------------------------------------------------------

def build_field():

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    traj = np.column_stack([result["r"], result["theta"]])

    return traj


# ------------------------------------------------------------
# Estimate local flow direction
# ------------------------------------------------------------

def estimate_flow_direction(traj, state):

    dr = traj[:, 0] - state[0]
    dtheta = np.array([wrap_theta(th - state[1]) for th in traj[:, 1]])
    dists = np.sqrt(dr**2 + dtheta**2)

    idx = np.argmin(dists)

    if idx <= 1:
        flow = traj[1] - traj[0]
    elif idx >= len(traj) - 2:
        flow = traj[-1] - traj[-2]
    else:
        forward = traj[idx + 1] - traj[idx]
        backward = traj[idx] - traj[idx - 1]
        flow = 0.5 * (forward + backward)

    flow[1] = wrap_theta(flow[1])

    return unit_vector(flow)


# ------------------------------------------------------------
# Structure
# ------------------------------------------------------------

def load_structure():

    basins = {
        0: np.array([0.8715, 0.6494]),
        1: np.array([0.9310, -2.3343]),
        3: np.array([1.6242, -1.3514]),
    }

    gates = {
        (0, 3): np.array([1.1488, -0.1580]),
        (3, 1): np.array([1.4856, -1.5620]),
    }

    path = [0, 3, 1]

    return basins, gates, path


# ------------------------------------------------------------
# π-consistent control
# ------------------------------------------------------------

def run_pi_consistent_control(
    field,
    basins,
    gates,
    path,
    max_steps=520,
    step_size=0.025,
    flow_weight=0.68,
    gate_weight=0.32,
    smoothness=0.94,
    gate_radius=0.16,
    target_radius=0.22
):

    state = basins[path[0]].copy()
    target_basin = basins[path[-1]]

    controlled = [state.copy()]
    direction_log = []
    turn_log = []
    gate_log = []

    gate_index = 0
    prev_u = np.zeros(2)
    prev_angle = None

    for _ in range(max_steps):

        if gate_index < len(path) - 1:
            edge = (path[gate_index], path[gate_index + 1])
            target = gates[edge]
        else:
            target = target_basin

        flow_dir = estimate_flow_direction(field, state)
        target_dir = unit_vector_to_target(state, target)

        desired_u = unit_vector(
            flow_weight * flow_dir
            + gate_weight * target_dir
        )

        # π-control: smooth continuous turning
        u = smooth_direction(prev_u, desired_u, smoothness=smoothness)

        angle = angle_of(u)

        if prev_angle is None:
            turn = 0.0
        else:
            turn = wrap_theta(angle - prev_angle)

        prev_angle = angle
        prev_u = u.copy()

        state = state + step_size * u
        state[1] = wrap_theta(state[1])

        controlled.append(state.copy())
        direction_log.append(u.copy())
        turn_log.append(turn)
        gate_log.append(gate_index)

        # gate reached
        if gate_index < len(path) - 1:
            if state_distance(state, target) < gate_radius:
                gate_index += 1
        else:
            if state_distance(state, target_basin) < target_radius:
                break

    return {
        "controlled": np.array(controlled),
        "directions": np.array(direction_log),
        "turns": np.array(turn_log),
        "gate_log": np.array(gate_log),
        "reached_gates": gate_index,
        "final_distance": state_distance(controlled[-1], target_basin),
    }


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    field = build_field()
    basins, gates, path = load_structure()

    result = run_pi_consistent_control(
        field,
        basins,
        gates,
        path
    )

    controlled = result["controlled"]

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.scatter(
        field[:, 1],
        field[:, 0],
        s=2,
        alpha=0.12,
        label="field"
    )

    ax.plot(
        controlled[:, 1],
        controlled[:, 0],
        linewidth=2.4,
        color="red",
        label="π-consistent control"
    )

    for bid, b in basins.items():
        ax.scatter(
            b[1],
            b[0],
            s=90,
            edgecolor="black"
        )
        ax.text(b[1], b[0], f"B{bid}", fontsize=9)

    for edge, g in gates.items():
        ax.scatter(
            g[1],
            g[0],
            s=120,
            marker="x",
            color="black"
        )
        ax.text(g[1], g[0], f"G{edge[0]}->{edge[1]}", fontsize=8)

    ax.set_xlabel("theta")
    ax.set_ylabel("r")
    ax.set_title(
        "NEXAH v76 — π-Consistent Control\n"
        f"reached={result['reached_gates']}/{len(path)-1}, "
        f"final_dist={result['final_distance']:.4f}"
    )
    ax.legend()

    out_path = os.path.join(
        OUT_DIR,
        "v76_pi_consistent_control.png"
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

    # --------------------------------------------------------
    # Turning profile
    # --------------------------------------------------------

    fig2, ax2 = plt.subplots(figsize=(9, 4))

    ax2.plot(result["turns"], linewidth=1.5)
    ax2.axhline(0.0, linestyle="--", linewidth=1)

    ax2.set_xlabel("step")
    ax2.set_ylabel("Δ direction angle")
    ax2.set_title("NEXAH v76 — Smooth Turning / π-Consistency")

    turn_path = os.path.join(
        OUT_DIR,
        "v76_pi_turning_profile.png"
    )

    fig2.tight_layout()
    fig2.savefig(turn_path, dpi=200)
    plt.close(fig2)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v76_pi_control_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("NEXAH v76 — π-Consistent Control\n")
        f.write("================================\n\n")

        f.write(f"Path: {path}\n")
        f.write(f"Reached gates: {result['reached_gates']}/{len(path)-1}\n")
        f.write(f"Final distance to target: {result['final_distance']:.6f}\n\n")

        f.write("π-consistency metrics:\n")
        f.write(f"  max |turn|:  {np.max(np.abs(result['turns'])):.6f}\n")
        f.write(f"  mean |turn|: {np.mean(np.abs(result['turns'])):.6f}\n")
        f.write(f"  total turn:  {np.sum(np.abs(result['turns'])):.6f}\n\n")

        f.write("Interpretation:\n")
        f.write("  Lower turn spikes indicate smoother directional evolution.\n")
        f.write("  This approximates continuous rotation instead of staircase-like motion.\n")

    print("NEXAH v76 complete")
    print(f"Reached gates: {result['reached_gates']}/{len(path)-1}")
    print(f"Final distance: {result['final_distance']:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {turn_path}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
