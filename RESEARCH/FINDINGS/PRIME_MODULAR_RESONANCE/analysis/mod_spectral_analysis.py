# mod_spectral_analysis.py

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os

# =========================
# PARAMETERS
# =========================
MOD_LIST = [7, 11, 13, 17, 19, 23, 29, 31]
N_PRIMES = 5000

OUTPUT_DIR = "output/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PRIME GENERATOR
# =========================
def generate_primes(n):
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
def build_transition_matrix(mod, primes):
    residues = [p % mod for p in primes]
    pairs = list(zip(residues[:-1], residues[1:]))

    counts = Counter(pairs)
    T = np.zeros((mod, mod))

    for (i, j), c in counts.items():
        T[i, j] = c

    # normalize rows
    for i in range(mod):
        row_sum = T[i].sum()
        if row_sum > 0:
            T[i] /= row_sum
        else:
            T[i] = np.ones(mod) / mod

    return T

# =========================
# SPECTRAL ANALYSIS
# =========================
def spectral_analysis(T):
    eigvals, eigvecs = np.linalg.eig(T.T)

    # sort by magnitude
    idx = np.argsort(-np.abs(eigvals))
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    # stationary distribution = eigenvector of eigenvalue ~1
    stationary = np.real(eigvecs[:, 0])
    stationary = stationary / stationary.sum()

    spectral_gap = 1 - np.abs(eigvals[1])

    return eigvals, stationary, spectral_gap

# =========================
# DRIFT MEASURE (ANGLE)
# =========================
def compute_drift(T):
    mod = T.shape[0]
    angles = np.array([2 * np.pi * i / mod for i in range(mod)])
    positions = np.column_stack((np.cos(angles), np.sin(angles)))

    drift = np.zeros(2)

    for i in range(mod):
        for j in range(mod):
            direction = positions[j] - positions[i]
            drift += T[i, j] * direction

    strength = np.linalg.norm(drift)
    angle = np.arctan2(drift[1], drift[0])

    return strength, angle

# =========================
# MAIN ANALYSIS
# =========================
def main():
    primes = generate_primes(N_PRIMES)

    drift_strengths = []
    spectral_gaps = []

    plt.figure(figsize=(8, 6))

    for mod in MOD_LIST:
        T = build_transition_matrix(mod, primes)

        eigvals, stationary, gap = spectral_analysis(T)
        drift_strength, drift_angle = compute_drift(T)

        drift_strengths.append(drift_strength)
        spectral_gaps.append(gap)

        print(f"\nmod {mod}")
        print(f"spectral gap   = {gap:.4f}")
        print(f"drift strength = {drift_strength:.4f}")
        print(f"drift angle    = {drift_angle:.4f}")

        # plot stationary distribution
        plt.plot(range(mod), stationary, label=f"mod {mod}")

    plt.title("Stationary Distributions")
    plt.xlabel("State")
    plt.ylabel("Probability")
    plt.legend()
    plt.grid()

    path1 = os.path.join(OUTPUT_DIR, "stationary_distributions.png")
    plt.savefig(path1, dpi=300)
    print(f"[OK] saved: {path1}")

    # =========================
    # DRIFT vs MOD
    # =========================
    plt.figure(figsize=(8, 6))
    plt.plot(MOD_LIST, drift_strengths, marker="o")
    plt.title("Drift Strength vs Modulus")
    plt.xlabel("Modulus")
    plt.ylabel("Drift Strength")
    plt.grid()

    path2 = os.path.join(OUTPUT_DIR, "drift_vs_mod.png")
    plt.savefig(path2, dpi=300)
    print(f"[OK] saved: {path2}")

    # =========================
    # SPECTRAL GAP vs MOD
    # =========================
    plt.figure(figsize=(8, 6))
    plt.plot(MOD_LIST, spectral_gaps, marker="o")
    plt.title("Spectral Gap vs Modulus")
    plt.xlabel("Modulus")
    plt.ylabel("Spectral Gap")
    plt.grid()

    path3 = os.path.join(OUTPUT_DIR, "spectral_gap_vs_mod.png")
    plt.savefig(path3, dpi=300)
    print(f"[OK] saved: {path3}")


if __name__ == "__main__":
    main()
