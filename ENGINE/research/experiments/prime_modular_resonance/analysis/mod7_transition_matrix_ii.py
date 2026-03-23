import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt
from scipy.stats import entropy

# -------------------------
# CONFIG
# -------------------------
N = 10000
mod = 7
num_trials = 50  # wie oft random vergleichen

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = list(primerange(2, N))
prime_seq = [p % mod for p in primes]

# -------------------------
# FUNCTION: TRANSITION MATRIX
# -------------------------
def build_transition_matrix(seq, mod):
    matrix = np.zeros((mod, mod))

    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i + 1]] += 1

    # normalize rows
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, where=row_sums != 0)

    return matrix

# -------------------------
# ENTROPY FUNCTION
# -------------------------
def matrix_entropy(matrix):
    return np.mean([entropy(row + 1e-12) for row in matrix])

# -------------------------
# PRIME MATRIX
# -------------------------
prime_matrix = build_transition_matrix(prime_seq, mod)
prime_entropy = matrix_entropy(prime_matrix)

# -------------------------
# RANDOM BASELINE
# -------------------------
random_entropies = []

for _ in range(num_trials):
    random_numbers = np.random.randint(2, N, size=len(primes))
    random_seq = [r % mod for r in random_numbers]

    random_matrix = build_transition_matrix(random_seq, mod)
    random_entropies.append(matrix_entropy(random_matrix))

random_mean = np.mean(random_entropies)
random_std = np.std(random_entropies)

# -------------------------
# Z-SCORE
# -------------------------
z_score = (prime_entropy - random_mean) / (random_std + 1e-12)

# -------------------------
# OUTPUT
# -------------------------
print("Prime entropy:", prime_entropy)
print("Random mean entropy:", random_mean)
print("Random std:", random_std)
print("Z-score:", z_score)

# -------------------------
# PLOT DISTRIBUTION
# -------------------------
plt.hist(random_entropies, bins=15, alpha=0.7, label="Random")
plt.axvline(prime_entropy, linestyle="--", label="Prime")
plt.title("Entropy Comparison (mod 7)")
plt.legend()
plt.show()
