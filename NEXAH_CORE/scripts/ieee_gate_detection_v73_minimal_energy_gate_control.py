# ============================================================
# NEXAH — IEEE GATE DETECTION v73
# Minimal Energy Gate Control
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


# ------------------------------------------------------------
# Build field (same base dynamics)
# ------------------------------------------------------------

def build_field():
    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.5 * np.sin(3 * t)
        + 0.2 * np.sin(7 * t)
    )

    y = (
        np.cos(t)
        + 0.3 * np.cos(2 * t)
        + 0.2 * np.cos(5 * t)
    )

    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    return np.stack([r, theta], axis=1)


# ------------------------------------------------------------
# Known structure (from v68 / v69)
# ------------------------------------------------------------

def load_structure():
    basins = {
        0: np.array([0.8715, 0.6494]),
        1: np.array([0.9310, -2.3343]),
        2: np.array([1.8223, 2.6151]),
        3: np.array([1.6242, -1.3514]),
        4: np.array([1.7431, 0.5090]),
    }

    gates = {
        (0, 3): np.array([1.1488, -0.1580]),
        (3, 1): np.array([1.4856, -1.5620]),
    }

    path = [0, 3, 1]

    return basins, gates, path


# ------------------------------------------------------------
# Minimal energy search
# ------------------------------------------------------------

def simulate_with_scale(states, start_idx, path, gates, scale):

    current_gate_idx = 0
    trajectory = [states[start_idx]]
    boosts = []

    s = states[start_idx].copy()

    for step in range(300):

        # Determine target
        if current_gate_idx < len(path) - 1:
            a = path[current_gate_idx]
            b = path[current_gate_idx + 1]
            gate = gates[(a, b)]
            target = gate
        else:
            target = None

        if target is None:
            break

        # Distance to gate
        dist = state_distance(s, target)

        # Gate reached?
        if dist < 0.2:
            current_gate_idx += 1
            continue

        # Direction
        u = unit_vector_to_target(s, target)

        # Apply minimal scaled control
        control = scale * u

        # Integrate step (simple Euler proxy)
        s = s + 0.05 * control

        trajectory.append(s)
        boosts.append(np.linalg.norm(control))

    reached = current_gate_idx

    return np.array(trajectory), np.array(boosts), reached


def find_minimal_scale(states, start_idx, path, gates):

    scales = np.linspace(0.05, 1.0, 30)

    best_scale = None
    best_energy = np.inf
    best_result = None

    for scale in scales:

        traj, boosts, reached = simulate_with_scale(
            states, start_idx, path, gates, scale
        )

        if reached == len(path) - 1:
            energy = np.sum(boosts**2)

            if energy < best_energy:
                best_energy = energy
                best_scale = scale
                best_result = (traj, boosts, reached)

    return best_scale, best_energy, best_result


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    states = build_field()
    basins, gates, path = load_structure()

    start_idx = 67
    start_state = states[start_idx]

    scale, energy, result = find_minimal_scale(
        states, start_idx, path, gates
    )

    if result is None:
        print("No valid control found")
        return

    traj, boosts, reached = result

    print("NEXAH v73 complete")
    print("Minimal scale:", scale)
    print("Energy:", energy)
    print("Gates reached:", reached, "/", len(path) - 1)

    # --------------------------------------------------------
    # Plot trajectory
    # --------------------------------------------------------

    plt.figure(figsize=(8, 6))

    plt.scatter(states[:, 1], states[:, 0], s=2, alpha=0.2)

    plt.plot(traj[:, 1], traj[:, 0], color="red", linewidth=2)

    for b, pos in basins.items():
        plt.scatter(pos[1], pos[0], s=80)

    for (a, b), g in gates.items():
        plt.scatter(g[1], g[0], color="red", marker="x", s=100)

    plt.title("NEXAH v73 — Minimal Energy Gate Control")
    plt.xlabel("theta")
    plt.ylabel("r")

    plt.tight_layout()
    plt.savefig("v73_minimal_energy_control.png")
    plt.close()

    # --------------------------------------------------------
    # Plot boost
    # --------------------------------------------------------

    plt.figure(figsize=(8, 4))
    plt.plot(boosts)
    plt.title("Minimal Energy Boost")
    plt.xlabel("step")
    plt.ylabel("||u||")

    plt.tight_layout()
    plt.savefig("v73_minimal_energy_boost.png")
    plt.close()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    with open("v73_minimal_energy_summary.txt", "w") as f:
        f.write("NEXAH v73 — Minimal Energy Control\n")
        f.write(f"Scale: {scale}\n")
        f.write(f"Energy: {energy}\n")
        f.write(f"Gates reached: {reached}/{len(path)-1}\n")


if __name__ == "__main__":
    main()
