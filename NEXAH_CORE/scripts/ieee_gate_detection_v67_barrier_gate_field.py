# ============================================================
# NEXAH — IEEE GATE DETECTION v67
# Barrier Field + Gate Detection
# ============================================================
#
# FILE:
# ieee_gate_detection_v67_barrier_gate_field.py
#
# PURPOSE:
# --------
# Combine the two modes discovered in v65/v66:
#
#   v65 = transport / transition-capable flow
#   v66 = stability / return-to-attractor flow
#
# v67 introduces a barrier field:
#
#   Barrier(s) = instability boundary between stable regions
#
# and detects gates as places where:
#
#   control_energy > barrier_height
#
# OUTPUTS:
# --------
# v67_barrier_gate_field.png
# v67_barrier_gate_profile.png
# v67_barrier_gate_summary.txt
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
# Utilities
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
# Density / Potential / Barrier
# ------------------------------------------------------------

def build_fields(states):

    data = np.vstack([states[:, 0], states[:, 1]])
    kde = gaussian_kde(data)

    def density(s):
        return kde(np.array([[s[0]], [s[1]]]))[0]

    def stability_potential(s):
        rho = density(s)
        return -np.log(rho + 1e-8)

    def grad_potential(s, eps=1e-3):

        er = np.array([eps, 0.0])
        et = np.array([0.0, eps])

        dVr = (
            stability_potential(s + er)
            - stability_potential(s - er)
        ) / (2 * eps)

        dVt = (
            stability_potential(s + et)
            - stability_potential(s - et)
        ) / (2 * eps)

        return np.array([dVr, dVt])

    return density, stability_potential, grad_potential


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
# Barrier height along trajectory
# ------------------------------------------------------------

def compute_barrier_profile(states, potential_fn):

    V = np.array([potential_fn(s) for s in states])

    # local roughness / ridge-like barrier
    dV = np.gradient(V)
    ddV = np.gradient(dV)

    barrier = np.abs(dV) + 0.5 * np.abs(ddV)

    # normalize
    barrier = barrier - np.min(barrier)
    if np.max(barrier) > 1e-12:
        barrier = barrier / np.max(barrier)

    return V, barrier


# ------------------------------------------------------------
# Control energy profile
# ------------------------------------------------------------

def compute_control_energy(states):

    # local curvature/turning energy
    vel = np.gradient(states, axis=0)
    acc = np.gradient(vel, axis=0)

    energy = np.linalg.norm(acc, axis=1)

    energy = energy - np.min(energy)
    if np.max(energy) > 1e-12:
        energy = energy / np.max(energy)

    return energy


# ------------------------------------------------------------
# Gate detection
# ------------------------------------------------------------

def detect_gates(barrier, control_energy, threshold=0.15):

    excess = control_energy - barrier

    gates = np.where(excess > threshold)[0]

    return gates, excess


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":

    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    states = build_pipeline()

    density, V_fn, gradV = build_fields(states)

    local_flow = learn_local_flow(states)

    V, barrier = compute_barrier_profile(states, V_fn)

    control_energy = compute_control_energy(states)

    gates, excess = detect_gates(
        barrier,
        control_energy,
        threshold=0.15
    )

    # --------------------------------------------------------
    # Plot gate field
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        states[:, 1],
        states[:, 0],
        s=2,
        alpha=0.12,
        label="trajectory field"
    )

    if len(gates) > 0:
        plt.scatter(
            states[gates, 1],
            states[gates, 0],
            s=18,
            color="red",
            label="detected gates"
        )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v67 — Barrier Gate Field")

    plt.legend(fontsize=7)
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v67_barrier_gate_field.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Plot profiles
    # --------------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(barrier, label="barrier height")
    plt.plot(control_energy, label="control energy")
    plt.plot(excess, label="excess energy")

    if len(gates) > 0:
        plt.scatter(
            gates,
            excess[gates],
            s=16,
            color="red",
            label="gates"
        )

    plt.axhline(0.15, linestyle="--", linewidth=1, label="gate threshold")

    plt.xlabel("trajectory index")
    plt.ylabel("normalized value")
    plt.title("NEXAH v67 — Barrier / Control / Gate Profile")

    plt.legend(fontsize=8)
    plt.tight_layout()

    profile_path = os.path.join(
        OUT_DIR,
        "v67_barrier_gate_profile.png"
    )

    plt.savefig(profile_path, dpi=200)
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary_path = os.path.join(
        OUT_DIR,
        "v67_barrier_gate_summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:

        f.write("NEXAH v67 — Barrier Gate Field\n")
        f.write("==============================\n\n")

        f.write(f"States: {len(states)}\n")
        f.write(f"Gates detected: {len(gates)}\n\n")

        if len(gates) > 0:
            f.write("Top gate candidates:\n")

            ranked = sorted(
                gates,
                key=lambda i: excess[i],
                reverse=True
            )[:20]

            for i in ranked:
                f.write(
                    f"  index {i}: "
                    f"barrier={barrier[i]:.4f}, "
                    f"control={control_energy[i]:.4f}, "
                    f"excess={excess[i]:.4f}, "
                    f"r={states[i,0]:.4f}, "
                    f"theta={states[i,1]:.4f}\n"
                )

    print("NEXAH v67 complete")
    print(f"Gates detected: {len(gates)}")
    print(f"Saved: {out_path}")
    print(f"Saved: {profile_path}")
    print(f"Saved: {summary_path}")
