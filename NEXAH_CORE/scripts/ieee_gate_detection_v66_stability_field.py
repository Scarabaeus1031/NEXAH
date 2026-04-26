# ============================================================
# NEXAH — IEEE GATE DETECTION v66
# Stability Field Dynamics (Potential-Based Flow)
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


# ------------------------------------------------------------
# Build data
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
# Density + Potential
# ------------------------------------------------------------

def build_density_field(states):

    data = np.vstack([states[:, 0], states[:, 1]])
    kde = gaussian_kde(data)

    def density(s):
        return kde(np.array([[s[0]], [s[1]]]))[0]

    def potential(s):
        rho = density(s)
        return -np.log(rho + 1e-8)

    def grad_potential(s, eps=1e-3):

        # finite diff
        dx = np.array([eps, 0])
        dy = np.array([0, eps])

        dV_dx = (potential(s + dx) - potential(s - dx)) / (2 * eps)
        dV_dy = (potential(s + dy) - potential(s - dy)) / (2 * eps)

        return np.array([dV_dx, dV_dy])

    return density, potential, grad_potential


# ------------------------------------------------------------
# Learned local flow
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
# Combined flow
# ------------------------------------------------------------

def combined_flow(s, local_flow, gradV, alpha=1.0, beta=0.5):

    v_local = local_flow(s)
    v_stable = -gradV(s)

    return alpha * v_local + beta * v_stable


# ------------------------------------------------------------
# Simulation
# ------------------------------------------------------------

def simulate(
    s0,
    local_flow,
    gradV,
    steps=300,
    dt=0.08,
    control_step=None,
    control_vector=None,
    control_gain=0.3
):

    traj = [s0.copy()]
    s = s0.copy()

    for t in range(steps):

        v = combined_flow(s, local_flow, gradV)

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

    local_flow = learn_local_flow(states)

    density, potential, gradV = build_density_field(states)

    start_index = 67
    s0 = states[start_index].copy()

    # small downward push (like before)
    control_vector = np.array([0.0, -1.0])

    # baseline
    baseline = simulate(
        s0,
        local_flow,
        gradV
    )

    # controlled
    controlled = simulate(
        s0,
        local_flow,
        gradV,
        control_step=10,
        control_vector=control_vector
    )

    deviation = np.linalg.norm(controlled - baseline, axis=1)

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(states[:, 1], states[:, 0], s=2, alpha=0.1)

    plt.plot(baseline[:, 1], baseline[:, 0], label="baseline")
    plt.plot(controlled[:, 1], controlled[:, 0], label="controlled")

    plt.scatter(s0[1], s0[0], color="red", s=70)

    plt.title("NEXAH v66 — Stability Field Flow")

    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v66_stability_field.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Deviation
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))

    plt.plot(deviation)
    plt.axvline(10, linestyle="--")

    plt.title("Deviation over time")

    dev_path = os.path.join(
        OUT_DIR,
        "v66_stability_field_deviation.png"
    )

    plt.savefig(dev_path, dpi=200)
    plt.close()

    print("NEXAH v66 complete")
    print(f"Final deviation: {deviation[-1]:.6f}")
    print(f"Max deviation:   {np.max(deviation):.6f}")
    print(f"Saved: {out_path}")
