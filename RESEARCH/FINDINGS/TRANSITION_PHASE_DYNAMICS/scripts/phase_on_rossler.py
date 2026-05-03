# phase_on_rossler.py

import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# OUTPUT PATH
# =========================

OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/phase"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# RÖSSLER SYSTEM
# =========================

def rossler(x, y, z, a=0.2, b=0.2, c=5.7):
    dx = -y - z
    dy = x + a*y
    dz = b + z*(x - c)
    return dx, dy, dz

# =========================
# SIMULATION
# =========================

dt = 0.01
steps = 20000

xs = np.zeros(steps)
ys = np.zeros(steps)
zs = np.zeros(steps)

# initial condition
xs[0], ys[0], zs[0] = (1.0, 0.0, 0.0)

for i in range(steps - 1):
    dx, dy, dz = rossler(xs[i], ys[i], zs[i])
    xs[i+1] = xs[i] + dx * dt
    ys[i+1] = ys[i] + dy * dt
    zs[i+1] = zs[i] + dz * dt

# =========================
# PHASE
# =========================

theta = np.arctan2(ys, xs)

# unwrap phase
theta_unwrapped = np.unwrap(theta)

# increments
dtheta = np.diff(theta_unwrapped)

# =========================
# STATS
# =========================

mean_dtheta = np.mean(dtheta)
std_dtheta = np.std(dtheta)

print("\n=== ROSSLER PHASE ANALYSIS ===")
print(f"Mean Δθ: {mean_dtheta:.6f}")
print(f"Std  Δθ: {std_dtheta:.6f}")

# =========================
# PLOT 1 — UNWRAPPED PHASE
# =========================

plt.figure(figsize=(10,4))
plt.plot(theta_unwrapped, linewidth=1)
plt.title("Unwrapped Phase — Rössler")
plt.xlabel("Time step")
plt.ylabel("θ (unwrapped)")
plt.tight_layout()

path1 = f"{OUTPUT_PATH}/rossler_phase_unwrapped.png"
plt.savefig(path1)
plt.close()

# =========================
# PLOT 2 — Δθ DISTRIBUTION
# =========================

plt.figure(figsize=(6,4))
plt.hist(dtheta, bins=100)
plt.title("Δθ Distribution — Rössler")
plt.xlabel("Δθ")
plt.ylabel("Frequency")
plt.tight_layout()

path2 = f"{OUTPUT_PATH}/rossler_phase_increment_hist.png"
plt.savefig(path2)
plt.close()

# =========================
# PLOT 3 — PHASE SPACE
# =========================

plt.figure(figsize=(5,5))
plt.scatter(xs, ys, s=1, alpha=0.3)
plt.title("Rössler Projection (x,y)")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()

path3 = f"{OUTPUT_PATH}/rossler_xy_projection.png"
plt.savefig(path3)
plt.close()

print(f"[OK] saved → {path1}")
print(f"[OK] saved → {path2}")
print(f"[OK] saved → {path3}")

# =========================
# INTERPRETATION
# =========================

print("\n=== INTERPRETATION ===")

print("""
If θ(t) grows smoothly:
→ continuous rotation

If Δθ is narrow / unimodal:
→ uniform transport

If mean Δθ ≠ 0:
→ directional drift exists
""")
