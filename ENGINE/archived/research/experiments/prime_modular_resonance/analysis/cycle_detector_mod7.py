# cycle_detector_mod7.py

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
CLUSTER_EPS = 0.06
MIN_CLUSTER_SIZE = 8
TOP_K = 12

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

def cluster_vortices(vortex_idx, x, y):
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
                if np.any(dists < CLUSTER_EPS):
                    cluster.append(j)
                    used[j] = True
                    changed = True

        if len(cluster) >= MIN_CLUSTER_SIZE:
            clusters.append(vortex_idx[np.array(cluster, dtype=int)])

    return clusters

# ============================================================
# BASIN ASSIGNMENT
# ============================================================

def nearest_center_label(px, py, centers):
    d = [np.hypot(px - cx, py - cy) for (cx, cy) in centers]
    return int(np.argmin(d))

def assign_basins(x, y, centers):
    return np.array([nearest_center_label(px, py, centers) for px, py in zip(x, y)], dtype=int)

# ============================================================
# CYCLE DETECTION
# ============================================================

def count_triples(labels):
    counts = {}
    for i in range(len(labels) - 2):
        triple = (int(labels[i]), int(labels[i+1]), int(labels[i+2]))
        counts[triple] = counts.get(triple, 0) + 1
    return counts

def normalize_cycle(cycle):
    # rotationally equivalent cycles map to same representative
    rots = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
    return min(rots)

def count_closed_3cycles(labels):
    counts = {}
    for i in range(len(labels) - 2):
        a, b, c = int(labels[i]), int(labels[i+1]), int(labels[i+2])
        if a != b and b != c and a != c:
            cyc = normalize_cycle((a, b, c))
            counts[cyc] = counts.get(cyc, 0) + 1
    return counts

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("CYCLE DETECTOR (mod 7 basins)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)
    x, y, theta, r, dtheta, dr = project_flow(residues, coords)

    vortex_idx = detect_vortices(dtheta, dr)
    clusters = cluster_vortices(vortex_idx, x, y)
    centers = [(float(np.mean(x[c])), float(np.mean(y[c]))) for c in clusters]

    if len(centers) == 0:
        print("No basin centers found.")
        return

    labels = assign_basins(x, y, centers)

    triple_counts = count_triples(labels)
    closed_counts = count_closed_3cycles(labels)

    print("\nTop basin triples:")
    for k, v in sorted(triple_counts.items(), key=lambda z: z[1], reverse=True)[:TOP_K]:
        print(f"{k}: {v}")

    print("\nClosed 3-cycles:")
    for k, v in sorted(closed_counts.items(), key=lambda z: z[1], reverse=True):
        print(f"{k}: {v}")

    # --------------------------------------------------------
    # Plot 1: top triples
    # --------------------------------------------------------
    top_items = sorted(triple_counts.items(), key=lambda z: z[1], reverse=True)[:TOP_K]
    labels_plot = [str(k) for k, _ in top_items]
    vals_plot = [v for _, v in top_items]

    plt.figure(figsize=(10, 4))
    plt.bar(range(len(vals_plot)), vals_plot)
    plt.xticks(range(len(vals_plot)), labels_plot, rotation=45, ha="right")
    plt.ylabel("Count")
    plt.title("Top Basin Triples")
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: closed cycle counts
    # --------------------------------------------------------
    if len(closed_counts) > 0:
        cyc_labels = [str(k) for k, _ in sorted(closed_counts.items(), key=lambda z: z[1], reverse=True)]
        cyc_vals = [v for _, v in sorted(closed_counts.items(), key=lambda z: z[1], reverse=True)]

        plt.figure(figsize=(8, 4))
        plt.bar(range(len(cyc_vals)), cyc_vals)
        plt.xticks(range(len(cyc_vals)), cyc_labels, rotation=45, ha="right")
        plt.ylabel("Count")
        plt.title("Closed 3-Cycles")
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
