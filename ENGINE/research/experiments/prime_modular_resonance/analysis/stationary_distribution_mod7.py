# stationary_distribution_mod7.py

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
primes = list(primerange(3, N))
seq = [p % mod for p in primes]

# -------------------------
# BUILD ROW-STOCHASTIC TRANSITION MATRIX
# -------------------------
def build_transition_matrix(seq, mod):
    matrix = np.zeros((mod, mod), dtype=float)

    for i in range(len(seq) - 1):
        matrix[seq[i], seq[i + 1]] += 1

    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(
        matrix,
        row_sums,
        out=np.zeros_like(matrix),
        where=row_sums != 0
    )
    return matrix

P = build_transition_matrix(seq, mod)

# -------------------------
# STATIONARY DISTRIBUTION
# Solve pi P = pi
# -------------------------
eigvals, eigvecs = np.linalg.eig(P.T)

# eigenvalue closest to 1
idx = np.argmin(np.abs(eigvals - 1.0))
pi = np.real(eigvecs[:, idx])

# normalize to probability vector
pi = np.abs(pi)
pi = pi / pi.sum()

print("Transition matrix P:")
print(np.round(P, 4))

print("\nStationary distribution pi:")
for i, val in enumerate(pi):
    print(f"State {i}: {val:.6f}")

print("\nCheck pi @ P:")
print(np.round(pi @ P, 6))

# -------------------------
# EMPIRICAL VISIT FREQUENCY
# -------------------------
counts = np.bincount(seq, minlength=mod).astype(float)
empirical = counts / counts.sum()

print("\nEmpirical residue frequency:")
for i, val in enumerate(empirical):
    print(f"State {i}: {val:.6f}")

# -------------------------
# PLOT
# -------------------------
x = np.arange(mod)
width = 0.38

plt.figure(figsize=(10, 5))
plt.bar(x - width/2, pi, width=width, label="Stationary distribution")
plt.bar(x + width/2, empirical, width=width, label="Empirical residue frequency")

plt.xticks(x)
plt.xlabel("Residue state (mod 7)")
plt.ylabel("Probability")
plt.title("Stationary Distribution vs Empirical Frequency (mod 7)")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# OPTIONAL: HEATMAP
# -------------------------
plt.figure(figsize=(6, 5))
plt.imshow(P, cmap="viridis")
plt.colorbar(label="Transition probability")
plt.xlabel("Next state")
plt.ylabel("Current state")
plt.title("Prime Transition Matrix (mod 7)")
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
