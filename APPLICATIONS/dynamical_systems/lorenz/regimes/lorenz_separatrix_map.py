"""
Lorenz Basin / Separatrix Map
High-resolution map of lobe attraction regions.
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
# simulate trajectory
# ------------------------------------------------

def simulate_lobe(x0,z0):

    dt = 0.01
    steps = 4000

    state = np.array([x0,0,z0])

    sign_sum = 0

    for _ in range(steps):

        state = state + dt*lorenz(state)

        sign_sum += np.sign(state[0])

    if sign_sum > 0:
        return 1
    else:
        return -1


# ------------------------------------------------
# grid
# ------------------------------------------------

res = 200

x_vals = np.linspace(-20,20,res)
z_vals = np.linspace(0,50,res)

basin = np.zeros((res,res))


for i,x in enumerate(x_vals):

    print("row",i,"/",res)

    for j,z in enumerate(z_vals):

        basin[j,i] = simulate_lobe(x,z)


# ------------------------------------------------
# plot basin map
# ------------------------------------------------

plt.figure(figsize=(8,6))

plt.imshow(
    basin,
    extent=[x_vals.min(),x_vals.max(),z_vals.min(),z_vals.max()],
    origin="lower",
    cmap="coolwarm",
    aspect="auto"
)

plt.xlabel("X")
plt.ylabel("Z")
plt.title("Lorenz Basin / Separatrix Map")

file_output = f"{OUTPUT_DIR}/lorenz_separatrix_map_{timestamp}.png"

plt.savefig(file_output,dpi=300,bbox_inches="tight")

print("saved:",file_output)

plt.show()
