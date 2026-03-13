"""
Lorenz Density Nebula

Compute a 3D density map of where the Lorenz system spends time.
This reveals the hidden structure of the attractor.

Output:
3D chaos density visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


# ---------------------------------------------------
# output
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------

sigma = 10
rho = 28
beta = 8/3


# ---------------------------------------------------
# Lorenz equations
# ---------------------------------------------------

def lorenz(state):

    x, y, z = state

    dx = sigma*(y-x)
    dy = x*(rho-z) - y
    dz = x*y - beta*z

    return np.array([dx,dy,dz])


# ---------------------------------------------------
# simulation
# ---------------------------------------------------

def simulate():

    dt = 0.01
    steps = 200000

    state = np.array([0.1,0.0,25.0])

    traj = np.zeros((steps,3))

    for i in range(steps):

        state = state + dt*lorenz(state)
        traj[i] = state

    return traj


# ---------------------------------------------------
# build density field
# ---------------------------------------------------

def density_field(traj):

    bins = 120

    H, edges = np.histogramdd(
        traj,
        bins=bins
    )

    return H


# ---------------------------------------------------
# visualize density cloud
# ---------------------------------------------------

def plot_density(H):

    threshold = np.percentile(H, 97)

    xs,ys,zs = np.where(H > threshold)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(
        xs,
        ys,
        zs,
        s=1,
        alpha=0.3
    )

    ax.set_title("Lorenz Density Nebula")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    file_output = f"{OUTPUT_DIR}/lorenz_density_nebula_{timestamp}.png"

    plt.savefig(file_output, dpi=300, bbox_inches="tight")

    print("saved:", file_output)

    plt.show()


# ---------------------------------------------------
# main
# ---------------------------------------------------

print("\nSimulating Lorenz density field...\n")

traj = simulate()

print("Building density map...\n")

H = density_field(traj)

print("Rendering nebula...\n")

plot_density(H)
