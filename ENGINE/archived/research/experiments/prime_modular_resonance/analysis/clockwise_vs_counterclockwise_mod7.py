# clockwise_vs_counterclockwise_mod7.py

import numpy as np
from sympy import primerange
import matplotlib.pyplot as plt

# -------------------------
# CONFIG
# -------------------------
N = 20000
MOD = 7
STEPS = 600
WINDOW = 12          # local window for CW/CCW balance
EPS = 1e-12

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
# SPECTRAL MODE (complex plane)
# -------------------------
eigvals, eigvecs = np.linalg.eig(P.T)
idx = np.argsort(np.abs(eigvals))[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

lam = eigvals[1]
v = eigvecs[:, 1]

print("=" * 80)
print("CLOCKWISE VS COUNTERCLOCKWISE ANALYSIS (mod 7)")
print("=" * 80)
print(f"Using mode 1 eigenvalue: {lam}")

# -------------------------
# STATE COORDINATES IN COMPLEX PLANE
# -------------------------
state_coords = {}
for state in range(MOD):
    z = v[state]
    state_coords[state] = np.array([np.real(z), np.imag(z)])

coords = np.array(list(state_coords.values()))
scale = np.max(np.abs(coords))
if scale > 0:
    for s in state_coords:
        state_coords[s] = state_coords[s] / scale

traj = np.array([state_coords[s] for s in seq[:STEPS]])

# -------------------------
# ANGLE / RADIUS
# -------------------------
angles = np.arctan2(traj[:, 1], traj[:, 0])
radii = np.sqrt(traj[:, 0]**2 + traj[:, 1]**2)

# unwrap angles to get continuous rotation signal
angles_unwrapped = np.unwrap(angles)
dtheta = np.diff(angles_unwrapped)

# local direction:
# dtheta > 0 => CCW
# dtheta < 0 => CW
direction = np.sign(dtheta)

# -------------------------
# LOCAL CW / CCW BALANCE
# -------------------------
cw_ccw_balance = []
for i in range(len(direction)):
    start = max(0, i - WINDOW)
    end = min(len(direction), i + WINDOW + 1)
    local = direction[start:end]

    ccw = np.sum(local > 0)
    cw = np.sum(local < 0)

    # positive => CCW dominates, negative => CW dominates
    balance = (ccw - cw) / max(1, (ccw + cw))
    cw_ccw_balance.append(balance)

cw_ccw_balance = np.array(cw_ccw_balance)

# -------------------------
# VORTEX / SWITCH EVENTS
# detect sign changes in angular velocity
# -------------------------
switch_idx = []
for i in range(1, len(dtheta)):
    if np.sign(dtheta[i]) != np.sign(dtheta[i - 1]) and abs(dtheta[i] - dtheta[i - 1]) > 1e-6:
        switch_idx.append(i)

print(f"\nNumber of CW/CCW switch events: {len(switch_idx)}")
print("First switch indices:", switch_idx[:20])

# -------------------------
# LOCAL WINDING ESTIMATE
# cumulative rotation / 2pi over sliding windows
# -------------------------
winding = []
for i in range(len(angles_unwrapped)):
    start = max(0, i - WINDOW)
    end = min(len(angles_unwrapped), i + WINDOW + 1)
    local_rot = angles_unwrapped[end - 1] - angles_unwrapped[start]
    winding.append(local_rot / (2 * np.pi))

winding = np.array(winding)

# -------------------------
# PLOT 1: trajectory with switch points
# -------------------------
plt.figure(figsize=(8, 8))
plt.plot(traj[:, 0], traj[:, 1], alpha=0.5, linewidth=1)
plt.scatter(traj[:, 0], traj[:, 1], c=np.arange(len(traj)), cmap="viridis", s=18)

# mark state positions
for state, c in state_coords.items():
    plt.scatter(c[0], c[1], s=220)
    plt.text(c[0] + 0.03, c[1] + 0.03, str(state), fontsize=11)

# mark switch points
if len(switch_idx) > 0:
    switch_pts = traj[np.array(switch_idx)]
    plt.scatter(switch_pts[:, 0], switch_pts[:, 1], color="red", s=50, label="CW/CCW switch")

circle = plt.Circle((0, 0), 1.0, fill=False, linestyle="--", color="gray", alpha=0.6)
plt.gca().add_patch(circle)

plt.axhline(0, color="gray", linewidth=0.5)
plt.axvline(0, color="gray", linewidth=0.5)
plt.title("Prime Flow in Complex Plane with Rotation Switches")
plt.xlabel("Re(mode 1)")
plt.ylabel("Im(mode 1)")
plt.axis("equal")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 2: angular velocity and balance
# -------------------------
fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

axes[0].plot(dtheta, label="Angular velocity dθ")
axes[0].axhline(0, color="gray", linewidth=0.8)
axes[0].set_ylabel("dθ")
axes[0].set_title("Angular Velocity (CW vs CCW)")
axes[0].grid(alpha=0.3)
axes[0].legend()

axes[1].plot(cw_ccw_balance, label="Local CW/CCW balance")
axes[1].axhline(0, color="gray", linewidth=0.8)
axes[1].set_xlabel("Prime index")
axes[1].set_ylabel("Balance")
axes[1].set_title("Local Rotation Dominance (+CCW / -CW)")
axes[1].grid(alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.show()

# -------------------------
# PLOT 3: winding number estimate
# -------------------------
plt.figure(figsize=(10, 4))
plt.plot(winding)
plt.axhline(0, color="gray", linewidth=0.8)
plt.title("Local Winding Estimate")
plt.xlabel("Prime index")
plt.ylabel("Winding k")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# PLOT 4: histogram of angular velocity
# -------------------------
plt.figure(figsize=(8, 4))
plt.hist(dtheta, bins=40, alpha=0.8)
plt.axvline(0, color="gray", linewidth=0.8)
plt.title("Distribution of Angular Velocity")
plt.xlabel("dθ")
plt.ylabel("Count")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# -------------------------
# SUMMARY
# -------------------------
ccw_frac = np.mean(dtheta > 0)
cw_frac = np.mean(dtheta < 0)

print("\nRotation summary:")
print(f"CCW fraction: {ccw_frac:.4f}")
print(f"CW fraction:  {cw_frac:.4f}")
print(f"Mean dθ:      {np.mean(dtheta):.6f}")
print(f"Std dθ:       {np.std(dtheta):.6f}")


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
