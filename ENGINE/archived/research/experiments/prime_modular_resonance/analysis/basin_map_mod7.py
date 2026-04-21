# basin_map_mod7.py

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
GRID_N = 220
XMIN, XMAX = -1.0, 1.0
YMIN, YMAX = -1.0, 1.0

WINDOW = 9
ANGLE_THRESHOLD = 0.8
RADIUS_STABILITY = 0.15
CLUSTER_EPS = 0.06
MIN_CLUSTER_SIZE = 8

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
# VORTICES + CLUSTERS
# ============================================================

def detect_vortices(dtheta, dr):
    vortices = []

    for i in range(WINDOW, len(dtheta) - WINDOW):
        local_dtheta = dtheta[i - WINDOW:i + WINDOW]
        local_dr = dr[i - WINDOW:i + WINDOW]

        mean_rot = np.mean(np.abs(local_dtheta))
        std_rot = np.std(local_dtheta)
        std_r = np.std(local_dr)

        if mean_rot > ANGLE_THRESHOLD and std_rot > 0.5 and std_r < RADIUS_STABILITY:
            vortices.append(i)

    return np.array(vortices, dtype=int)

def cluster_vortices(vortex_idx, x, y, eps=CLUSTER_EPS):
    if len(vortex_idx) == 0:
        return []

    points = np.column_stack([x[vortex_idx], y[vortex_idx]])
    used = np.zeros(len(points), dtype=bool)
    clusters = []

    for i in range(len(points)):
        if used[i]:
            continue

        cluster = [i]
        used[i] = True
        changed = True

        while changed:
            changed = False
            for j in range(len(points)):
                if used[j]:
                    continue
                dists = np.sqrt(np.sum((points[cluster] - points[j])**2, axis=1))
                if np.any(dists < eps):
                    cluster.append(j)
                    used[j] = True
                    changed = True

        if len(cluster) >= MIN_CLUSTER_SIZE:
            clusters.append(vortex_idx[np.array(cluster, dtype=int)])

    return clusters

# ============================================================
# BASIN MAP
# ============================================================

def nearest_center_label(px, py, centers):
    d = [np.hypot(px - cx, py - cy) for (cx, cy) in centers]
    return int(np.argmin(d))

def build_basin_grid(centers):
    xs = np.linspace(XMIN, XMAX, GRID_N)
    ys = np.linspace(YMIN, YMAX, GRID_N)

    Z = np.zeros((GRID_N, GRID_N), dtype=int)

    for iy, y in enumerate(ys):
        for ix, x in enumerate(xs):
            Z[iy, ix] = nearest_center_label(x, y, centers)

    return xs, ys, Z

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("BASIN MAP (mod 7)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)
    x, y, theta, r, dtheta, dr = project_flow(residues, coords)

    vortex_idx = detect_vortices(dtheta, dr)
    clusters = cluster_vortices(vortex_idx, x, y)

    centers = []
    for c in clusters:
        centers.append((float(np.mean(x[c])), float(np.mean(y[c]))))

    print(f"\nDetected vortex points: {len(vortex_idx)}")
    print(f"Detected basin centers: {len(centers)}")

    for i, (cx, cy) in enumerate(centers):
        print(f"Basin {i}: center=({cx:.4f}, {cy:.4f})")

    if len(centers) == 0:
        print("\nNo centers found. Basin map cannot be built.")
        return

    xs, ys, Z = build_basin_grid(centers)

    # --------------------------------------------------------
    # Plot 1: basin map
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    plt.imshow(
        Z,
        origin="lower",
        extent=[XMIN, XMAX, YMIN, YMAX],
        aspect="equal",
        alpha=0.85
    )
    plt.colorbar(label="basin index")

    for i, (cx, cy) in enumerate(centers):
        plt.scatter(cx, cy, s=160, edgecolor="black", color="yellow", zorder=5)
        plt.text(cx + 0.015, cy + 0.015, f"Q{i+1}", fontsize=12, weight="bold")

    plt.scatter(x, y, s=2, c="white", alpha=0.18)
    plt.title("mod-7 Resonance Basin Map")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: basin occupancy over time
    # --------------------------------------------------------
    labels = np.array([nearest_center_label(px, py, centers) for px, py in zip(x, y)], dtype=int)

    plt.figure(figsize=(12, 4))
    plt.plot(labels, lw=1)
    plt.title("Basin Occupancy Over Time")
    plt.xlabel("Prime index")
    plt.ylabel("Basin")
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 3: occupancy counts
    # --------------------------------------------------------
    counts = [np.sum(labels == i) for i in range(len(centers))]

    plt.figure(figsize=(8, 4))
    plt.bar(range(len(centers)), counts)
    plt.title("Basin Occupancy Counts")
    plt.xlabel("Basin")
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
