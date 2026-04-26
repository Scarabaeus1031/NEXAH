# ============================================================
# NEXAH — IEEE GATE DETECTION v64
# Learned Flow Field (First Real Dynamics)
# ============================================================
#
# FILE:
# ieee_gate_detection_v64_learned_flow_field.py
#
# PURPOSE:
# --------
# Introduce REAL system dynamics by learning a local vector field
# from trajectory data.
#
# Instead of:
#   manually shifting points
#
# We now:
#   learn local flow f(s)
#   and simulate:
#       s(t+1) = s(t) + f(s)
#
# RESULT:
# -------
# First true propagation of control through system dynamics.
#
# OUTPUTS:
# --------
# v64_learned_flow_trajectory.png
# v64_learned_flow_summary.txt
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
# Build base trajectory
# ------------------------------------------------------------

def build_pipeline():

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
# Learn local flow field via k-NN averaging
# ------------------------------------------------------------

def learn_flow_field(states, k=20):

    N = len(states)

    # precompute velocities (finite differences)
    dr = np.gradient(states[:, 0])
    dtheta = np.gradient(states[:, 1])

    velocities = np.column_stack([dr, dtheta])

    def flow(s):

        # distance to all points
        dists = np.linalg.norm(states - s, axis=1)

        # nearest neighbors
        idx = np.argsort(dists)[:k]

        # average velocity
        v = np.mean(velocities[idx], axis=0)

        return v

    return flow


# ------------------------------------------------------------
# Wrap angle
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


# ------------------------------------------------------------
# Simulate dynamics with optional control impulse
# ------------------------------------------------------------

def simulate_dynamics(flow, s0, steps=200, control=None):

    traj = [s0.copy()]

    s = s0.copy()

    for t in range(steps):

        v = flow(s)

        # optional control injection (single time step)
        if control is not None and t == control["t"]:
            v = v + control["u"]

        s = s + 0.05 * v
        s[1] = wrap_theta(s[1])

        traj.append(s.copy())

    return np.array(traj)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states = build_pipeline()

    # learn flow
    flow = learn_flow_field(states, k=25)

    # pick initial point (same region as control core)
    start_index = 67
    s0 = states[start_index].copy()

    # define control impulse (small push downward in theta)
    control = {
        "t": 10,
        "u": np.array([0.0, -0.5])
    }

    # simulate
    traj_baseline = simulate_dynamics(flow, s0, steps=250)
    traj_control  = simulate_dynamics(flow, s0, steps=250, control=control)

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    # background field
    plt.scatter(states[:, 1], states[:, 0], s=2, alpha=0.1, label="data field")

    # trajectories
    plt.plot(traj_baseline[:, 1], traj_baseline[:, 0], linewidth=2, label="baseline traj")
    plt.plot(traj_control[:, 1], traj_control[:, 0], linewidth=2, label="controlled traj")

    # start point
    plt.scatter(s0[1], s0[0], color="red", s=60, label="start")

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v64 — Learned Flow Field Dynamics")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v64_learned_flow_trajectory.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    final_dev = np.linalg.norm(traj_control[-1] - traj_baseline[-1])

    summary_path = os.path.join(
        OUT_DIR,
        "v64_learned_flow_summary.txt"
    )

    with open(summary_path, "w") as f:
        f.write("NEXAH v64 — Learned Flow Field\n")
        f.write("================================\n\n")
        f.write(f"Start index: {start_index}\n")
        f.write(f"Final deviation: {final_dev:.6f}\n")
        f.write("Control applied at step t=10\n")

    print("NEXAH v64 complete")
    print(f"Final deviation: {final_dev:.6f}")
    print(f"Saved: {out_path}")
    print(f"Saved: {summary_path}")
