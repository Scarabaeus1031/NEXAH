import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig
import os

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
RADIUS = 1.0

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

def primes_upto(n: int) -> np.ndarray:
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(np.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = False
    return np.where(sieve)[0]

# ============================================================
# TRANSITION MATRIX
# ============================================================

def build_transition_matrix(primes: np.ndarray):
    residues = primes % 7
    T = np.zeros((7, 7), dtype=float)

    for i in range(len(residues) - 1):
        a, b = residues[i], residues[i + 1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums
    return T, residues

# ============================================================
# HEXAGON / HEPTAGON POSITIONS
# ============================================================

def ring_positions(radius: float = 1.0):
    angles = np.linspace(0, 2 * np.pi, 7, endpoint=False)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return x, y

# ============================================================
# SPECTRAL FLOW
# ============================================================

def spectral_flow(T: np.ndarray) -> np.ndarray:
    eigvals, eigvecs = eig(T)
    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]
    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

# ============================================================
# ENERGY DENSITY
# ============================================================

def local_energy(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    dx = np.diff(x)
    dy = np.diff(y)
    theta = np.arctan2(y, x)
    dtheta = np.diff(np.unwrap(theta))
    dr = np.diff(np.sqrt(x**2 + y**2))
    e = np.abs(dtheta) + 0.5 * np.abs(dr)
    return e

def density_field(x: np.ndarray, y: np.ndarray, weights: np.ndarray,
                  grid_n: int = 240, sigma: float = 0.05):
    xmin, xmax = -1.4, 1.4
    ymin, ymax = -1.4, 1.4
    xs = np.linspace(xmin, xmax, grid_n)
    ys = np.linspace(ymin, ymax, grid_n)
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros_like(X, dtype=float)

    for xi, yi, wi in zip(x, y, weights):
        Z += wi * np.exp(-((X - xi)**2 + (Y - yi)**2) / (2 * sigma**2))

    return X, Y, Z

# ============================================================
# SIMPLE BASIN CENTERS FROM FLOW
# ============================================================

def estimate_basin_centers(x: np.ndarray, y: np.ndarray):
    scores = x + y
    idx = np.argsort(scores)
    groups = np.array_split(idx, 3)
    centers = []
    for g in groups:
        centers.append((float(np.mean(x[g])), float(np.mean(y[g]))))
    return centers

# ============================================================
# BASIN LABELS
# ============================================================

def assign_basins(x: np.ndarray, y: np.ndarray, centers):
    labels = []
    for px, py in zip(x, y):
        d = [np.hypot(px - cx, py - cy) for (cx, cy) in centers]
        labels.append(int(np.argmin(d)))
    return np.array(labels, dtype=int)

# ============================================================
# DOMINANT 3-CYCLE
# ============================================================

def normalize_cycle(cycle):
    rots = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
    return min(rots)

def dominant_closed_3cycle(labels: np.ndarray):
    counts = {}
    for i in range(len(labels) - 2):
        a, b, c = int(labels[i]), int(labels[i + 1]), int(labels[i + 2])
        if a != b and b != c and a != c:
            cyc = normalize_cycle((a, b, c))
            counts[cyc] = counts.get(cyc, 0) + 1

    if not counts:
        return None, {}
    dom = sorted(counts.items(), key=lambda z: z[1], reverse=True)[0][0]
    return dom, counts

# ============================================================
# MAIN
# ============================================================

def main():
    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)

    # outer discrete ring
    hx, hy = ring_positions(RADIUS)

    # inner spectral flow
    coords = spectral_flow(T)
    traj = np.array([coords[r] for r in residues], dtype=float)
    x, y = traj[:, 0], traj[:, 1]

    # basin approximation in spectral space
    centers = estimate_basin_centers(x, y)
    labels = assign_basins(x, y, centers)
    dom_cycle, cycle_counts = dominant_closed_3cycle(labels)

    # energy glow
    e = local_energy(x, y)
    X, Y, Z = density_field(x[:-1], y[:-1], e, grid_n=260, sigma=0.045)

    fig, ax = plt.subplots(figsize=(10, 10))

    # --------------------------------------------------------
    # LAYER 0 — ENERGY GLOW
    # --------------------------------------------------------
    ax.imshow(
        Z,
        origin="lower",
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        cmap="magma",
        alpha=0.45,
        zorder=0
    )

    # --------------------------------------------------------
    # LAYER 1 — OUTER RING
    # --------------------------------------------------------
    ax.plot(
        np.append(hx, hx[0]),
        np.append(hy, hy[0]),
        color="black",
        linewidth=1.2,
        alpha=0.35,
        zorder=1
    )

    # --------------------------------------------------------
    # LAYER 2 — TRANSITION LINES
    # --------------------------------------------------------
    for i in range(7):
        for j in range(7):
            w = T[i, j]
            if w > 0.08:
                ax.plot(
                    [hx[i], hx[j]],
                    [hy[i], hy[j]],
                    color=COLORS[i],
                    linewidth=2.5 * w + 0.3,
                    alpha=0.42,
                    zorder=2
                )

    # --------------------------------------------------------
    # LAYER 3 — SPECTRAL FLOW TRAJECTORY
    # --------------------------------------------------------
    ax.plot(x, y, linewidth=0.5, alpha=0.22, color="white", zorder=3)

    step = max(1, len(residues) // 900)
    for i in range(0, len(residues), step):
        r = int(residues[i])
        ax.scatter(x[i], y[i], color=COLORS[r], s=9, alpha=0.65, zorder=4)

    # --------------------------------------------------------
    # LAYER 4 — OUTER NODES
    # --------------------------------------------------------
    for i in range(7):
        ax.scatter(hx[i], hy[i], s=260, color=COLORS[i], edgecolor="black", linewidth=1.0, zorder=6)
        ax.text(hx[i] * 1.13, hy[i] * 1.13, str(i),
                ha="center", va="center", fontsize=11, weight="bold", zorder=7)

    # --------------------------------------------------------
    # LAYER 5 — BASIN CENTERS
    # --------------------------------------------------------
    for k, (cx, cy) in enumerate(centers):
        ax.scatter(cx, cy, s=220, color="yellow", edgecolor="black", linewidth=1.2, zorder=8)
        ax.text(cx + 0.03, cy + 0.03, f"Q{k+1}", fontsize=12, weight="bold", zorder=9)

    # --------------------------------------------------------
    # LAYER 6 — DOMINANT 3-CYCLE OVERLAY
    # --------------------------------------------------------
    if dom_cycle is not None:
        cyc = list(dom_cycle) + [dom_cycle[0]]
        xs = [centers[i][0] for i in cyc]
        ys = [centers[i][1] for i in cyc]

        ax.plot(xs, ys, color="cyan", linewidth=3.0, alpha=0.9, zorder=10)

        for i in range(len(xs) - 1):
            dx = xs[i + 1] - xs[i]
            dy = ys[i + 1] - ys[i]
            ax.arrow(
                xs[i], ys[i],
                0.82 * dx, 0.82 * dy,
                head_width=0.03,
                head_length=0.045,
                fc="cyan", ec="cyan",
                linewidth=0,
                length_includes_head=True,
                alpha=0.95,
                zorder=11
            )

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)

    subtitle = "Discrete States · Transition Bias · Spectral Flow · Basin Cycles"
    if dom_cycle is not None and dom_cycle in cycle_counts:
        subtitle += f"\nDominant 3-cycle: {dom_cycle}  |  count = {cycle_counts[dom_cycle]}"

    ax.set_title(
        "PRIME MODULAR RESONANCE\nMod 7 — Title Visual III",
        fontsize=16,
        pad=18
    )
    fig.text(0.5, 0.065, subtitle, ha="center", va="center", fontsize=10)

    # --------------------------------------------------------
    # SAVE / SHOW
    # --------------------------------------------------------
    filename = "output/plots/title_visual_iii_mod7.png"

    if os.environ.get("AUTO_SAVE") == "1":
        fig.savefig(filename, dpi=260, bbox_inches="tight")
        plt.close()
        print(f"[SAVED] {filename}")
    else:
        plt.show()

if __name__ == "__main__":
    main()
