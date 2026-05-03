import numpy as np
import matplotlib.pyplot as plt

from sympy import primerange

# =========================
# PRIME GENERATOR
# =========================

def generate_primes(n):
    return np.array(list(primerange(2, 100000)))[:n]


# =========================
# TRANSITION MATRIX
# =========================

def build_transition_matrix(seq, mod):
    residues = seq % mod
    T = np.zeros((mod, mod))

    for i in range(len(residues)-1):
        T[residues[i], residues[i+1]] += 1

    # normalize rows
    for i in range(mod):
        if T[i].sum() > 0:
            T[i] /= T[i].sum()

    return T


# =========================
# METRICS
# =========================

def spectral_gap(T):
    eigvals = np.linalg.eigvals(T)
    eigvals = np.sort(np.abs(eigvals))[::-1]
    return eigvals[0] - eigvals[1]


def drift_strength(T):
    n = T.shape[0]
    angles = 2*np.pi*np.arange(n)/n
    vec = np.exp(1j*angles)

    drift = np.abs(np.sum(T @ vec - vec))
    return drift


def stationary_deviation(T):
    n = T.shape[0]
    pi = np.linalg.matrix_power(T, 100)[0]
    uniform = np.ones(n)/n
    return np.linalg.norm(pi - uniform)


# =========================
# NULL MODELS
# =========================

def random_sequence(n):
    return np.random.randint(0, 100000, size=n)


def shuffled_sequence(seq):
    return np.random.permutation(seq)


# =========================
# MAIN VALIDATION
# =========================

def run_validation(moduli=[7,11,13,17,19,23,29,31], n_primes=2000, n_runs=50):

    primes = generate_primes(n_primes)

    results = []

    for mod in moduli:

        T_prime = build_transition_matrix(primes, mod)

        gap_p = spectral_gap(T_prime)
        drift_p = drift_strength(T_prime)
        stat_p = stationary_deviation(T_prime)

        # RANDOM BASELINE
        gaps_r = []
        drifts_r = []
        stats_r = []

        for _ in range(n_runs):
            seq = random_sequence(n_primes)
            T = build_transition_matrix(seq, mod)

            gaps_r.append(spectral_gap(T))
            drifts_r.append(drift_strength(T))
            stats_r.append(stationary_deviation(T))

        # Z-scores
        z_gap = (gap_p - np.mean(gaps_r)) / np.std(gaps_r)
        z_drift = (drift_p - np.mean(drifts_r)) / np.std(drifts_r)
        z_stat = (stat_p - np.mean(stats_r)) / np.std(stats_r)

        results.append((mod, gap_p, drift_p, stat_p, z_gap, z_drift, z_stat))

        print(f"\nmod {mod}")
        print(f"gap   = {gap_p:.4f}  Z={z_gap:.2f}")
        print(f"drift = {drift_p:.4f}  Z={z_drift:.2f}")
        print(f"stat  = {stat_p:.4f}  Z={z_stat:.2f}")

    return results


# =========================
# PLOTTING
# =========================

def plot_results(results):

    mods = [r[0] for r in results]
    z_gap = [r[4] for r in results]
    z_drift = [r[5] for r in results]
    z_stat = [r[6] for r in results]

    plt.figure(figsize=(10,6))
    plt.plot(mods, z_gap, 'o-', label='Z-gap')
    plt.plot(mods, z_drift, 'o-', label='Z-drift')
    plt.plot(mods, z_stat, 'o-', label='Z-stat')

    plt.axhline(0, linestyle='--')
    plt.title("Validation Summary (Prime vs Random)")
    plt.xlabel("Modulus")
    plt.ylabel("Z-score")
    plt.legend()
    plt.grid()

    plt.savefig("output/plots/validation_summary.png")
    plt.show()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    results = run_validation()
    plot_results(results)
