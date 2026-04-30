# resonance_node_tracker_mod7.py

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
# TRANSITION MATRIX
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

# ============================================================
# SPECTRAL PROJECTION
# ============================================================

def spectral_projection(T):
    eigvals, eigvecs = eig(T)
    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]
    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

# ============================================================
# FLOW
# ============================================================

def project_flow(residues, coords):
    traj = np.array([coords[r] for r in residues], dtype=float)
    x, y = traj[:, 0], traj[:, 1]
    theta = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)
    dtheta = np.diff(theta)
    dr = np.diff(r)
    return x, y, theta, r, dtheta, dr

# ============================================================
# VORTEX DETECTION
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

# ============================================================
# SIMPLE DENSITY CLUSTERING
# ============================================================

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
# ASSIGN EACH TIME STEP TO NEAREST NODE
# ============================================================

def assign_nodes(x, y, centers):
    if len(centers) == 0:
        return np.full(len(x), -1, dtype=int)

    pts = np.column_stack([x, y])
    centers_arr = np.array(centers, dtype=float)

    labels = []
    for p in pts:
        d = np.sqrt(np.sum((centers_arr - p)**2, axis=1))
        labels.append(int(np.argmin(d)))
    return np.array(labels, dtype=int)

def contiguous_runs(labels):
    runs = []
    if len(labels) == 0:
        return runs

    start = 0
    current = labels[0]

    for i in range(1, len(labels)):
        if labels[i] != current:
            runs.append((current, start, i - 1, i - start))
            start = i
            current = labels[i]

    runs.append((current, start, len(labels) - 1, len(labels) - start))
    return runs

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("RESONANCE NODE TRACKER (mod 7)")
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

    print(f"\nDetected vortex points:   {len(vortex_idx)}")
    print(f"Detected node clusters:   {len(clusters)}")

    for i, c in enumerate(clusters):
        cx, cy = centers[i]
        print(f"Node {i}: size={len(c):4d} center=({cx:.4f}, {cy:.4f})")

    labels = assign_nodes(x, y, centers)
    runs = contiguous_runs(labels)

    print("\nTop residence runs:")
    runs_sorted = sorted(runs, key=lambda z: z[3], reverse=True)
    for node, a, b, L in runs_sorted[:12]:
        print(f"node={node}  start={a:4d}  end={b:4d}  length={L:4d}")

    # --------------------------------------------------------
    # Plot 1: trajectory + nodes
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=2, alpha=0.25, label="trajectory")

    if len(vortex_idx) > 0:
        plt.scatter(x[vortex_idx], y[vortex_idx], color="red", s=15, alpha=0.7, label="vortex points")

    for i, c in enumerate(clusters):
        plt.scatter(x[c], y[c], s=10, alpha=0.25)
        cx, cy = centers[i]
        plt.scatter(cx, cy, color="yellow", edgecolor="black", s=140, zorder=5)
        plt.text(cx + 0.01, cy + 0.01, f"Q{i+1}", fontsize=12, weight="bold")

    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title("Resonance Nodes in mod-7 Spectral Flow")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: node assignment over time
    # --------------------------------------------------------
    plt.figure(figsize=(12, 4))
    plt.plot(labels, lw=1)
    plt.title("Nearest Resonance Node Over Time")
    plt.xlabel("Prime index")
    plt.ylabel("Node label")
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 3: residence lengths per node
    # --------------------------------------------------------
    if len(centers) > 0:
        lengths_by_node = {i: [] for i in range(len(centers))}
        for node, a, b, L in runs:
            if node >= 0:
                lengths_by_node[node].append(L)

        plt.figure(figsize=(10, 4))
        means = [np.mean(lengths_by_node[i]) if lengths_by_node[i] else 0 for i in range(len(centers))]
        plt.bar(range(len(centers)), means)
        plt.title("Mean Residence Length per Resonance Node")
        plt.xlabel("Node")
        plt.ylabel("Mean run length")
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
