"""
NEXAH Resonance Phase Space
===========================

Plots phase space trajectories for the NEXAH resonance kernel.

This allows visualization of attractors, quasiperiodic motion,
limit cycles, and chaotic regions.

Output
------
ENGINE/nexah_kernel/demos/visuals/resonance_landscape/phase_space.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


OUT_IMG = Path(
    "ENGINE/nexah_kernel/demos/visuals/resonance_landscape/phase_space.png"
)

OUT_IMG.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# NEXAH angular dynamics
# --------------------------------------------------

def step(theta, n, drift):

    return (theta + (2*np.pi)/n + np.deg2rad(drift)) % (2*np.pi)


# --------------------------------------------------
# simulate trajectory
# --------------------------------------------------

def simulate(n, drift, steps=2000):

    theta = np.random.rand() * 2*np.pi

    traj = []

    for _ in range(steps):

        theta = step(theta, n, drift)
        traj.append(theta)

    return np.array(traj)


# --------------------------------------------------
# phase space plot
# --------------------------------------------------

def plot_phase_space():

    plt.figure(figsize=(10,6))

    test_cases = [
        (5,0.2),
        (7,1.3),
        (9,2.0),
        (12,3.0),
        (15,4.5)
    ]

    for n, drift in test_cases:

        traj = simulate(n, drift)

        plt.scatter(
            traj[:-1],
            traj[1:],
            s=4,
            alpha=0.5,
            label=f"n={n}, drift={drift}"
        )

    plt.xlabel("θ(t)")
    plt.ylabel("θ(t+1)")

    plt.title("NEXAH Phase Space")

    plt.legend()

    plt.tight_layout()

    plt.savefig(OUT_IMG, dpi=300)

    print("\nSaved phase space:", OUT_IMG)

    plt.show()


# --------------------------------------------------
# main
# --------------------------------------------------

def main():

    print("\nGenerating NEXAH phase space...\n")

    plot_phase_space()


if __name__ == "__main__":
    main()
