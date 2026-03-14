"""
NEXAH Lorenz Trajectory on Potential Landscape

This script overlays a Lorenz trajectory onto the previously computed
potential landscape derived from the resilience map.

Pipeline:

resilience_map.csv
    ↓
quasi-potential field V(x,z)
    ↓
Lorenz trajectory
    ↓
trajectory projected onto landscape

Outputs stored in:

APPLICATIONS/outputs/lorenz_potential/

Artifacts:
- lorenz_trajectory_on_landscape.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Paths
# ---------------------------------------------------

INPUT_FILE = "APPLICATIONS/outputs/lorenz_resilience/lorenz_resilience_map.csv"
OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_potential"
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
# Load potential landscape
# ---------------------------------------------------

def load_potential():
    tau = np.loadtxt(INPUT_FILE, delimiter=",")

    rows, cols = tau.shape

    xs = np.linspace(-4, 4, cols)
    zs = np.linspace(15, 35, rows)

    epsilon = 1e-6
    V = 1.0 / (tau + epsilon)

    # normalize for plotting
    V = (V - V.min()) / (V.max() - V.min())

    return V, xs, zs


# ---------------------------------------------------
# Generate Lorenz trajectory
# ---------------------------------------------------

def generate_trajectory(steps=12000, t_max=40.0, init_state=(-3.0, 0.0, 25.0)):
    t = np.linspace(0, t_max, steps)
    traj = odeint(lorenz, init_state, t)
    return traj


# ---------------------------------------------------
# Bilinear interpolation of landscape height
# ---------------------------------------------------

def sample_potential_height(x, z, xs, zs, V):
    """
    Sample normalized potential V(x,z) from the grid using nearest-neighbor
    lookup for robustness and simplicity.
    """
    if x < xs[0] or x > xs[-1] or z < zs[0] or z > zs[-1]:
        return np.nan

    j = np.searchsorted(xs, x)
    i = np.searchsorted(zs, z)

    j = min(max(j, 1), len(xs) - 1)
    i = min(max(i, 1), len(zs) - 1)

    # nearest neighbor among surrounding cell centers
    x_candidates = [j - 1, j]
    z_candidates = [i - 1, i]

    best = None
    best_dist = None

    for ii in z_candidates:
        for jj in x_candidates:
            dx = x - xs[jj]
            dz = z - zs[ii]
            dist = dx * dx + dz * dz

            if best_dist is None or dist < best_dist:
                best_dist = dist
                best = V[ii, jj]

    return best


# ---------------------------------------------------
# Plot trajectory on landscape
# ---------------------------------------------------

def plot_trajectory_on_landscape(V, xs, zs, traj):
    X, Z = np.meshgrid(xs, zs)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    # surface
    ax.plot_surface(
        X,
        Z,
        V,
        cmap="magma",
        linewidth=0,
        antialiased=True,
        alpha=0.82
    )

    # project Lorenz trajectory onto landscape coordinates (x,z,V(x,z))
    tx = []
    tz = []
    tv = []

    for x, y, z in traj:
        if xs[0] <= x <= xs[-1] and zs[0] <= z <= zs[-1]:
            v = sample_potential_height(x, z, xs, zs, V)
            if not np.isnan(v):
                tx.append(x)
                tz.append(z)
                tv.append(v + 0.01)  # slight lift so line is visible

    if len(tx) > 1:
        ax.plot(
            tx,
            tz,
            tv,
            linewidth=2.0,
            label="Lorenz trajectory on landscape"
        )

        # mark start and end
        ax.scatter(
            [tx[0]], [tz[0]], [tv[0]],
            s=60,
            label="start"
        )
        ax.scatter(
            [tx[-1]], [tz[-1]], [tv[-1]],
            s=60,
            label="end"
        )

    ax.set_title("Lorenz Trajectory on Potential Landscape")
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("Instability Potential")

    ax.legend()

    path = os.path.join(OUTPUT_DIR, "lorenz_trajectory_on_landscape.png")
    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()
    plt.close()


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():
    print("\nGenerating Lorenz trajectory on potential landscape...\n")

    V, xs, zs = load_potential()
    traj = generate_trajectory()

    plot_trajectory_on_landscape(V, xs, zs, traj)

    print("\nLorenz trajectory-on-landscape plot finished.\n")


if __name__ == "__main__":
    main()
