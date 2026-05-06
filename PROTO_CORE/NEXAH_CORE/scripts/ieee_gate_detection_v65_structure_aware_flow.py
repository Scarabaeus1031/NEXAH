# ============================================================
# NEXAH — IEEE GATE DETECTION v65 (FIXED)
# Structure-Aware Flow (No Clustering Dependency)
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import run_v38_control


# ------------------------------------------------------------
# Wrap theta
# ------------------------------------------------------------

def wrap_theta(theta):
    return (theta + np.pi) % (2 * np.pi) - np.pi


# ------------------------------------------------------------
# Build base data
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
# Learned local flow (kNN)
# ------------------------------------------------------------

def learn_local_flow(states, k=25):

    velocities = np.gradient(states, axis=0)

    def flow(s):

        dr = states[:, 0] - s[0]
        dtheta = np.array([wrap_theta(p[1] - s[1]) for p in states])

        dists = np.sqrt(dr**2 + dtheta**2)
        idx = np.argsort(dists)[:k]

        return np.mean(velocities[idx], axis=0)

    return flow


# ------------------------------------------------------------
# Simple structural stabilization (IMPORTANT)
# ------------------------------------------------------------

def radial_stabilization(s, center):

    dr = center[0] - s[0]
    dtheta = wrap_theta(center[1] - s[1])

    v = np.array([dr, dtheta])
    norm = np.linalg.norm(v)

    if norm > 1e-9:
        v = v / norm

    return v


# ------------------------------------------------------------
# Target direction
# ------------------------------------------------------------

def target_vector(s, target):

    dr = target[0] - s[0]
    dtheta = wrap_theta(target[1] - s[1])

    v = np.array([dr, dtheta])
    norm = np.linalg.norm(v)

    if norm > 1e-9:
        v = v / norm

    return v


# ------------------------------------------------------------
# Structure-aware flow
# ------------------------------------------------------------

def structure_flow(
    s,
    local_flow,
    center,
    target=None,
    alpha=1.0,
    beta=0.08,
    gamma=0.04
):

    v = local_flow(s)

    # weak stabilization (prevents drift)
    v += beta * radial_stabilization(s, center)

    # optional directional bias
    if target is not None:
        v += gamma * target_vector(s, target)

    return v


# ------------------------------------------------------------
# Simulate dynamics
# ------------------------------------------------------------

def simulate(
    s0,
    local_flow,
    center,
    target=None,
    steps=300,
    dt=0.08,
    control_step=None,
    control_vector=None,
    control_gain=0.2
):

    traj = [s0.copy()]
    s = s0.copy()

    for t in range(steps):

        v = structure_flow(
            s,
            local_flow,
            center,
            target=target
        )

        # control injection
        if control_step is not None and t == control_step:
            v = v + control_gain * control_vector

        s = s + dt * v
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

    local_flow = learn_local_flow(states, k=25)

    # global center (fallback structure)
    center = np.mean(states, axis=0)

    # start point (same as before)
    start_index = 67
    s0 = states[start_index].copy()

    # define artificial target (slightly shifted region)
    target = s0 + np.array([0.0, -0.5])

    control_vector = target_vector(s0, target)

    # baseline
    baseline = simulate(
        s0,
        local_flow,
        center,
        target=None,
        steps=300
    )

    # controlled
    controlled = simulate(
        s0,
        local_flow,
        center,
        target=target,
        steps=300,
        control_step=10,
        control_vector=control_vector
    )

    # deviation
    deviation = np.linalg.norm(controlled - baseline, axis=1)

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(states[:, 1], states[:, 0], s=2, alpha=0.1, label="field")

    plt.plot(baseline[:, 1], baseline[:, 0], label="baseline")
    plt.plot(controlled[:, 1], controlled[:, 0], label="controlled")

    plt.scatter(s0[1], s0[0], color="red", s=70, label="start")

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v65 — Structure-Aware Flow (Fixed)")

    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v65_structure_aware_flow.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot deviation
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))

    plt.plot(deviation)
    plt.axvline(10, linestyle="--")

    plt.title("Deviation over time")

    dev_path = os.path.join(
        OUT_DIR,
        "v65_structure_aware_flow_deviation.png"
    )

    plt.savefig(dev_path, dpi=200)
    plt.close()

    print("NEXAH v65 complete (FIXED)")
    print(f"Final deviation: {deviation[-1]:.6f}")
    print(f"Max deviation:   {np.max(deviation):.6f}")
    print(f"Saved: {out_path}")
