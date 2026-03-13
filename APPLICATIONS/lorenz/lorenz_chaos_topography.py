"""
Lorenz Chaos Topography

Map of chaos intensity using lobe switch frequency.
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


# -----------------------------
# Lorenz system
# -----------------------------

def lorenz(state):

    x,y,z = state

    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y-beta*z

    return np.array([dx,dy,dz])


# -----------------------------
# measure chaos
# -----------------------------

def chaos_measure(x0,z0):

    dt = 0.01
    steps = 6000

    state = np.array([x0,0,z0])

    last_lobe = np.sign(state[0])
    switches = 0

    for _ in range(steps):

        state = state + dt*lorenz(state)

        new_lobe = np.sign(state[0])

        if new_lobe != last_lobe:

            switches += 1
            last_lobe = new_lobe

    return switches


# -----------------------------
# grid
# -----------------------------

res = 200

x_vals = np.linspace(-20,20,res)
z_vals = np.linspace(0,50,res)

chaos_map = np.zeros((res,res))


for i,x in enumerate(x_vals):

    print("row",i,"/",res)

    for j,z in enumerate(z_vals):

        chaos_map[j,i] = chaos_measure(x,z)


# -----------------------------
# plot
# -----------------------------

plt.figure(figsize=(9,7))

plt.imshow(
    chaos_map,
    extent=[x_vals.min(),x_vals.max(),z_vals.min(),z_vals.max()],
    origin="lower",
    cmap="plasma",
    aspect="auto"
)

plt.colorbar(label="Lobe Switch Count")

plt.xlabel("X")
plt.ylabel("Z")

plt.title("Lorenz Chaos Topography")

file_output = f"{OUTPUT_DIR}/lorenz_chaos_topography_{timestamp}.png"

plt.savefig(file_output,dpi=300,bbox_inches="tight")

print("saved:",file_output)

plt.show()
