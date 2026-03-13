"""
Lorenz Separatrix Zoom

Zoom into the fractal basin boundary near the separatrix.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

sigma = 10
rho = 28
beta = 8/3

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# -------------------------------
# Lorenz system
# -------------------------------

def lorenz(state):

    x,y,z = state

    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y-beta*z

    return np.array([dx,dy,dz])


# -------------------------------
# trajectory simulation
# -------------------------------

def simulate_lobe(x0,z0):

    dt = 0.01
    steps = 3000

    state = np.array([x0,0,z0])

    sign_sum = 0

    for _ in range(steps):

        state = state + dt*lorenz(state)

        sign_sum += np.sign(state[0])

    if sign_sum > 0:
        return 1
    else:
        return -1


# -------------------------------
# zoom parameters
# -------------------------------

center_x = 0
center_z = 27

scales = [4,2,1,0.5]

resolution = 150


# -------------------------------
# compute zooms
# -------------------------------

for scale in scales:

    print("Zoom scale:",scale)

    x_vals = np.linspace(center_x-scale, center_x+scale, resolution)
    z_vals = np.linspace(center_z-scale, center_z+scale, resolution)

    basin = np.zeros((resolution,resolution))

    for i,x in enumerate(x_vals):

        print("row",i,"/",resolution)

        for j,z in enumerate(z_vals):

            basin[j,i] = simulate_lobe(x,z)

    plt.figure(figsize=(6,6))

    plt.imshow(
        basin,
        extent=[x_vals.min(),x_vals.max(),z_vals.min(),z_vals.max()],
        origin="lower",
        cmap="coolwarm",
        aspect="auto"
    )

    plt.xlabel("X")
    plt.ylabel("Z")
    plt.title(f"Lorenz Separatrix Zoom (scale={scale})")

    file_output = f"{OUTPUT_DIR}/lorenz_separatrix_zoom_{scale}_{timestamp}.png"

    plt.savefig(file_output,dpi=300,bbox_inches="tight")

    print("saved:",file_output)

    plt.show()
