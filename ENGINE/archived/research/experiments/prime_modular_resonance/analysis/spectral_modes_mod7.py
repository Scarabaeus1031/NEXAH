# spectral_modes_mod7.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 20000
MOD = 7

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = list(primerange(3, N))
seq = [p % MOD for p in primes]

# -------------------------
# BUILD TRANSITION MATRIX
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

P = build_transition_matrix(seq, MOD)

# -------------------------
# SPECTRAL DECOMPOSITION
# right eigenvectors of P^T are natural for stationary / modes
# -------------------------
eigvals, eigvecs = np.linalg.eig(P.T)

# sort by magnitude of eigenvalue (descending)
idx = np.argsort(np.abs(eigvals))[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

print("=" * 80)
print("SPECTRAL MODES OF PRIME mod-7 TRANSITION MATRIX")
print("=" * 80)

for i in range(min(7, len(eigvals))):
    print(f"Mode {i}: eigenvalue = {eigvals[i]}")

# -------------------------
# STATIONARY MODE
# -------------------------
stationary = np.real(eigvecs[:, 0])
stationary = np.abs(stationary)
stationary = stationary / stationary.sum()

print("\nStationary mode:")
for i, val in enumerate(stationary):
    print(f"State {i}: {val:.6f}")

# -------------------------
# SECONDARY MODES
# normalize for visualization
# -------------------------
modes_to_plot = min(4, eigvecs.shape[1])

mode_vectors = []
for k in range(modes_to_plot):
    v = np.real(eigvecs[:, k])
    if np.max(np.abs(v)) > 0:
        v = v / np.max(np.abs(v))
    mode_vectors.append(v)

# -------------------------
# PLOT 1: Eigenvalues in complex plane
# -------------------------
plt.figure(figsize=(6, 6))
plt.scatter(np.real(eigvals), np.imag(eigvals), s=80)
unit_circle = plt.Circle((0, 0), 1.0, color='gray', fill=False, linestyle='--')
plt.gca().add_patch(unit_circle)

for i, lam in enumerate(eigvals[:7]):
    plt.text(np.real(lam) + 0.02, np.imag(lam), str(i), fontsize=9)

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.xlabel("Re(λ)")
plt.ylabel("Im(λ)")
plt.title("Eigenvalues of Prime mod-7 Transition Matrix")
plt.axis("equal")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: Stationary distribution
# -------------------------
plt.figure(figsize=(8, 4))
plt.bar(range(MOD), stationary)
plt.xlabel("State")
plt.ylabel("Weight")
plt.title("Stationary Spectral Mode (mod 7)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 3: Leading mode shapes
# -------------------------
fig, axes = plt.subplots(modes_to_plot, 1, figsize=(8, 2.5 * modes_to_plot), sharex=True)

if modes_to_plot == 1:
    axes = [axes]

for k, ax in enumerate(axes):
    ax.bar(range(MOD), mode_vectors[k])
    ax.set_ylabel(f"Mode {k}")
    ax.set_title(f"Mode {k} | λ = {eigvals[k]:.4f}")
    ax.grid(axis="y", alpha=0.3)

axes[-1].set_xlabel("State")
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 4: Heatmap of mode vectors
# -------------------------
mode_matrix = np.array(mode_vectors)

plt.figure(figsize=(8, 4))
plt.imshow(mode_matrix, aspect='auto', cmap='coolwarm')
plt.colorbar(label="Normalized mode amplitude")
plt.xlabel("State")
plt.ylabel("Mode index")
plt.title("Spectral Mode Patterns (mod 7)")
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
