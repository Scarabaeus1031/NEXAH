"""
NEXAH Lorenz Regime Map

This script renders the full Lorenz attractor and colors each
trajectory point by regime classification.

Outputs stored in:

APPLICATIONS/outputs/lorenz_regime_map/

Artifacts:
- lorenz_regime_map.png
- lorenz_regime_points.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output directory
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_regime_map"
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
# Regime classification
# ---------------------------------------------------

def classify(x, y, z):

    if abs(x) > 25 or abs(y) > 25 or z > 45:
        return "ESCAPE"

    elif x < -5:
        return "LEFT_ATTRACTOR"

    elif x > 5:
        return "RIGHT_ATTRACTOR"

    else:
        return "TRANSITION"


COLORS = {
    "LEFT_ATTRACTOR": "blue",
    "RIGHT_ATTRACTOR": "red",
    "TRANSITION": "gold",
    "ESCAPE": "black"
}


# ---------------------------------------------------
# Generate trajectory
# ---------------------------------------------------

def generate_lorenz(steps=40000):

    t = np.linspace(0, 60, steps)

    traj = odeint(
        lorenz,
        [1.0, 1.0, 1.0],
        t
    )

    return traj


# ---------------------------------------------------
# Save CSV
# ---------------------------------------------------

def save_csv(points):

    path = os.path.join(OUTPUT_DIR, "lorenz_regime_points.csv")

    with open(path, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(["x", "y", "z", "regime"])

        for row in points:
            writer.writerow(row)

    print("Saved:", path)


# ---------------------------------------------------
# Plot attractor
# ---------------------------------------------------

def plot_map(points):

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(projection="3d")

    xs = []
    ys = []
    zs = []
    colors = []

    for x, y, z, regime in points:

        xs.append(x)
        ys.append(y)
        zs.append(z)

        colors.append(COLORS[regime])

    ax.scatter(
        xs,
        ys,
        zs,
        c=colors,
        s=1
    )

    ax.set_title("Lorenz Regime Map")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    path = os.path.join(OUTPUT_DIR, "lorenz_regime_map.png")

    plt.savefig(path, dpi=250)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main pipeline
# ---------------------------------------------------

def main():

    print("\nGenerating Lorenz regime map...\n")

    traj = generate_lorenz()

    points = []

    counts = {
        "LEFT_ATTRACTOR": 0,
        "RIGHT_ATTRACTOR": 0,
        "TRANSITION": 0,
        "ESCAPE": 0
    }

    for x, y, z in traj:

        regime = classify(x, y, z)

        counts[regime] += 1

        points.append((x, y, z, regime))

    print("Regime counts:\n")

    for k, v in counts.items():
        print(f"{k}: {v}")

    save_csv(points)

    plot_map(points)

    print("\nLorenz regime map finished.\n")


if __name__ == "__main__":
    main()
