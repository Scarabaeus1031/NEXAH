import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig
import os

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 1500
RADIUS = 1.0

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
# TRANSITION MATRIX
# ============================================================

def build_transition_matrix(primes):
    residues = primes % 7
    T = np.zeros((7,7))

    for i in range(len(residues)-1):
        a, b = residues[i], residues[i+1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums
    return T, residues

# ============================================================
# HEXAGON POSITIONS
# ============================================================

def hex_positions():
    angles = np.linspace(0, 2*np.pi, 7, endpoint=False)
    x = RADIUS * np.cos(angles)
    y = RADIUS * np.sin(angles)
    return x, y

# ============================================================
# FLOW FIELD (from spectral)
# ============================================================

def spectral_flow(T):
    eigvals, eigvecs = eig(T)

    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]

    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

# ============================================================
# MAIN
# ============================================================

def main():
    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]

    T, residues = build_transition_matrix(primes)
    hx, hy = hex_positions()
    coords = spectral_flow(T)

    fig, ax = plt.subplots(figsize=(8,8))

    # --------------------------------------------------------
    # LAYER 1 — HEXAGON NODES
    # --------------------------------------------------------
    ax.scatter(hx, hy, s=120, zorder=5)

    for i in range(7):
        ax.text(hx[i]*1.1, hy[i]*1.1, str(i),
                ha='center', va='center', fontsize=10)

    # --------------------------------------------------------
    # LAYER 2 — TRANSITIONS
    # --------------------------------------------------------
    for i in range(7):
        for j in range(7):
            w = T[i,j]
            if w > 0.05:
                ax.plot([hx[i], hx[j]],
                        [hy[i], hy[j]],
                        linewidth=2*w,
                        alpha=0.5)

    # --------------------------------------------------------
    # LAYER 3 — FLOW TRAJECTORY
    # --------------------------------------------------------
    traj = np.array([coords[r] for r in residues])
    x, y = traj[:,0], traj[:,1]

    ax.plot(x, y, linewidth=0.5, alpha=0.3)

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(
        "PRIME MODULAR RESONANCE\nDiscrete → Geometric Emergence",
        fontsize=12
    )

    # --------------------------------------------------------
    # SAVE / SHOW
    # --------------------------------------------------------
    if os.environ.get("AUTO_SAVE") == "1":
        fig.savefig("output/plots/title_visual_mod7.png",
                    dpi=200, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

# ============================================================
if __name__ == "__main__":
    main()
