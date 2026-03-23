# mod17_transition_entropy.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

def compute_transition(seq, mod):
    matrix = np.zeros((mod, mod))
    for i in range(len(seq)-1):
        matrix[seq[i], seq[i+1]] += 1
    matrix /= matrix.sum()
    return matrix

def entropy(matrix):
    p = matrix.flatten()
    p = p[p > 0]
    return -np.sum(p * np.log(p))

# primes
primes = list(primerange(3, 10000))
mod = 17
seq = [p % mod for p in primes]

# prime matrix
prime_matrix = compute_transition(seq, mod)
prime_entropy = entropy(prime_matrix)

# random baseline (odd only)
def random_odd_sequence(n):
    return np.random.choice([i for i in range(mod) if i % 2 == 1], size=n)

random_entropies = []
for _ in range(200):
    rseq = random_odd_sequence(len(seq))
    rmat = compute_transition(rseq, mod)
    random_entropies.append(entropy(rmat))

print("Prime entropy:", prime_entropy)
print("Random mean:", np.mean(random_entropies))
print("Z-score:", (prime_entropy - np.mean(random_entropies)) / np.std(random_entropies))

# plot
plt.imshow(prime_matrix)
plt.colorbar()
plt.title("Prime Transition Matrix (mod 17)")
plt.show()
