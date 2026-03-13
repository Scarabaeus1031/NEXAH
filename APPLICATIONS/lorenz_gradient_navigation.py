"""
NEXAH Lorenz Gradient Navigation Visualization

Shows:

• Potential landscape
• Gradient field (stability directions)
• Lorenz trajectory

This is the full regime navigation map.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


INPUT_FILE = "APPLICATIONS/outputs/lorenz_resilience/lorenz_resilience_map.csv"
OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Lorenz system
# ---------------------------------------------------

def lorenz(state, t, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return [dx, dy, dz]


# ---------------------------------------------------
# Load landscape
# ---------------------------------------------------

def load_landscape():

    tau = np.loadtxt(INPUT_FILE, delimiter=",")

    rows, cols = tau.shape

    xs = np.linspace(-4, 4, cols)
    zs = np.linspace(15, 35, rows)

    epsilon = 1e-6

    V = 1.0 / (tau + epsilon)

    V = (V - V.min()) / (V.max() - V.min())

    return V, xs, zs


# ---------------------------------------------------
# Gradient field
# ---------------------------------------------------

def compute_gradient(V, xs, zs):

    dV_dz, dV_dx = np.gradient(V)

    return dV_dx, dV_dz


# ---------------------------------------------------
# Trajectory
# ---------------------------------------------------

def generate_trajectory():

    t = np.linspace(0, 40, 12000)

    init = [-3, 0, 25]

    traj = odeint(lorenz, init, t)

    return traj


# ---------------------------------------------------
# Sample potential
# ---------------------------------------------------

def sample_height(x, z, xs, zs, V):

    if x < xs[0] or x > xs[-1] or z < zs[0] or z > zs[-1]:
        return None

    j = np.searchsorted(xs, x)
    i = np.searchsorted(zs, z)

    j = min(max(j,1), len(xs)-1)
    i = min(max(i,1), len(zs)-1)

    return V[i,j]


# ---------------------------------------------------
# Plot everything
# ---------------------------------------------------

def plot_navigation(V, xs, zs, traj, dV_dx, dV_dz):

    X, Z = np.meshgrid(xs, zs)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection="3d")

    # surface
    ax.plot_surface(
        X,
        Z,
        V,
        cmap="magma",
        alpha=0.75,
        linewidth=0
    )


    # gradient field (downsample for readability)

    step = 8

    gx = -dV_dx[::step, ::step]
    gz = -dV_dz[::step, ::step]

    xg = X[::step, ::step]
    zg = Z[::step, ::step]
    vg = V[::step, ::step]

    ax.quiver(
        xg,
        zg,
        vg,
        gx,
        gz,
        0,
        length=0.25,
        normalize=True
    )


    # trajectory
    tx = []
    tz = []
    tv = []

    for x,y,z in traj:

        h = sample_height(x,z,xs,zs,V)

        if h is not None:

            tx.append(x)
            tz.append(z)
            tv.append(h+0.02)

    ax.plot(tx, tz, tv, linewidth=2)


    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("Instability potential")

    ax.set_title("Lorenz Navigation Landscape")


    path = os.path.join(
        OUTPUT_DIR,
        "lorenz_navigation_map.png"
    )

    plt.savefig(path, dpi=300)

    print("Saved:", path)

    plt.show()



# ---------------------------------------------------
# main
# ---------------------------------------------------

def main():

    print("\nComputing navigation landscape...\n")

    V, xs, zs = load_landscape()

    dV_dx, dV_dz = compute_gradient(V, xs, zs)

    traj = generate_trajectory()

    plot_navigation(V, xs, zs, traj, dV_dx, dV_dz)


if __name__ == "__main__":
    main()
