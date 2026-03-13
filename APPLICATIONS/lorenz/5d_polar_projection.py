"""
Lorenz 5D Polar Projection Attractor

Build a 5D embedding of the Lorenz system using:
(x, y, z, dx/dt, dy/dt)

Then project it into a custom 3D polar-style visualization.

Goal:
Reveal hidden geometric structure beyond the standard (x,y,z) view.
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------------

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0


# ---------------------------------------------------------
# Lorenz system
# ---------------------------------------------------------

def lorenz(state):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz], dtype=float)


# ---------------------------------------------------------
# Simulation
# ---------------------------------------------------------

def simulate(initial_state=(0.1, 0.0, 25.0), dt=0.01, steps=120000):
    state = np.array(initial_state, dtype=float)

    traj = np.zeros((steps, 3), dtype=float)
    deriv = np.zeros((steps, 3), dtype=float)

    for i in range(steps):
        d = lorenz(state)
        state = state + dt * d
        traj[i] = state
        deriv[i] = d

    return traj, deriv


# ---------------------------------------------------------
# 5D polar-style projection
# ---------------------------------------------------------

def project_5d(traj, deriv, alpha=0.025, gamma=0.015):
    x = traj[:, 0]
    y = traj[:, 1]
    z = traj[:, 2]

    dx = deriv[:, 0]
    dy = deriv[:, 1]

    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)

    # 5D -> 3D custom projection
    X = r * np.cos(theta + alpha * dx)
    Y = r * np.sin(theta + alpha * dy)
    Z = z + gamma * (dx - dy)

    return X, Y, Z


# ---------------------------------------------------------
# Plot
# ---------------------------------------------------------

def main():
    print("\nSimulating Lorenz trajectory for 5D polar projection...\n")

    traj, deriv = simulate()

    # skip transient
    traj = traj[5000:]
    deriv = deriv[5000:]

    # subsample
    traj = traj[::3]
    deriv = deriv[::3]

    X, Y, Z = project_5d(traj, deriv)

    c = np.linspace(0, 1, len(X))

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(
        X, Y, Z,
        c=c,
        cmap="viridis",
        s=0.35,
        alpha=0.65
    )

    ax.set_title("Lorenz 5D Polar Projection Attractor")
    ax.set_xlabel("Projected X")
    ax.set_ylabel("Projected Y")
    ax.set_zlabel("Projected Z")

    file_output = f"{OUTPUT_DIR}/lorenz_5d_polar_projection_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
