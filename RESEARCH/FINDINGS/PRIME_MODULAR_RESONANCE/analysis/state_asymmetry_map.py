import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================

MODS = [7, 11, 13, 17, 19, 23, 29, 31]
N_PRIMES = 20000
RANDOM_RUNS = 20

OUTPUT_PATH = "output/plots"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# PRIME GENERATOR
# =========================

def generate_primes(n):
    primes = list(primerange(2, 300000))
    return np.array(primes[:n])

# =========================
# TRANSITION MATRIX
# =========================

def transition_matrix(sequence, mod):
    residues = sequence % mod
    T = np.zeros((mod, mod))

    for i in range(len(residues) - 1):
        a = residues[i]
        b = residues[i+1]
        T[a, b] += 1

    # normalize rows
    row_sums = T.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    T = T / row_sums

    return T

# =========================
# ASYMMETRY MEASURE
# =========================

def asymmetry_map(T):
    return np.abs(T - T.T)

# =========================
# RANDOM BASELINE
# =========================

def random_baseline(mod, length, runs):
    maps = []
    for _ in range(runs):
        seq = np.random.randint(0, mod, size=length)
        T = transition_matrix(seq, mod)
        maps.append(asymmetry_map(T))
    return np.mean(maps, axis=0)

# =========================
# MAIN
# =========================

primes = generate_primes(N_PRIMES)

for mod in MODS:

    print(f"\n=== MOD {mod} ===")

    # prime transition matrix
    T_prime = transition_matrix(primes, mod)
    A_prime = asymmetry_map(T_prime)

    # random baseline
    A_rand = random_baseline(mod, len(primes), RANDOM_RUNS)

    # difference
    A_diff = A_prime - A_rand

    # =========================
    # PLOTS
    # =========================

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    im0 = axes[0].imshow(A_prime, cmap='viridis')
    axes[0].set_title(f"Prime Asymmetry (mod {mod})")

    im1 = axes[1].imshow(A_rand, cmap='viridis')
    axes[1].set_title("Random Baseline")

    im2 = axes[2].imshow(A_diff, cmap='coolwarm')
    axes[2].set_title("Difference (Prime - Random)")

    for ax in axes:
        ax.set_xlabel("to state")
        ax.set_ylabel("from state")

    fig.colorbar(im0, ax=axes[0])
    fig.colorbar(im1, ax=axes[1])
    fig.colorbar(im2, ax=axes[2])

    plt.tight_layout()

    save_path = f"{OUTPUT_PATH}/asymmetry_map_mod{mod}.png"
    plt.savefig(save_path)
    plt.close()

    print(f"[OK] saved → {save_path}")

    # =========================
    # METRIC SUMMARY
    # =========================

    mean_asym_prime = np.mean(A_prime)
    mean_asym_rand  = np.mean(A_rand)

    print(f"mean asymmetry (prime): {mean_asym_prime:.5f}")
    print(f"mean asymmetry (rand) : {mean_asym_rand:.5f}")
    print(f"excess asymmetry      : {(mean_asym_prime - mean_asym_rand):.5f}")

# =========================
# DONE
# =========================

print("\n=== DONE ===")
