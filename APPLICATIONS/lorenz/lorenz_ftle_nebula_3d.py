"""
Lorenz 3D FTLE Nebula

Compute a sparse 3D finite-time Lyapunov field for the Lorenz system
and render the strongest FTLE ridges as a 3D nebula.

This reveals the transport skeleton of chaos in the full phase space.
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Output folder
# ---------------------------------------------------------

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------
# Lorenz parameters
# ---------------------------------------------------------

sigma = 10.0
rho = 28.0
beta = 8 / 3

dt = 0.01
T = 2.5
steps = int(T / dt)


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
# Integrator
# ---------------------------------------------------------

def integrate(state):
    s = state.copy()

    for _ in range(steps):
        s = s + dt * lorenz(s)

    return s


# ---------------------------------------------------------
# Local FTLE estimate
# ---------------------------------------------------------

def local_ftle(x0, y0, z0, eps=1e-5):
    p0 = np.array([x0, y0, z0], dtype=float)
    p1 = p0 + np.array([eps, 0.0, 0.0], dtype=float)

    a = integrate(p0)
    b = integrate(p1)

    d0 = eps
    dT = np.linalg.norm(a - b)

    d0 = max(d0, 1e-15)
    dT = max(dT, 1e-15)

    return (1.0 / T) * np.log(dT / d0)


# ---------------------------------------------------------
# 3D FTLE field
# ---------------------------------------------------------

def compute_ftle_field(res=28):
    x_vals = np.linspace(-20, 20, res)
    y_vals = np.linspace(-30, 30, res)
    z_vals = np.linspace(0, 50, res)

    ftle = np.zeros((res, res, res), dtype=float)

    total = res * res
    done = 0

    for ix, x in enumerate(x_vals):
        for iy, y in enumerate(y_vals):
            for iz, z in enumerate(z_vals):
                ftle[ix, iy, iz] = local_ftle(x, y, z)

            done += 1
            print(f"slice {done} / {total}")

    return x_vals, y_vals, z_vals, ftle


# ---------------------------------------------------------
# Plot FTLE nebula
# ---------------------------------------------------------

def plot_ftle_nebula(x_vals, y_vals, z_vals, ftle):
    threshold = np.percentile(ftle, 96)

    mask = ftle >= threshold
    ix, iy, iz = np.where(mask)

    xs = x_vals[ix]
    ys = y_vals[iy]
    zs = z_vals[iz]
    cs = ftle[ix, iy, iz]

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    sc = ax.scatter(
        xs, ys, zs,
        c=cs,
        cmap="inferno",
        s=4,
        alpha=0.55
    )

    plt.colorbar(sc, ax=ax, shrink=0.7, pad=0.08, label="FTLE")

    ax.set_title("Lorenz 3D FTLE Nebula")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    file_output = f"{OUTPUT_DIR}/lorenz_ftle_nebula_3d_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    print("\nComputing Lorenz 3D FTLE field...\n")

    x_vals, y_vals, z_vals, ftle = compute_ftle_field(res=28)

    print("\nRendering 3D FTLE nebula...\n")

    plot_ftle_nebula(x_vals, y_vals, z_vals, ftle)

    print("\n3D FTLE nebula complete.\n")


if __name__ == "__main__":
    main()
