import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 10000
mod = 7

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = list(primerange(2, N))
prime_seq = [p % mod for p in primes]

# -------------------------
# RANDOM SEQUENCE (CONTROL)
# -------------------------
random_numbers = np.random.randint(2, N, size=len(primes))
random_seq = [r % mod for r in random_numbers]

# -------------------------
# FUNCTION: TRANSITION MATRIX
# -------------------------
def build_transition_matrix(seq, mod):
    matrix = np.zeros((mod, mod))

    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i + 1]] += 1

    # normalize rows (important!)
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, where=row_sums != 0)

    return matrix

# -------------------------
# BUILD MATRICES
# -------------------------
prime_matrix = build_transition_matrix(prime_seq, mod)
random_matrix = build_transition_matrix(random_seq, mod)

# -------------------------
# DIFFERENCE MATRIX
# -------------------------
diff_matrix = prime_matrix - random_matrix

# -------------------------
# PLOTS
# -------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].imshow(prime_matrix)
axes[0].set_title("Prime Transition (mod 7)")

axes[1].imshow(random_matrix)
axes[1].set_title("Random Transition (mod 7)")

axes[2].imshow(diff_matrix)
axes[2].set_title("Difference (Prime - Random)")

for ax in axes:
    ax.set_xlabel("Next State")
    ax.set_ylabel("Current State")

plt.tight_layout()
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
