# mod_random_control_comparison.py

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os
import random

# =========================
# PARAMETERS
# =========================
MOD_LIST = [7, 11, 13, 17, 19, 23, 29, 31]
N_PRIMES = 5000
N_RANDOM = 5000

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
# RANDOM SEQUENCES
# =========================
def generate_random_sequence(n, max_val=100000):
    return np.random.randint(2, max_val, size=n)

def shuffle_sequence(seq):
    shuffled = list(seq)
    random.shuffle(shuffled)
    return shuffled

# =========================
# TRANSITION MATRIX
# =========================
def build_transition_matrix(mod, sequence):
    residues = [x % mod for x in sequence]
    pairs = list(zip(residues[:-1], residues[1:]))

    counts = Counter(pairs)
    T = np.zeros((mod, mod))

    for (i, j), c in counts.items():
        T[i, j] = c

    for i in range(mod):
        s = T[i].sum()
        if s > 0:
            T[i] /= s
        else:
            T[i] = np.ones(mod) / mod

    return T

# =========================
# METRICS
# =========================
def spectral_gap(T):
    eigvals = np.linalg.eigvals(T)
    eigvals = np.sort(np.abs(eigvals))[::-1]
    return 1 - eigvals[1]

def compute_drift(T):
    mod = T.shape[0]
    angles = np.array([2*np.pi*i/mod for i in range(mod)])
    pos = np.column_stack((np.cos(angles), np.sin(angles)))

    drift = np.zeros(2)

    for i in range(mod):
        for j in range(mod):
            drift += T[i,j] * (pos[j] - pos[i])

    return np.linalg.norm(drift)

def stationary_deviation(T):
    eigvals, eigvecs = np.linalg.eig(T.T)
    idx = np.argmin(np.abs(eigvals - 1))
    vec = np.real(eigvecs[:, idx])
    vec = np.abs(vec)
    vec /= vec.sum()

    uniform = np.ones(len(vec)) / len(vec)
    return np.linalg.norm(vec - uniform)

# =========================
# MAIN
# =========================
def main():
    primes = generate_primes(N_PRIMES)
    shuffled_primes = shuffle_sequence(primes)
    random_seq = generate_random_sequence(N_RANDOM)

    results = {
        "prime": {"drift": [], "gap": [], "stat": []},
        "shuffled": {"drift": [], "gap": [], "stat": []},
        "random": {"drift": [], "gap": [], "stat": []},
    }

    print("\n=== COMPARISON ANALYSIS ===")

    for mod in MOD_LIST:

        # PRIME
        T_prime = build_transition_matrix(mod, primes)
        d_p = compute_drift(T_prime)
        g_p = spectral_gap(T_prime)
        s_p = stationary_deviation(T_prime)

        # SHUFFLED
        T_shuf = build_transition_matrix(mod, shuffled_primes)
        d_s = compute_drift(T_shuf)
        g_s = spectral_gap(T_shuf)
        s_s = stationary_deviation(T_shuf)

        # RANDOM
        T_rand = build_transition_matrix(mod, random_seq)
        d_r = compute_drift(T_rand)
        g_r = spectral_gap(T_rand)
        s_r = stationary_deviation(T_rand)

        results["prime"]["drift"].append(d_p)
        results["prime"]["gap"].append(g_p)
        results["prime"]["stat"].append(s_p)

        results["shuffled"]["drift"].append(d_s)
        results["shuffled"]["gap"].append(g_s)
        results["shuffled"]["stat"].append(s_s)

        results["random"]["drift"].append(d_r)
        results["random"]["gap"].append(g_r)
        results["random"]["stat"].append(s_r)

        print(f"\nmod {mod}")
        print(f"PRIME    drift={d_p:.4f} gap={g_p:.4f} stat_dev={s_p:.4f}")
        print(f"SHUFFLED drift={d_s:.4f} gap={g_s:.4f} stat_dev={s_s:.4f}")
        print(f"RANDOM   drift={d_r:.4f} gap={g_r:.4f} stat_dev={s_r:.4f}")

    # =========================
    # PLOTS
    # =========================

    def plot_metric(metric_name, ylabel, filename):
        plt.figure(figsize=(8,6))

        plt.plot(MOD_LIST, results["prime"][metric_name], marker="o", label="prime")
        plt.plot(MOD_LIST, results["shuffled"][metric_name], marker="o", label="shuffled")
        plt.plot(MOD_LIST, results["random"][metric_name], marker="o", label="random")

        plt.xlabel("mod")
        plt.ylabel(ylabel)
        plt.title(f"{ylabel} Comparison")
        plt.legend()
        plt.grid()

        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=300)
        print(f"[OK] saved: {path}")

    plot_metric("drift", "Drift Strength", "comparison_drift.png")
    plot_metric("gap", "Spectral Gap", "comparison_gap.png")
    plot_metric("stat", "Stationary Deviation", "comparison_stationary.png")


if __name__ == "__main__":
    main()
