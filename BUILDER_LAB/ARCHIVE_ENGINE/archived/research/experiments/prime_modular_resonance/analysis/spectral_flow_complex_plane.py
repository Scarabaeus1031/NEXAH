# spectral_flow_complex_plane.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 20000
MOD = 7
STEPS = 400   # how many prime states to project

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

print("=" * 80)
print("SPECTRAL FLOW IN COMPLEX PLANE (mod 7)")
print("=" * 80)
for i in range(min(7, len(eigvals))):
    print(f"Mode {i}: eigenvalue = {eigvals[i]}")

# first complex pair after stationary mode
lam = eigvals[1]
v = eigvecs[:, 1]

print(f"\nUsing mode 1: λ = {lam}")

# -------------------------
# STATE COORDINATES IN COMPLEX PLANE
# -------------------------
state_coords = {}
for state in range(MOD):
    z = v[state]
    state_coords[state] = np.array([np.real(z), np.imag(z)])

# normalize for plotting
coords = np.array(list(state_coords.values()))
scale = np.max(np.abs(coords))
if scale > 0:
    for s in state_coords:
        state_coords[s] = state_coords[s] / scale

# trajectory through residue states
traj = np.array([state_coords[s] for s in seq[:STEPS]])

# -------------------------
# PLOT 1: residue states in complex plane
# -------------------------
plt.figure(figsize=(7, 7))
for state, c in state_coords.items():
    plt.scatter(c[0], c[1], s=220)
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=12)

# unit circle
circle = plt.Circle((0, 0), 1.0, fill=False, linestyle="--", color="gray", alpha=0.6)
plt.gca().add_patch(circle)

plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.title("Residue States in Complex Spectral Plane (mod 7)")
plt.xlabel("Re(mode 1)")
plt.ylabel("Im(mode 1)")
plt.axis("equal")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: trajectory in complex plane
# -------------------------
plt.figure(figsize=(8, 8))
plt.plot(traj[:, 0], traj[:, 1], alpha=0.6, linewidth=1)
plt.scatter(traj[:, 0], traj[:, 1], c=np.arange(len(traj)), cmap="viridis", s=16)

plt.scatter(traj[0, 0], traj[0, 1], color="red", s=100, label="start")
plt.scatter(traj[-1, 0], traj[-1, 1], color="black", s=100, label="end")

for state, c in state_coords.items():
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=11)

circle = plt.Circle((0, 0), 1.0, fill=False, linestyle="--", color="gray", alpha=0.6)
plt.gca().add_patch(circle)

plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.title("Prime Flow Trajectory in Complex Spectral Plane")
plt.xlabel("Re(mode 1)")
plt.ylabel("Im(mode 1)")
plt.legend()
plt.axis("equal")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 3: dominant transitions as arrows
# -------------------------
plt.figure(figsize=(8, 8))

for state, c in state_coords.items():
    plt.scatter(c[0], c[1], s=220)
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=12)

for i in range(MOD):
    for j in range(MOD):
        w = P[i, j]
        if w > 0.12:
            x1, y1 = state_coords[i]
            x2, y2 = state_coords[j]
            dx, dy = x2 - x1, y2 - y1
            plt.arrow(
                x1, y1,
                dx * 0.85, dy * 0.85,
                head_width=0.03,
                head_length=0.05,
                length_includes_head=True,
                alpha=min(1.0, w * 2.5)
            )

circle = plt.Circle((0, 0), 1.0, fill=False, linestyle="--", color="gray", alpha=0.6)
plt.gca().add_patch(circle)

plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.title("Dominant Prime Transitions in Complex Spectral Plane")
plt.xlabel("Re(mode 1)")
plt.ylabel("Im(mode 1)")
plt.axis("equal")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 4: angle over time
# -------------------------
angles = np.arctan2(traj[:, 1], traj[:, 0])
radii = np.sqrt(traj[:, 0]**2 + traj[:, 1]**2)

plt.figure(figsize=(10, 5))
plt.plot(angles, label="angle")
plt.plot(radii, label="radius")
plt.title("Angle / Radius over Time in Complex Spectral Plane")
plt.xlabel("Prime index")
plt.ylabel("Value")
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
