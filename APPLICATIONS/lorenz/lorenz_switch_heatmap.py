"""
Lorenz Switch Frequency Heatmap

Compute how often the system switches lobes
for different initial states in the (x,z) plane.
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
# Lorenz equations
# ------------------------------------------------

def lorenz(state):

    x,y,z = state

    dx = sigma*(y-x)
    dy = x*(rho-z)-y
    dz = x*y-beta*z

    return np.array([dx,dy,dz])


# ------------------------------------------------
# count lobe switches
# ------------------------------------------------

def simulate_switches(x0,z0):

    dt = 0.01
    steps = 5000

    state = np.array([x0,0,z0])

    last_lobe = np.sign(state[0])
    switches = 0

    for _ in range(steps):

        dx = lorenz(state)
        state = state + dt*dx

        new_lobe = np.sign(state[0])

        if new_lobe != last_lobe:
            switches += 1
            last_lobe = new_lobe

    return switches


# ------------------------------------------------
# grid
# ------------------------------------------------

res = 60

x_vals = np.linspace(-20,20,res)
z_vals = np.linspace(0,50,res)

heatmap = np.zeros((res,res))


for i,x in enumerate(x_vals):

    print("row",i,"/",res)

    for j,z in enumerate(z_vals):

        heatmap[j,i] = simulate_switches(x,z)


# ------------------------------------------------
# plot heatmap
# ------------------------------------------------

plt.figure(figsize=(8,6))

plt.imshow(
    heatmap,
    extent=[x_vals.min(),x_vals.max(),z_vals.min(),z_vals.max()],
    origin="lower",
    aspect="auto"
)

plt.colorbar(label="Lobe Switch Count")

plt.xlabel("X")
plt.ylabel("Z")
plt.title("Lorenz Switch Frequency Heatmap")

file_heatmap = f"{OUTPUT_DIR}/lorenz_switch_heatmap_{timestamp}.png"

plt.savefig(file_heatmap,dpi=300,bbox_inches="tight")

print("saved:",file_heatmap)

plt.show()
