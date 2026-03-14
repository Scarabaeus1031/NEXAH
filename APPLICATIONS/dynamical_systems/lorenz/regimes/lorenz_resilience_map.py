"""
NEXAH Lorenz Resilience Map

For each initial condition (x,z) we measure:

tau = time until first lobe switch

This indicates how resilient a state is.

Large tau  -> stable region
Small tau  -> near separatrix

Outputs:

APPLICATIONS/outputs/lorenz_resilience/

Files:
- lorenz_resilience_map.png
- lorenz_resilience_map.csv
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


# ---------------------------------------------------
# Output folder
# ---------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_resilience"
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
# time until lobe switch
# ---------------------------------------------------

def first_switch(traj):

    x = traj[:,0]

    start = np.sign(x[0])

    for i,v in enumerate(x):

        if np.sign(v) != start:
            return i

    return len(x)


# ---------------------------------------------------
# compute resilience map
# ---------------------------------------------------

def compute_map(resolution=160):

    xs = np.linspace(-4,4,resolution)
    zs = np.linspace(15,35,resolution)

    t = np.linspace(0,50,4000)

    tau = np.zeros((resolution,resolution))

    for i,z in enumerate(zs):

        print("row",i+1,"/",resolution)

        for j,x in enumerate(xs):

            init = [x,0,z]

            traj = odeint(lorenz,init,t)

            tau[i,j] = first_switch(traj)

    return tau,xs,zs


# ---------------------------------------------------
# save csv
# ---------------------------------------------------

def save_csv(grid):

    path = os.path.join(
        OUTPUT_DIR,
        "lorenz_resilience_map.csv"
    )

    with open(path,"w",newline="") as f:

        writer = csv.writer(f)

        for row in grid:
            writer.writerow(row.tolist())

    print("Saved:",path)


# ---------------------------------------------------
# plot
# ---------------------------------------------------

def plot_map(grid,xs,zs):

    plt.figure(figsize=(8,8))

    plt.imshow(
        grid,
        extent=[xs[0],xs[-1],zs[0],zs[-1]],
        origin="lower",
        cmap="inferno",
        aspect="auto"
    )

    plt.colorbar(label="time until lobe switch")

    plt.xlabel("X")
    plt.ylabel("Z")

    plt.title("Lorenz Resilience Map")

    path = os.path.join(
        OUTPUT_DIR,
        "lorenz_resilience_map.png"
    )

    plt.savefig(path,dpi=300)

    print("Saved:",path)

    plt.show()

    plt.close()


# ---------------------------------------------------
# main
# ---------------------------------------------------

def main():

    print("\nRunning Lorenz resilience test...\n")

    grid,xs,zs = compute_map()

    save_csv(grid)

    plot_map(grid,xs,zs)

    print("\nResilience test finished.\n")


if __name__ == "__main__":
    main()
