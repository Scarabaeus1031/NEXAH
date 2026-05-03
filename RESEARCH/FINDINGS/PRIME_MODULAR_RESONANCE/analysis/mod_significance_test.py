import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PRIME GENERATOR
# -----------------------------
def generate_primes(n):
    primes = []
    x = 2
    while len(primes) < n:
        for p in primes:
            if x % p == 0:
                break
        else:
            primes.append(x)
        x += 1
    return np.array(primes)


# -----------------------------
# TRANSITION MATRIX
# -----------------------------
def transition_matrix(seq, mod):
    residues = seq % mod
    T = np.zeros((mod, mod))

    for i in range(len(residues) - 1):
        a, b = residues[i], residues[i + 1]
        T[a, b] += 1

    # normalize rows
    for i in range(mod):
        if T[i].sum() > 0:
            T[i] /= T[i].sum()

    return T


# -----------------------------
# METRICS
# -----------------------------
def spectral_gap(T):
    eigvals = np.linalg.eigvals(T)
    eigvals = np.sort(np.abs(eigvals))[::-1]
    return eigvals[0] - eigvals[1]


def drift_strength(T):
    mod = T.shape[0]
    angles = 2 * np.pi * np.arange(mod) / mod
    vectors = np.exp(1j * angles)

    drift = 0
    for i in range(mod):
        drift += np.sum(T[i] * vectors)

    return np.abs(drift)


def stationary_deviation(T):
    eigvals, eigvecs = np.linalg.eig(T.T)
    idx = np.argmax(np.real(eigvals))
    pi = np.real(eigvecs[:, idx])
    pi = pi / np.sum(pi)

    uniform = np.ones_like(pi) / len(pi)
    return np.linalg.norm(pi - uniform)


# -----------------------------
# RANDOM BASELINE SAMPLING
# -----------------------------
def random_baseline(primes, mod, runs=200):
    gaps = []
    drifts = []
    stats = []

    for _ in range(runs):
        shuffled = np.random.permutation(primes)
        T = transition_matrix(shuffled, mod)

        gaps.append(spectral_gap(T))
        drifts.append(drift_strength(T))
        stats.append(stationary_deviation(T))

    return {
        "gap": np.array(gaps),
        "drift": np.array(drifts),
        "stat": np.array(stats),
    }


# -----------------------------
# Z-SCORE
# -----------------------------
def z_score(value, baseline):
    mean = np.mean(baseline)
    std = np.std(baseline)
    return (value - mean) / (std + 1e-12)


# -----------------------------
# MAIN ANALYSIS
# -----------------------------
def analyze(mod_list, n_primes=2000, runs=200):
    primes = generate_primes(n_primes)

    results = []

    for mod in mod_list:
        print(f"\n=== MOD {mod} ===")

        # prime system
        T_prime = transition_matrix(primes, mod)

        gap_p = spectral_gap(T_prime)
        drift_p = drift_strength(T_prime)
        stat_p = stationary_deviation(T_prime)

        # random baseline
        baseline = random_baseline(primes, mod, runs=runs)

        z_gap = z_score(gap_p, baseline["gap"])
        z_drift = z_score(drift_p, baseline["drift"])
        z_stat = z_score(stat_p, baseline["stat"])

        print(f"PRIME gap   = {gap_p:.4f}  (Z={z_gap:.2f})")
        print(f"PRIME drift = {drift_p:.4f}  (Z={z_drift:.2f})")
        print(f"PRIME stat  = {stat_p:.4f}  (Z={z_stat:.2f})")

        results.append({
            "mod": mod,
            "z_gap": z_gap,
            "z_drift": z_drift,
            "z_stat": z_stat
        })

    return results


# -----------------------------
# PLOT RESULTS
# -----------------------------
def plot_results(results):
    mods = [r["mod"] for r in results]
    z_gap = [r["z_gap"] for r in results]
    z_drift = [r["z_drift"] for r in results]
    z_stat = [r["z_stat"] for r in results]

    plt.figure()
    plt.plot(mods, z_gap, marker='o', label="Z-gap")
    plt.plot(mods, z_drift, marker='o', label="Z-drift")
    plt.plot(mods, z_stat, marker='o', label="Z-stat")

    plt.axhline(0, linestyle="--")
    plt.title("Z-Score Significance vs Modulus")
    plt.xlabel("Modulus")
    plt.ylabel("Z-score")
    plt.legend()

    plt.savefig("output/plots/zscore_significance.png")
    print("[OK] saved: output/plots/zscore_significance.png")
    plt.close()


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    MOD_LIST = [7, 11, 13, 17, 19, 23, 29, 31, 39]

    results = analyze(MOD_LIST, n_primes=2000, runs=200)
    plot_results(results)
