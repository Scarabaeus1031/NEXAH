import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig
import os

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
RADIUS = 1.0

# Farben für Residues (stabil & unterscheidbar)
COLORS = [
    "#1f77b4",  # 0
    "#ff7f0e",  # 1
    "#2ca02c",  # 2
    "#d62728",  # 3
    "#9467bd",  # 4
    "#8c564b",  # 5
    "#e377c2"   # 6
]

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
# SPECTRAL FLOW
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

    fig, ax = plt.subplots(figsize=(9,9))

    # --------------------------------------------------------
    # FLOW TRAJECTORY (background)
    # --------------------------------------------------------
    traj = np.array([coords[r] for r in residues])
    x, y = traj[:,0], traj[:,1]

    ax.plot(x, y, linewidth=0.4, alpha=0.25, color="black")

    # --------------------------------------------------------
    # COLORED RESIDUE POINTS (sampled)
    # --------------------------------------------------------
    step = max(1, len(residues)//800)

    for i in range(0, len(residues), step):
        r = residues[i]
        ax.scatter(x[i], y[i], color=COLORS[r], s=8, alpha=0.7)

    # --------------------------------------------------------
    # HEXAGON NODES (foreground)
    # --------------------------------------------------------
    for i in range(7):
        ax.scatter(hx[i], hy[i], s=200, color=COLORS[i], zorder=5)
        ax.text(hx[i]*1.15, hy[i]*1.15, str(i),
                ha='center', va='center', fontsize=11, weight='bold')

    # --------------------------------------------------------
    # TRANSITION LINES (clean & strong)
    # --------------------------------------------------------
    for i in range(7):
        for j in range(7):
            w = T[i,j]
            if w > 0.08:
                ax.plot([hx[i], hx[j]],
                        [hy[i], hy[j]],
                        color=COLORS[i],
                        linewidth=3*w,
                        alpha=0.6)

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(
        "PRIME MODULAR RESONANCE\nMod 7 — Transition → Flow → Structure",
        fontsize=14
    )

    # --------------------------------------------------------
    # SAVE / SHOW
    # --------------------------------------------------------
    filename = "output/plots/title_visual_ii_mod7.png"

    if os.environ.get("AUTO_SAVE") == "1":
        fig.savefig(filename, dpi=250, bbox_inches="tight")
        plt.close()
        print(f"[SAVED] {filename}")
    else:
        plt.show()

# ============================================================
if __name__ == "__main__":
    main()
