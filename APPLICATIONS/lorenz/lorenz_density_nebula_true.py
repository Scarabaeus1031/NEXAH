"""
Lorenz Density Nebula (True Phase Space)

Visualizes the real Lorenz attractor density in true (x,y,z) coordinates.
Produces a nebula-like structure of the chaotic flow.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


# ------------------------------------------------
# output
# ------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ------------------------------------------------
# parameters
# ------------------------------------------------

sigma = 10
rho = 28
beta = 8/3


# ------------------------------------------------
# Lorenz system
# ------------------------------------------------

def lorenz(state):

    x,y,z = state

    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y-beta*z

    return np.array([dx,dy,dz])


# ------------------------------------------------
# simulation
# ------------------------------------------------

def simulate():

    dt = 0.01
    steps = 300000

    state = np.array([0.1,0.0,25.0])

    traj = np.zeros((steps,3))

    for i in range(steps):

        state = state + dt*lorenz(state)
        traj[i] = state

    return traj


# ------------------------------------------------
# plot nebula
# ------------------------------------------------

def plot_nebula(traj):

    # skip transient
    traj = traj[5000:]

    # subsample to reduce point count
    traj = traj[::5]

    x = traj[:,0]
    y = traj[:,1]
    z = traj[:,2]

    colors = np.linspace(0,1,len(x))

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(
        x,y,z,
        c=colors,
        cmap="viridis",
        s=0.3,
        alpha=0.6
    )

    ax.set_title("Lorenz Density Nebula (True Phase Space)")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    file_output = f"{OUTPUT_DIR}/lorenz_density_nebula_true_{timestamp}.png"

    plt.savefig(file_output,dpi=300,bbox_inches="tight")

    print("saved:",file_output)

    plt.show()


# ------------------------------------------------
# main
# ------------------------------------------------

print("\nSimulating Lorenz attractor...\n")

traj = simulate()

print("Rendering density nebula...\n")

plot_nebula(traj)
