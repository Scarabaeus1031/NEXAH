# energy_density_map_mod7.py

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
WINDOW = 9
ANGLE_THRESHOLD = 0.8
RADIUS_STABILITY = 0.15
GRID_N = 220
XMIN, XMAX = -1.0, 1.0
YMIN, YMAX = -1.0, 1.0
SIGMA = 0.04

# ============================================================
# PRIME GENERATOR
# ============================================================

def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = False
    return np.where(sieve)[0]

# ============================================================
# TRANSITION + SPECTRAL
# ============================================================

def build_transition_matrix(primes):
    residues = primes % 7
    T = np.zeros((7, 7), dtype=float)

    for i in range(len(residues) - 1):
        a, b = residues[i], residues[i + 1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    T = T / row_sums
    return T, residues

def spectral_projection(T):
    eigvals, eigvecs = eig(T)
    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]
    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

def project_flow(residues, coords):
    traj = np.array([coords[r] for r in residues], dtype=float)
    x, y = traj[:, 0], traj[:, 1]
    theta = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)
    dtheta = np.diff(theta)
    dr = np.diff(r)
    return x, y, theta, r, dtheta, dr

# ============================================================
# ENERGY DEFINITIONS
# ============================================================

def local_energy(dtheta, dr):
    # rotational + radial activity
    return np.abs(dtheta) + 0.5 * np.abs(dr)

def local_density_field(x, y, weights):
    xs = np.linspace(XMIN, XMAX, GRID_N)
    ys = np.linspace(YMIN, YMAX, GRID_N)
    X, Y = np.meshgrid(xs, ys)

    Z = np.zeros_like(X, dtype=float)

    for xi, yi, wi in zip(x, y, weights):
        Z += wi * np.exp(-((X - xi)**2 + (Y - yi)**2) / (2 * SIGMA**2))

    return xs, ys, Z

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("ENERGY DENSITY MAP (mod 7)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)
    x, y, theta, r, dtheta, dr = project_flow(residues, coords)

    # align lengths
    x2 = x[:-1]
    y2 = y[:-1]

    E = local_energy(dtheta, dr)

    print(f"\nEnergy stats:")
    print(f"Mean: {np.mean(E):.6f}")
    print(f"Std:  {np.std(E):.6f}")
    print(f"Max:  {np.max(E):.6f}")

    xs, ys, Z = local_density_field(x2, y2, E)

    # identify top energy points
    top_idx = np.argsort(E)[-25:]

    # --------------------------------------------------------
    # Plot 1: energy density field
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    plt.imshow(
        Z,
        origin="lower",
        extent=[XMIN, XMAX, YMIN, YMAX],
        aspect="equal"
    )
    plt.colorbar(label="energy density")

    plt.scatter(x2[top_idx], y2[top_idx], color="red", s=20, label="top energy points")
    plt.title("Energy Density Map in mod-7 Spectral Space")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: energy over time
    # --------------------------------------------------------
    plt.figure(figsize=(12, 4))
    plt.plot(E, lw=1)
    plt.title("Local Energy Over Time")
    plt.xlabel("Prime index")
    plt.ylabel("Energy")
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 3: energy histogram
    # --------------------------------------------------------
    plt.figure(figsize=(8, 4))
    plt.hist(E, bins=40)
    plt.title("Energy Distribution")
    plt.xlabel("Energy")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
