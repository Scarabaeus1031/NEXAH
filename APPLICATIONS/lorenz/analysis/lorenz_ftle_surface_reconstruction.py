"""
Lorenz FTLE Surface Reconstruction

Compute a 2D FTLE field on the (x,z)-plane and render it
as a 3D surface.

This reveals the ridge landscape as a continuous surface.
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt


OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

dt = 0.01
T = 4.0
steps = int(T / dt)


def lorenz(state):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz], dtype=float)


def integrate(state):
    s = state.copy()

    for _ in range(steps):
        s = s + dt * lorenz(s)

    return s


def local_ftle(x0, z0, eps=1e-5):
    p0 = np.array([x0, 0.0, z0], dtype=float)
    p1 = p0 + np.array([eps, 0.0, 0.0], dtype=float)

    a = integrate(p0)
    b = integrate(p1)

    d0 = max(eps, 1e-15)
    dT = max(np.linalg.norm(a - b), 1e-15)

    return (1.0 / T) * np.log(dT / d0)


def compute_ftle_surface(res=90):
    x_vals = np.linspace(-20, 20, res)
    z_vals = np.linspace(0, 50, res)

    ftle = np.zeros((res, res), dtype=float)

    for i, x in enumerate(x_vals):
        print(f"row {i + 1} / {res}")
        for j, z in enumerate(z_vals):
            ftle[j, i] = local_ftle(x, z)

    return x_vals, z_vals, ftle


def main():
    print("\nComputing FTLE surface...\n")

    x_vals, z_vals, ftle = compute_ftle_surface(res=90)

    X, Z = np.meshgrid(x_vals, z_vals)

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(
        X, Z, ftle,
        cmap="inferno",
        linewidth=0,
        antialiased=True,
        alpha=0.95
    )

    plt.colorbar(surf, ax=ax, shrink=0.7, pad=0.08, label="FTLE")

    ax.set_title("Lorenz FTLE Surface Reconstruction")
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("FTLE")

    file_output = f"{OUTPUT_DIR}/lorenz_ftle_surface_reconstruction_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
