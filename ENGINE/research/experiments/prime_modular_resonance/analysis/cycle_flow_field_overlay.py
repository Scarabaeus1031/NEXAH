# cycle_flow_field_overlay.py

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
# VORTEX / BASIN
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

def nearest_center_label(px, py, centers):
    d = [np.hypot(px - cx, py - cy) for (cx, cy) in centers]
    return int(np.argmin(d))

def assign_basins(x, y, centers):
    return np.array([nearest_center_label(px, py, centers) for px, py in zip(x, y)], dtype=int)

# ============================================================
# CYCLE DETECTION
# ============================================================

def normalize_cycle(cycle):
    rots = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
    return min(rots)

def count_closed_3cycles(labels):
    counts = {}
    positions = {}

    for i in range(len(labels) - 2):
        a, b, c = int(labels[i]), int(labels[i+1]), int(labels[i+2])
        if a != b and b != c and a != c:
            cyc = normalize_cycle((a, b, c))
            counts[cyc] = counts.get(cyc, 0) + 1
            positions.setdefault(cyc, []).append(i)

    return counts, positions

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("CYCLE FLOW FIELD OVERLAY (mod 7)")
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
    cycle_counts, cycle_positions = count_closed_3cycles(labels)

    print("\nClosed 3-cycles:")
    for k, v in sorted(cycle_counts.items(), key=lambda z: z[1], reverse=True):
        print(f"{k}: {v}")

    # dominant cycle
    if len(cycle_counts) == 0:
        print("No closed 3-cycles found.")
        return

    dominant_cycle = sorted(cycle_counts.items(), key=lambda z: z[1], reverse=True)[0][0]
    pos = cycle_positions[dominant_cycle]

    print(f"\nDominant cycle: {dominant_cycle}")
    print(f"Occurrences: {len(pos)}")

    # --------------------------------------------------------
    # Plot 1: full flow + dominant cycle edges
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=2, alpha=0.08, color="gray", label="trajectory")

    for i, (cx, cy) in enumerate(centers):
        plt.scatter(cx, cy, s=180, color="yellow", edgecolor="black", zorder=5)
        plt.text(cx + 0.01, cy + 0.01, f"Q{i+1}", fontsize=12, weight="bold")

    cyc = list(dominant_cycle)
    cyc.append(cyc[0])
    for i in range(len(cyc) - 1):
        a = cyc[i]
        b = cyc[i + 1]
        x1, y1 = centers[a]
        x2, y2 = centers[b]
        plt.arrow(
            x1, y1,
            0.82 * (x2 - x1),
            0.82 * (y2 - y1),
            head_width=0.02,
            head_length=0.03,
            linewidth=3,
            color="red",
            alpha=0.85,
            length_includes_head=True
        )

    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title(f"Dominant Basin Cycle Overlay: {dominant_cycle}")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Plot 2: highlight actual trajectory snippets
    # --------------------------------------------------------
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=2, alpha=0.04, color="gray")

    for start in pos[:120]:
        xs = x[start:start+3]
        ys = y[start:start+3]
        plt.plot(xs, ys, alpha=0.35, linewidth=1.5)

    for i, (cx, cy) in enumerate(centers):
        plt.scatter(cx, cy, s=180, color="yellow", edgecolor="black", zorder=5)
        plt.text(cx + 0.01, cy + 0.01, f"Q{i+1}", fontsize=12, weight="bold")

    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)
    plt.title("Trajectory Snippets Following Dominant 3-Cycle")
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
