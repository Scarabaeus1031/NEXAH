import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================

np.random.seed(42)

mods = np.array([7,11,13,17,19,23,29,31])
N_PRIMES = 10000
N_RANDOM = 20

OUTPUT_PATH = "output/plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# PRIME GENERATION
# =========================

def generate_primes(n):
    return np.array(list(primerange(2, 200000))[:n])

# =========================
# TRANSITION MATRIX
# =========================

def build_transition_matrix(seq, mod):
    residues = seq % mod
    T = np.zeros((mod, mod))

    for i in range(len(residues)-1):
        a = residues[i]
        b = residues[i+1]
        T[a, b] += 1

    row_sums = T.sum(axis=1, keepdims=True) + 1e-12
    T = T / row_sums

    return T, residues

# =========================
# METRICS
# =========================

# 1. Asymmetry
def compute_asymmetry(T):
    return np.mean(np.abs(T - T.T))

# 2. Entropy
def compute_entropy(T):
    ent = []
    for row in T:
        p = row[row > 0]
        if len(p) == 0:
            continue
        ent.append(-np.sum(p * np.log(p)))
    return np.mean(ent)

# 3. Cycle density (length-3 loops)
def compute_cycle_density(residues):
    count = 0
    total = len(residues) - 3

    for i in range(total):
        if residues[i] == residues[i+3]:
            count += 1

    return count / (total + 1e-9)

# =========================
# RANDOM BASELINE
# =========================

def compute_random_metrics(length, mod):
    asym_list = []
    ent_list = []
    cyc_list = []

    for _ in range(N_RANDOM):
        seq = np.random.randint(0, mod, size=length)
        T, res = build_transition_matrix(seq, mod)

        asym_list.append(compute_asymmetry(T))
        ent_list.append(compute_entropy(T))
        cyc_list.append(compute_cycle_density(res))

    return (
        np.mean(asym_list), np.std(asym_list),
        np.mean(ent_list),  np.std(ent_list),
        np.mean(cyc_list),  np.std(cyc_list)
    )

# =========================
# MAIN
# =========================

primes = generate_primes(N_PRIMES)

asym_prime = []
entropy_prime = []
cycle_prime = []

asym_rand_mean = []
entropy_rand_mean = []
cycle_rand_mean = []

asym_rand_std = []
entropy_rand_std = []
cycle_rand_std = []

print("\n=== LOCAL STRUCTURE DETECTOR ===\n")

for m in mods:

    T, residues = build_transition_matrix(primes, m)

    # PRIME METRICS
    a = compute_asymmetry(T)
    e = compute_entropy(T)
    c = compute_cycle_density(residues)

    # RANDOM BASELINE
    ar, ar_std, er, er_std, cr, cr_std = compute_random_metrics(len(residues), m)

    asym_prime.append(a)
    entropy_prime.append(e)
    cycle_prime.append(c)

    asym_rand_mean.append(ar)
    entropy_rand_mean.append(er)
    cycle_rand_mean.append(cr)

    asym_rand_std.append(ar_std)
    entropy_rand_std.append(er_std)
    cycle_rand_std.append(cr_std)

    print(f"mod {m}")
    print(f" asymmetry: {a:.5f}  (rand {ar:.5f} ± {ar_std:.5f})")
    print(f" entropy:   {e:.5f}  (rand {er:.5f} ± {er_std:.5f})")
    print(f" cycles:    {c:.5f}  (rand {cr:.5f} ± {cr_std:.5f})")
    print()

# =========================
# TO ARRAY
# =========================

asym_prime = np.array(asym_prime)
entropy_prime = np.array(entropy_prime)
cycle_prime = np.array(cycle_prime)

asym_rand_mean = np.array(asym_rand_mean)
entropy_rand_mean = np.array(entropy_rand_mean)
cycle_rand_mean = np.array(cycle_rand_mean)

asym_rand_std = np.array(asym_rand_std)
entropy_rand_std = np.array(entropy_rand_std)
cycle_rand_std = np.array(cycle_rand_std)

# =========================
# PLOT
# =========================

plt.figure(figsize=(10,6))

def plot_metric(x, prime, rand, std, label):
    plt.plot(x, prime, 'o-', label=f'{label} (prime)')
    plt.plot(x, rand, '--', label=f'{label} (random)')
    plt.fill_between(x, rand-std, rand+std, alpha=0.2)

plot_metric(mods, asym_prime, asym_rand_mean, asym_rand_std, "asymmetry")
plot_metric(mods, entropy_prime, entropy_rand_mean, entropy_rand_std, "entropy")
plot_metric(mods, cycle_prime, cycle_rand_mean, cycle_rand_std, "cycles")

plt.title("Local Structure vs Random")
plt.xlabel("Modulus")
plt.ylabel("Metric")
plt.legend()
plt.grid()

plt.savefig(f"{OUTPUT_PATH}/local_structure_detector.png")
plt.show()

# =========================
# SUMMARY
# =========================

print("\n=== INTERPRETATION ===")
print("""
If prime curves deviate from random bands:

→ local structure exists

If they overlap:

→ structure likely illusion from sampling

Key:

asymmetry → directionality
entropy   → order vs randomness
cycles    → recurrence / loops
""")
