# mod_sweep_entropy.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# Helper Functions
# -------------------------

def compute_transition(seq, mod):
    matrix = np.zeros((mod, mod), dtype=float)

    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i+1]] += 1

    # Row normalization (Markov)
    row_sums = matrix.sum(axis=1, keepdims=True)

    matrix = np.divide(
        matrix,
        row_sums,
        out=np.zeros_like(matrix),
        where=row_sums != 0
    )

    return matrix


def entropy(matrix):
    p = matrix.flatten()
    p = p[p > 0]
    return -np.sum(p * np.log(p + 1e-12))  # numerically stable


def random_odd_sequence(n, mod):
    choices = [i for i in range(mod) if i % 2 == 1]
    return np.random.choice(choices, size=n)


def prime_like_sequence(n, mod):
    exclude = set()

    for i in range(mod):
        if i % 2 == 0 or i % 3 == 0 or i % 5 == 0 or i % 7 == 0:
            exclude.add(i)

    choices = [i for i in range(mod) if i not in exclude]

    if len(choices) == 0:
        choices = list(range(mod))  # fallback

    return np.random.choice(choices, size=n)


# -------------------------
# Main Experiment
# -------------------------

mods = [5, 7, 11, 13, 17, 19, 23]

primes = list(primerange(3, 20000))

results = []

for mod in mods:

    print(f"\n--- MOD {mod} ---")

    seq = [p % mod for p in primes]

    # Prime entropy
    prime_matrix = compute_transition(seq, mod)
    prime_entropy = entropy(prime_matrix)

    rand_entropies = []
    prime_like_entropies = []

    for _ in range(200):

        rseq = random_odd_sequence(len(seq), mod)
        rmat = compute_transition(rseq, mod)
        rand_entropies.append(entropy(rmat))

        plseq = prime_like_sequence(len(seq), mod)
        plmat = compute_transition(plseq, mod)
        prime_like_entropies.append(entropy(plmat))

    rand_mean = np.mean(rand_entropies)
    rand_std = np.std(rand_entropies)

    pl_mean = np.mean(prime_like_entropies)
    pl_std = np.std(prime_like_entropies)

    z_rand = (prime_entropy - rand_mean) / (rand_std + 1e-12)
    z_pl = (prime_entropy - pl_mean) / (pl_std + 1e-12)

    print(f"Prime entropy: {prime_entropy:.4f}")
    print(f"Random mean:   {rand_mean:.4f} | Z: {z_rand:.2f}")
    print(f"Prime-like:    {pl_mean:.4f} | Z: {z_pl:.2f}")

    results.append({
        "mod": mod,
        "prime": prime_entropy,
        "random": rand_mean,
        "prime_like": pl_mean
    })


# -------------------------
# Plot Results
# -------------------------

mods_plot = [r["mod"] for r in results]
prime_vals = [r["prime"] for r in results]
rand_vals = [r["random"] for r in results]
pl_vals = [r["prime_like"] for r in results]

plt.figure(figsize=(10,6))

plt.plot(mods_plot, prime_vals, marker='o', label="Prime")
plt.plot(mods_plot, rand_vals, marker='o', label="Random")
plt.plot(mods_plot, pl_vals, marker='o', label="Prime-like")

plt.title("Entropy vs Modulus (corrected)")
plt.xlabel("Modulus")
plt.ylabel("Entropy")
plt.legend()
plt.grid()

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
