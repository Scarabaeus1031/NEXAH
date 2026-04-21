import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
GRID_N = 120
XMIN, XMAX = -1.0, 1.0
YMIN, YMAX = -1.0, 1.0

# ============================================================
# PRIME GENERATOR
# ============================================================

def primes_upto(n):
    sieve = np.ones(n+1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(np.sqrt(n))+1):
        if sieve[i]:
            sieve[i*i:n+1:i] = False
    return np.where(sieve)[0]

# ============================================================
# TRANSITION + SPECTRAL
# ============================================================

def build_transition_matrix(primes):
    residues = primes % 7
    T = np.zeros((7,7))

    for i in range(len(residues)-1):
        T[residues[i], residues[i+1]] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums
    return T, residues

def spectral_projection(T):
    eigvals, eigvecs = eig(T)

    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]

    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

# ============================================================
# TRAJECTORY
# ============================================================

def project_flow(residues, coords):
    traj = np.array([coords[r] for r in residues])
    x, y = traj[:,0], traj[:,1]
    return x, y

# ============================================================
# BUILD FLUX FIELD
# ============================================================

def compute_flux_field(x, y):
    dx = np.diff(x)
    dy = np.diff(y)

    # grid
    xs = np.linspace(XMIN, XMAX, GRID_N)
    ys = np.linspace(YMIN, YMAX, GRID_N)

    X, Y = np.meshgrid(xs, ys)
    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    counts = np.zeros_like(X)

    # binning flow into grid
    for i in range(len(dx)):
        gx = int((x[i] - XMIN) / (XMAX - XMIN) * (GRID_N-1))
        gy = int((y[i] - YMIN) / (YMAX - YMIN) * (GRID_N-1))

        if 0 <= gx < GRID_N and 0 <= gy < GRID_N:
            U[gy, gx] += dx[i]
            V[gy, gx] += dy[i]
            counts[gy, gx] += 1

    # normalize
    mask = counts > 0
    U[mask] /= counts[mask]
    V[mask] /= counts[mask]

    return X, Y, U, V

# ============================================================
# DETECT ENERGY NODES (simple clustering)
# ============================================================

def detect_energy_nodes(x, y, n_nodes=3):
    # very simple: k-means style via sorting radius
    r = np.sqrt(x**2 + y**2)
    idx = np.argsort(r)

    split = np.array_split(idx, n_nodes)
    nodes = []

    for s in split:
        cx = np.mean(x[s])
        cy = np.mean(y[s])
        nodes.append((cx, cy))

    return nodes

# ============================================================
# MAIN
# ============================================================

def main():
    print("="*70)
    print("ENERGY FLUX FIELD (mod 7)")
    print("="*70)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]

    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)
    x, y = project_flow(residues, coords)

    # flux field
    X, Y, U, V = compute_flux_field(x, y)

    # nodes
    nodes = detect_energy_nodes(x, y, n_nodes=3)

    # ========================================================
    # PLOT 1: STREAM FIELD
    # ========================================================

    plt.figure(figsize=(8,8))
    plt.streamplot(X, Y, U, V, density=1.2, linewidth=1)

    # nodes
    for i, (cx, cy) in enumerate(nodes):
        plt.scatter(cx, cy, color='red', s=100)
        plt.text(cx+0.02, cy+0.02, f"Q{i+1}")

    plt.title("Energy Flux Field (mod 7)")
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.xlim(XMIN, XMAX)
    plt.ylim(YMIN, YMAX)
    plt.show()

    # ========================================================
    # PLOT 2: VECTOR FIELD
    # ========================================================

    plt.figure(figsize=(8,8))
    plt.quiver(X, Y, U, V, alpha=0.7)

    for i, (cx, cy) in enumerate(nodes):
        plt.scatter(cx, cy, color='yellow', s=120, edgecolor='black')
        plt.text(cx+0.02, cy+0.02, f"Q{i+1}")

    plt.title("Energy Flow Vectors")
    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.xlim(XMIN, XMAX)
    plt.ylim(YMIN, YMAX)
    plt.show()

# ============================================================

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
