import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 2000
WINDOW = 5              # local window for stability

# relaxed thresholds (wichtig!)
ANGLE_THRESHOLD = 0.8
RADIUS_STABILITY = 0.15

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
# BUILD TRANSITION MATRIX (mod 7)
# ============================================================

def build_transition_matrix(primes):
    residues = primes % 7
    T = np.zeros((7,7))

    for i in range(len(residues)-1):
        a, b = residues[i], residues[i+1]
        T[a, b] += 1

    # normalize rows
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums
    return T, residues

# ============================================================
# SPECTRAL PROJECTION
# ============================================================

def spectral_projection(T):
    eigvals, eigvecs = eig(T)

    # pick complex conjugate pair
    idx = np.argsort(-np.abs(np.imag(eigvals)))
    v1 = eigvecs[:, idx[0]]
    v2 = eigvecs[:, idx[1]]

    coords = np.vstack([np.real(v1), np.real(v2)]).T
    return coords

# ============================================================
# FLOW TRAJECTORY
# ============================================================

def project_flow(residues, coords):
    traj = np.array([coords[r] for r in residues])
    x, y = traj[:,0], traj[:,1]

    theta = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)

    dtheta = np.diff(theta)
    dr = np.diff(r)

    return x, y, theta, r, dtheta, dr

# ============================================================
# VORTEX DETECTION (improved!)
# ============================================================

def detect_vortices(dtheta, dr):
    vortices = []

    for i in range(WINDOW, len(dtheta)-WINDOW):
        local_dtheta = dtheta[i-WINDOW:i+WINDOW]
        local_dr = dr[i-WINDOW:i+WINDOW]

        mean_rot = np.mean(np.abs(local_dtheta))
        std_rot = np.std(local_dtheta)
        std_r = np.std(local_dr)

        # relaxed + real-system conditions
        if (
            mean_rot > ANGLE_THRESHOLD and
            std_rot > 0.5 and
            std_r < RADIUS_STABILITY
        ):
            vortices.append(i)

    return np.array(vortices, dtype=int)  # FIX!

# ============================================================
# CLUSTER VORTICES
# ============================================================

def cluster_vortices(vortex_idx, x, y, eps=0.05):
    clusters = []
    used = set()

    for i in vortex_idx:
        if i in used:
            continue

        cluster = [i]
        used.add(i)

        for j in vortex_idx:
            if j in used:
                continue

            dist = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)
            if dist < eps:
                cluster.append(j)
                used.add(j)

        clusters.append(cluster)

    return clusters

# ============================================================
# MAIN
# ============================================================

def main():
    print("="*70)
    print("VORTEX FIELD DETECTOR (mod 7)")
    print("="*70)

    primes = primes_upto(N_PRIMES * 20)[:N_PRIMES]

    T, residues = build_transition_matrix(primes)
    coords = spectral_projection(T)

    x, y, theta, r, dtheta, dr = project_flow(residues, coords)

    vortex_idx = detect_vortices(dtheta, dr)
    clusters = cluster_vortices(vortex_idx, x, y)

    print(f"\nDetected vortex points: {len(vortex_idx)}")
    print(f"Detected vortex clusters: {len(clusters)}")

    # ========================================================
    # PLOT
    # ========================================================

    plt.figure(figsize=(8,8))
    plt.scatter(x, y, s=2, alpha=0.3, label="trajectory")

    # plot vortices (SAFE)
    if len(vortex_idx) > 0:
        plt.scatter(x[vortex_idx], y[vortex_idx],
                    color='red', s=30, label="vortex points")

    # cluster centers
    for c in clusters:
        cx = np.mean(x[c])
        cy = np.mean(y[c])
        plt.scatter(cx, cy, color='yellow', s=100, edgecolor='black')

    plt.axhline(0, linewidth=0.5)
    plt.axvline(0, linewidth=0.5)

    plt.title("Detected Vortex Field (mod 7 spectral flow)")
    plt.legend()
    plt.show()

    # ========================================================
    # TIME / ROTATION VIEW
    # ========================================================

    plt.figure(figsize=(10,4))
    plt.plot(dtheta, label="dθ")

    if len(vortex_idx) > 0:
        plt.scatter(vortex_idx, dtheta[vortex_idx], color='red')

    plt.title("Angular velocity with vortex markers")
    plt.legend()
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
