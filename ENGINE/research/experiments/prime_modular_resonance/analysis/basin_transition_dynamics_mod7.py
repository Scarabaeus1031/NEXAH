# basin_transition_dynamics_mod7.py

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
# CLUSTERING → BASINS
# ============================================================

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
# TRANSITION MATRIX BETWEEN BASINS
# ============================================================

def build_basin_transition_matrix(labels, n_basins):
    M = np.zeros((n_basins, n_basins), dtype=int)

    for i in range(len(labels) - 1):
        a, b = labels[i], labels[i + 1]
        M[a, b] += 1

    return M

def normalize_matrix(M):
    row_sums = M.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return M / row_sums

# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 72)
    print("BASIN TRANSITION DYNAMICS (mod 7)")
    print("=" * 72)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]
    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)

    x, y, theta, r, dtheta, dr = project_flow(residues, coords)

    vortex_idx = detect_vortices(dtheta, dr)
    clusters = cluster_vortices(vortex_idx, x, y)

    centers = [(np.mean(x[c]), np.mean(y[c])) for c in clusters]

    print(f"\nDetected basins: {len(centers)}")

    labels = assign_basins(x, y, centers)

    # --------------------------------------------------------
    # TRANSITION MATRIX
    # --------------------------------------------------------

    M = build_basin_transition_matrix(labels, len(centers))
    P = normalize_matrix(M)

    print("\nTransition counts matrix:")
    print(M)

    print("\nTransition probability matrix:")
    print(np.round(P, 4))

    # --------------------------------------------------------
    # FLOW GRAPH (optional visualization)
    # --------------------------------------------------------

    plt.figure(figsize=(6, 6))
    plt.imshow(P, cmap='viridis')
    plt.colorbar(label="transition probability")
    plt.title("Basin Transition Matrix (mod 7)")
    plt.xlabel("to basin")
    plt.ylabel("from basin")
    plt.xticks(range(len(centers)))
    plt.yticks(range(len(centers)))
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # SEQUENCE VIEW
    # --------------------------------------------------------

    plt.figure(figsize=(12, 4))
    plt.plot(labels, lw=1)
    plt.title("Basin Transitions Over Time")
    plt.xlabel("Prime index")
    plt.ylabel("Basin")
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
