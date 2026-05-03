import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations
from sklearn.cluster import KMeans

# =========================
# PARAMETERS
# =========================
MODS = [7, 11, 13, 17, 19, 23, 29, 31]
N_PRIMES = 5000

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

    # normalize rows
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums

    return T

# =========================
# DRIFT COMPUTATION
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
    # SIMILARITY MATRIX
    # =========================
    print("\n=== Pairwise Matrix Distance ===")
    dist_matrix = np.zeros((len(MODS), len(MODS)))

    for i, m1 in enumerate(MODS):
        for j, m2 in enumerate(MODS):
            if i == j:
                continue

            T1 = transition_matrices[m1]
            T2 = transition_matrices[m2]

            # resize smaller matrix into bigger space
            max_dim = max(T1.shape[0], T2.shape[0])
            A = np.zeros((max_dim, max_dim))
            B = np.zeros((max_dim, max_dim))

            A[:T1.shape[0], :T1.shape[1]] = T1
            B[:T2.shape[0], :T2.shape[1]] = T2

            dist = np.linalg.norm(A - B)
            dist_matrix[i, j] = dist

    # print pairs
    for (i, m1), (j, m2) in combinations(list(enumerate(MODS)), 2):
        print(f"{m1:2d} ↔ {m2:2d} : {dist_matrix[i,j]:.3f}")

    # =========================
    # CLUSTERING
    # =========================
    print("\n=== Clustering (K=3) ===")

    X = np.array(drift_values).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, random_state=0, n_init=10)
    labels = kmeans.fit_predict(X)

    for mod, label in zip(MODS, labels):
        print(f"mod {mod:2d} → cluster {label}")

    # =========================
    # PLOT DRIFT
    # =========================
    plt.figure(figsize=(6,4))
    plt.plot(MODS, drift_values, marker='o')
    plt.title("Drift Strength across Moduli")
    plt.xlabel("mod")
    plt.ylabel("drift strength")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # =========================
    # HEATMAP DISTANCE
    # =========================
    plt.figure(figsize=(6,5))
    plt.imshow(dist_matrix, cmap='viridis')
    plt.colorbar(label="matrix distance")
    plt.xticks(range(len(MODS)), MODS)
    plt.yticks(range(len(MODS)), MODS)
    plt.title("Transition Matrix Distance (mod comparison)")
    plt.tight_layout()
    plt.show()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
