"""
NEXAH Lorenz Visual Pipeline

This script runs the Lorenz adapter and produces:

1. 3D Lorenz attractor visualization
2. regime timeline visualization
3. raw trajectory CSV

All artifacts are stored in:

APPLICATIONS/outputs/lorenz/
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

from APPLICATIONS.adapters.examples.lorenz_adapter import LorenzAdapter


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Generate Lorenz trajectory
# ---------------------------------------------------

def generate_trajectory(steps=2000):

    def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
        x, y, z = state
        return [
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z
        ]

    t = np.linspace(0, 30, steps)
    traj = odeint(lorenz, [1, 1, 1], t)

    return traj


# ---------------------------------------------------
# Save trajectory CSV
# ---------------------------------------------------

def save_csv(traj):

    path = os.path.join(OUTPUT_DIR, "lorenz_trajectory.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z"])

        for row in traj:
            writer.writerow(row)

    print("Saved:", path)


# ---------------------------------------------------
# 3D attractor plot
# ---------------------------------------------------

def plot_attractor(traj):

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    ax.plot(traj[:,0], traj[:,1], traj[:,2], lw=0.5)

    ax.set_title("Lorenz Attractor")

    path = os.path.join(OUTPUT_DIR, "lorenz_attractor.png")

    plt.savefig(path, dpi=200)
    plt.close()

    print("Saved:", path)


# ---------------------------------------------------
# Regime timeline
# ---------------------------------------------------

def plot_regime_timeline(adapter):

    regimes = adapter.regimes()
    states = adapter.states()

    values = []

    mapping = {
        "LEFT_ATTRACTOR": 0,
        "TRANSITION": 1,
        "RIGHT_ATTRACTOR": 2,
        "ESCAPE": 3
    }

    for s in states:
        values.append(mapping[regimes[s]])

    plt.figure(figsize=(10,3))
    plt.plot(values)

    plt.yticks(
        [0,1,2,3],
        ["LEFT","TRANS","RIGHT","ESC"]
    )

    plt.title("Lorenz Regime Timeline")

    path = os.path.join(OUTPUT_DIR, "lorenz_regime_timeline.png")

    plt.savefig(path, dpi=200)
    plt.close()

    print("Saved:", path)


# ---------------------------------------------------
# Main pipeline
# ---------------------------------------------------

def main():

    print("\nRunning Lorenz visual pipeline...\n")

    traj = generate_trajectory()

    adapter = LorenzAdapter()

    save_csv(traj)

    plot_attractor(traj)

    plot_regime_timeline(adapter)

    print("\nPipeline finished.\n")


if __name__ == "__main__":
    main()
