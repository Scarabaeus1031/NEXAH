import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt
from scipy.stats import entropy

# -------------------------
# CONFIG
# -------------------------
N = 10000
mod = 7
num_trials = 50

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = list(primerange(2, N))
prime_seq = [p % mod for p in primes]

# -------------------------
# HELPER: BUILD MATRIX
# -------------------------
def build_transition_matrix(seq, mod):
    matrix = np.zeros((mod, mod))

    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i + 1]] += 1

    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, where=row_sums != 0)

    return matrix

# -------------------------
# HELPER: ENTROPY
# -------------------------
def matrix_entropy(matrix):
    return np.mean([entropy(row + 1e-12) for row in matrix])

# -------------------------
# CONTROL SETS
# -------------------------

# 1. ODD RANDOM (nur ungerade Zahlen)
odd_numbers = [x for x in range(3, N, 2)]

# 2. PRIME-LIKE RANDOM (keine Vielfachen von 2,3,5,7)
def is_prime_like(x):
    return (x % 2 != 0 and x % 3 != 0 and x % 5 != 0 and x % 7 != 0)

prime_like_numbers = [x for x in range(11, N) if is_prime_like(x)]

# -------------------------
# PRIME BASELINE
# -------------------------
prime_matrix = build_transition_matrix(prime_seq, mod)
prime_entropy = matrix_entropy(prime_matrix)

print("Prime entropy:", prime_entropy)

# -------------------------
# RANDOM TESTS
# -------------------------
def run_trials(source_numbers, label):
    entropies = []

    for _ in range(num_trials):
        sample = np.random.choice(source_numbers, size=len(primes))
        seq = [x % mod for x in sample]

        matrix = build_transition_matrix(seq, mod)
        entropies.append(matrix_entropy(matrix))

    mean = np.mean(entropies)
    std = np.std(entropies)
    z = (prime_entropy - mean) / (std + 1e-12)

    print(f"\n[{label}]")
    print("Mean entropy:", mean)
    print("Std:", std)
    print("Z-score:", z)

    return entropies, mean

# -------------------------
# RUN
# -------------------------
odd_entropies, odd_mean = run_trials(odd_numbers, "Odd Random")
prime_like_entropies, pl_mean = run_trials(prime_like_numbers, "Prime-like Random")

# -------------------------
# PLOT
# -------------------------
plt.hist(odd_entropies, bins=15, alpha=0.5, label="Odd Random")
plt.hist(prime_like_entropies, bins=15, alpha=0.5, label="Prime-like Random")

plt.axvline(prime_entropy, linestyle="--", label="Prime", linewidth=2)

plt.title("Entropy Comparison (mod 7, corrected baseline)")
plt.legend()
plt.show()


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
