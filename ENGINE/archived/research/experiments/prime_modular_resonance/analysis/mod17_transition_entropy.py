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
