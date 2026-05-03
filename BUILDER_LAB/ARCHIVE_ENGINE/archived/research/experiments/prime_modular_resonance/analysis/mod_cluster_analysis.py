import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
from sklearn.cluster import KMeans
import os

# =========================
# PARAMETERS
# =========================
MODS = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
N_PRIMES = 6000

OUT_DIR = "BUILDER_LAB/ARCHIVE_ENGINE/archived/research/experiments/prime_modular_resonance/analysis/output/plots"
os.makedirs(OUT_DIR, exist_ok=True)

# =========================
# PRIME GENERATOR
# =========================
def generate_primes(n: int):
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

# =========================
# TRANSITION MATRIX
# =========================
def build_transition_matrix(mod: int, primes):
    residues = [p % mod for p in primes]
    pairs = list(zip(residues[:-1], residues[1:]))

    counts = Counter(pairs)
    T = np.zeros((mod, mod))

    for (i, j), c in counts.items():
        T[i, j] = c

    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums

    return T

# =========================
# DRIFT
# =========================
def compute_drift(mod: int, T):
    angles = np.array([2 * np.pi * i / mod for i in range(mod)])
    directions = np.exp(1j * angles)

    drift = 0 + 0j
    for i in range(mod):
        for j in range(mod):
            if T[i, j] > 0:
                delta = directions[j] / directions[i]
                drift += T[i, j] * delta

    return np.abs(drift)

# =========================
# MAIN
# =========================
def main():
    primes = generate_primes(N_PRIMES)

    transition_matrices = {}
    drift_values = []

    print("\n=== Drift Strength ===")
    for mod in MODS:
        T = build_transition_matrix(mod, primes)
        transition_matrices[mod] = T

        drift = compute_drift(mod, T)
        drift_values.append(drift)

        print(f"mod {mod:2d} → drift = {drift:.4f}")

    # =========================
    # DISTANCE MATRIX
    # =========================
    dist_matrix = np.zeros((len(MODS), len(MODS)))

    for i, m1 in enumerate(MODS):
        for j, m2 in enumerate(MODS):
            if i == j:
                continue

            T1 = transition_matrices[m1]
            T2 = transition_matrices[m2]

            max_dim = max(T1.shape[0], T2.shape[0])
            A = np.zeros((max_dim, max_dim))
            B = np.zeros((max_dim, max_dim))

            A[:T1.shape[0], :T1.shape[1]] = T1
            B[:T2.shape[0], :T2.shape[1]] = T2

            dist = np.linalg.norm(A - B)
            dist_matrix[i, j] = dist

    # =========================
    # CLUSTERING
    # =========================
    X = np.array(drift_values).reshape(-1, 1)

    kmeans = KMeans(n_clusters=4, random_state=0, n_init=10)
    labels = kmeans.fit_predict(X)

    print("\n=== Clusters ===")
    for mod, label in zip(MODS, labels):
        print(f"mod {mod:2d} → cluster {label}")

    # =========================
    # SORTED MATRIX (IMPORTANT)
    # =========================
    order = np.argsort(labels)
    sorted_mods = [MODS[i] for i in order]
    sorted_matrix = dist_matrix[order][:, order]

    # =========================
    # PLOT 1 — DRIFT SCALING
    # =========================
    plt.figure(figsize=(7,5))
    plt.plot(MODS, drift_values, marker='o')
    plt.title("Drift Strength across Moduli")
    plt.xlabel("mod")
    plt.ylabel("drift strength")
    plt.grid(True)
    plt.tight_layout()

    path = f"{OUT_DIR}/mod_drift_scaling.png"
    plt.savefig(path, dpi=300)
    print(f"[OK] saved: {path}")
    plt.close()

    # =========================
    # PLOT 2 — RAW DISTANCE
    # =========================
    plt.figure(figsize=(7,6))
    plt.imshow(dist_matrix, cmap='viridis')
    plt.colorbar(label="matrix distance")
    plt.xticks(range(len(MODS)), MODS)
    plt.yticks(range(len(MODS)), MODS)
    plt.title("Transition Matrix Distance (raw)")
    plt.tight_layout()

    path = f"{OUT_DIR}/mod_distance_matrix_raw.png"
    plt.savefig(path, dpi=300)
    print(f"[OK] saved: {path}")
    plt.close()

    # =========================
    # PLOT 3 — CLUSTERED MATRIX
    # =========================
    plt.figure(figsize=(7,6))
    plt.imshow(sorted_matrix, cmap='viridis')
    plt.colorbar(label="matrix distance")
    plt.xticks(range(len(sorted_mods)), sorted_mods, rotation=45)
    plt.yticks(range(len(sorted_mods)), sorted_mods)
    plt.title("Transition Matrix Distance (cluster-sorted)")
    plt.tight_layout()

    path = f"{OUT_DIR}/mod_distance_matrix_clustered.png"
    plt.savefig(path, dpi=300)
    print(f"[OK] saved: {path}")
    plt.close()

    # =========================
    # PLOT 4 — DRIFT BAR (clean)
    # =========================
    plt.figure(figsize=(7,5))
    plt.bar(MODS, drift_values)
    plt.title("Drift Strength across Moduli (Bar)")
    plt.xlabel("mod")
    plt.ylabel("drift strength")
    plt.tight_layout()

    path = f"{OUT_DIR}/mod_drift_bar.png"
    plt.savefig(path, dpi=300)
    print(f"[OK] saved: {path}")
    plt.close()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
