# spectral_flow_projection.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 20000
MOD = 7
STEPS = 300   # how many prime states to project

# -------------------------
# PRIME SEQUENCE
# -------------------------
primes = list(primerange(3, N))
seq = np.array([p % MOD for p in primes], dtype=int)

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
# -------------------------
eigvals, eigvecs = np.linalg.eig(P.T)

# sort by magnitude descending
idx = np.argsort(np.abs(eigvals))[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

# stationary mode = 0
# first complex pair is usually 1 and 2
v1 = eigvecs[:, 1]
v2 = eigvecs[:, 2]

print("=" * 80)
print("SPECTRAL FLOW PROJECTION (mod 7)")
print("=" * 80)
print(f"Mode 1 eigenvalue: {eigvals[1]}")
print(f"Mode 2 eigenvalue: {eigvals[2]}")

# -------------------------
# PROJECT STATES INTO 2D SPECTRAL SPACE
# Each residue state k gets coordinates from eigenmodes
# -------------------------
state_coords = {}

for state in range(MOD):
    x = np.real(v1[state])
    y = np.real(v2[state])
    state_coords[state] = np.array([x, y])

# normalize for nicer plotting
coords_array = np.array(list(state_coords.values()))
max_abs = np.max(np.abs(coords_array))
if max_abs > 0:
    for state in state_coords:
        state_coords[state] = state_coords[state] / max_abs

# -------------------------
# TRAJECTORY OF PRIME FLOW
# -------------------------
traj = np.array([state_coords[s] for s in seq[:STEPS]])

# -------------------------
# PLOT 1: state positions
# -------------------------
plt.figure(figsize=(7, 7))

for state, c in state_coords.items():
    plt.scatter(c[0], c[1], s=220)
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=12)

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.title("Residue States in Spectral Space (mod 7)")
plt.xlabel("Mode 1 projection")
plt.ylabel("Mode 2 projection")
plt.grid(alpha=0.3)
plt.axis("equal")
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: spectral trajectory
# -------------------------
plt.figure(figsize=(8, 8))

plt.plot(traj[:, 0], traj[:, 1], alpha=0.65, linewidth=1)
plt.scatter(traj[:, 0], traj[:, 1], c=np.arange(len(traj)), cmap="viridis", s=18)

# mark start / end
plt.scatter(traj[0, 0], traj[0, 1], color="red", s=100, label="start")
plt.scatter(traj[-1, 0], traj[-1, 1], color="black", s=100, label="end")

for state, c in state_coords.items():
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=11)

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.title("Prime Flow Trajectory in Spectral Space")
plt.xlabel("Mode 1 projection")
plt.ylabel("Mode 2 projection")
plt.legend()
plt.grid(alpha=0.3)
plt.axis("equal")
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 3: arrows for transitions between residue states
# -------------------------
plt.figure(figsize=(8, 8))

for state, c in state_coords.items():
    plt.scatter(c[0], c[1], s=220)
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=12)

# draw arrows from transition probabilities
for i in range(MOD):
    for j in range(MOD):
        w = P[i, j]
        if w > 0.12:  # threshold to keep plot readable
            x1, y1 = state_coords[i]
            x2, y2 = state_coords[j]
            dx, dy = x2 - x1, y2 - y1

            plt.arrow(
                x1, y1, dx * 0.85, dy * 0.85,
                head_width=0.03,
                head_length=0.05,
                alpha=min(1.0, w * 2.5),
                length_includes_head=True
            )

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.title("Dominant Prime Transitions in Spectral Space")
plt.xlabel("Mode 1 projection")
plt.ylabel("Mode 2 projection")
plt.grid(alpha=0.3)
plt.axis("equal")
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 4: time traces of spectral coordinates
# -------------------------
plt.figure(figsize=(10, 5))
plt.plot(traj[:, 0], label="Mode 1 coordinate")
plt.plot(traj[:, 1], label="Mode 2 coordinate")
plt.title("Spectral Coordinates Over Time")
plt.xlabel("Prime index")
plt.ylabel("Projection value")
plt.legend()
plt.grid(alpha=0.3)
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
