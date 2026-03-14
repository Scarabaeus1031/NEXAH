"""
NEXAH Lorenz Transition Channel

This script isolates and visualizes the Lorenz transition channel:
the region where the trajectory moves between left and right attractor wings.

Outputs stored in:

APPLICATIONS/outputs/lorenz_transition_channel/

Artifacts:
- lorenz_transition_channel.png
- lorenz_transition_channel.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_transition_channel"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Lorenz system
# ---------------------------------------------------

def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state
    return [
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    ]


# ---------------------------------------------------
# Generate trajectory
# ---------------------------------------------------

def generate_trajectory(steps=80000, t_max=80.0):
    t = np.linspace(0, t_max, steps)
    traj = odeint(lorenz, [1.0, 1.0, 1.0], t)
    return traj


# ---------------------------------------------------
# Transition channel filter
# ---------------------------------------------------

def is_transition_channel(x, y, z):
    """
    Heuristic filter for the Lorenz switch/gate region.

    This selects points near the central bridge where attractor switching
    becomes possible.
    """
    return (
        abs(x) < 6.0 and
        8.0 < z < 32.0
    )


def extract_transition_points(traj):
    points = []

    for x, y, z in traj:
        if is_transition_channel(x, y, z):
            points.append((x, y, z))

    return points


# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

def save_csv(points):
    path = os.path.join(OUTPUT_DIR, "lorenz_transition_channel.csv")

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "z"])
        for row in points:
            writer.writerow(row)

    print("Saved:", path)


# ---------------------------------------------------
# Plot
# ---------------------------------------------------

def plot_transition_channel(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")

    ax.scatter(xs, ys, zs, s=1)

    ax.set_title("Lorenz Transition Channel")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    path = os.path.join(OUTPUT_DIR, "lorenz_transition_channel.png")
    plt.savefig(path, dpi=250)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    print("\nGenerating Lorenz transition channel...\n")

    traj = generate_trajectory()
    points = extract_transition_points(traj)

    print("Number of transition-channel points:", len(points))

    save_csv(points)
    plot_transition_channel(points)

    print("\nLorenz transition channel finished.\n")


if __name__ == "__main__":
    main()
