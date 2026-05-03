import numpy as np
import matplotlib.pyplot as plt

# =========================
# PARAMETERS
# =========================
MODS = [7, 11, 13, 17]
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
# DRIFT METRICS
# =========================
def compute_drift(mod, primes):
    residues = np.array([p % mod for p in primes])

    # differences mod m
    delta = (residues[1:] - residues[:-1]) % mod

    # center jumps to [-m/2, m/2]
    delta_centered = np.where(delta > mod/2, delta - mod, delta)

    # mean drift (linear)
    mean_drift = np.mean(delta_centered)

    # circular drift
    theta = 2 * np.pi * delta / mod
    complex_mean = np.mean(np.exp(1j * theta))
    drift_strength = np.abs(complex_mean)
    drift_angle = np.angle(complex_mean)

    return mean_drift, drift_strength, drift_angle

# =========================
# MAIN
# =========================
def main():
    primes = generate_primes(N_PRIMES)

    results = {}

    for mod in MODS:
        mean_drift, strength, angle = compute_drift(mod, primes)
        results[mod] = (mean_drift, strength, angle)

        print(f"\nmod {mod}")
        print(f"mean drift      = {mean_drift:.4f}")
        print(f"drift strength  = {strength:.4f}")
        print(f"drift angle     = {angle:.4f} rad")

    # =========================
    # PLOT
    # =========================
    mods = list(results.keys())
    strengths = [results[m][1] for m in mods]

    plt.figure(figsize=(6,4))
    plt.bar(mods, strengths)
    plt.title("Drift Strength across Moduli")
    plt.xlabel("mod")
    plt.ylabel("circular drift strength")

    plt.tight_layout()
    plt.savefig("drift_strength_comparison.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
