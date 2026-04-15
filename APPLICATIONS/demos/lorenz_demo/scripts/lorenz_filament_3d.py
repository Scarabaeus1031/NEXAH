"""
Lorenz Filament 3D

Visualizes the 3D state-space structure of the Lorenz system
by launching many nearby trajectories and plotting them together.

Goal:
Reveal filament-like flow structures in the full 3D state space.
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Output folder
# ---------------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------------

sigma = 10.0
rho = 28.0
beta = 8 / 3


# ---------------------------------------------------------
# Lorenz system
# ---------------------------------------------------------

def lorenz(state):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz])


# ---------------------------------------------------------
# Simulate one trajectory
# ---------------------------------------------------------

def simulate_trajectory(initial_state, dt=0.01, steps=4000):
    state = np.array(initial_state, dtype=float)

    traj = np.zeros((steps, 3), dtype=float)

    for i in range(steps):
        state = state + dt * lorenz(state)
        traj[i] = state

    return traj


# ---------------------------------------------------------
# Build a cloud of nearby trajectories
# ---------------------------------------------------------

def build_filament_bundle(center_state=(0.0, 1.0, 27.0), n_traj=40, spread=0.25):
    trajectories = []

    rng = np.random.default_rng(42)

    for _ in range(n_traj):
        perturbation = rng.normal(0.0, spread, size=3)
        init = np.array(center_state) + perturbation

        traj = simulate_trajectory(init, dt=0.01, steps=3500)
        trajectories.append(traj)

    return trajectories


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("\nBuilding Lorenz 3D filament bundle...\n")

    trajectories = build_filament_bundle(
        center_state=(0.0, 1.0, 27.0),
        n_traj=40,
        spread=0.25
    )

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    for i, traj in enumerate(trajectories):
        ax.plot(
            traj[:, 0],
            traj[:, 1],
            traj[:, 2],
            alpha=0.35,
            linewidth=0.8
        )

        # mark start points for first few only
        if i < 8:
            ax.scatter(
                traj[0, 0],
                traj[0, 1],
                traj[0, 2],
                s=20
            )

    ax.set_title("Lorenz 3D State Space Filaments")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    file_output = f"{OUTPUT_DIR}/lorenz_filament_3d_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
