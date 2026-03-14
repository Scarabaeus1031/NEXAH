"""
Lorenz FTLE Surface Reconstruction in 5D Projection

Compute a 2D FTLE field on the (x,z)-plane and project the surface
through a custom 5D-inspired embedding.

This reveals deformed ridge geometry beyond the standard FTLE surface.
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


def local_ftle_and_dynamics(x0, z0, eps=1e-5):
    p0 = np.array([x0, 0.0, z0], dtype=float)
    p1 = p0 + np.array([eps, 0.0, 0.0], dtype=float)

    a = integrate(p0)
    b = integrate(p1)

    d0 = max(eps, 1e-15)
    dT = max(np.linalg.norm(a - b), 1e-15)

    lam = (1.0 / T) * np.log(dT / d0)

    # local dynamics near initial point
    d = lorenz(p0)
    dx, dy, dz = d

    return lam, dx, dy, dz


def compute_surface(res=80):
    x_vals = np.linspace(-20, 20, res)
    z_vals = np.linspace(0, 50, res)

    ftle = np.zeros((res, res), dtype=float)
    DX = np.zeros((res, res), dtype=float)
    DY = np.zeros((res, res), dtype=float)
    DZ = np.zeros((res, res), dtype=float)

    for i, x in enumerate(x_vals):
        print(f"row {i + 1} / {res}")
        for j, z in enumerate(z_vals):
            lam, dx, dy, dz = local_ftle_and_dynamics(x, z)
            ftle[j, i] = lam
            DX[j, i] = dx
            DY[j, i] = dy
            DZ[j, i] = dz

    return x_vals, z_vals, ftle, DX, DY, DZ


def project_surface(X, Z, FTLE, DX, DY, DZ, a=0.02, b=0.015, c=0.03):
    # 5D-inspired deformation of the surface
    XP = X + a * DX
    YP = Z + a * DY
    ZP = FTLE + b * DZ + c * np.sin(FTLE * 2.0)

    return XP, YP, ZP


def main():
    print("\nComputing 5D-projected FTLE surface...\n")

    x_vals, z_vals, ftle, DX, DY, DZ = compute_surface(res=80)

    X, Z = np.meshgrid(x_vals, z_vals)
    XP, YP, ZP = project_surface(X, Z, ftle, DX, DY, DZ)

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(
        XP, YP, ZP,
        cmap="plasma",
        linewidth=0,
        antialiased=True,
        alpha=0.95
    )

    plt.colorbar(surf, ax=ax, shrink=0.7, pad=0.08, label="Projected FTLE")

    ax.set_title("Lorenz FTLE Surface Reconstruction (5D Projection)")
    ax.set_xlabel("Projected X")
    ax.set_ylabel("Projected Y")
    ax.set_zlabel("Projected FTLE")

    file_output = f"{OUTPUT_DIR}/lorenz_ftle_surface_5d_projection_{timestamp}.png"
    plt.savefig(file_output, dpi=300, bbox_inches="tight")
    print("saved:", file_output)

    plt.show()
    plt.close()


if __name__ == "__main__":
    main()
