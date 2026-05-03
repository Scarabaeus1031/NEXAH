# phase_on_halvorsen.py

import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# OUTPUT PATH
# =========================

OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/phase"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# HALVORSEN SYSTEM
# =========================

def halvorsen(x, y, z, a=1.4):
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
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
    dx, dy, dz = halvorsen(xs[i], ys[i], zs[i])
    xs[i+1] = xs[i] + dx * dt
    ys[i+1] = ys[i] + dy * dt
    zs[i+1] = zs[i] + dz * dt

# =========================
# PHASE
# =========================

theta = np.arctan2(ys, xs)

# unwrap
theta_unwrapped = np.unwrap(theta)

# increments
dtheta = np.diff(theta_unwrapped)

# =========================
# STATS
# =========================

mean_dtheta = np.mean(dtheta)
std_dtheta = np.std(dtheta)

print("\n=== HALVORSEN PHASE ANALYSIS ===")
print(f"Mean Δθ: {mean_dtheta:.6f}")
print(f"Std  Δθ: {std_dtheta:.6f}")

# =========================
# PLOT 1 — UNWRAPPED PHASE
# =========================

plt.figure(figsize=(10,4))
plt.plot(theta_unwrapped, linewidth=1)
plt.title("Unwrapped Phase — Halvorsen")
plt.xlabel("Time step")
plt.ylabel("θ (unwrapped)")
plt.tight_layout()

path1 = f"{OUTPUT_PATH}/halvorsen_phase_unwrapped.png"
plt.savefig(path1)
plt.close()

# =========================
# PLOT 2 — Δθ DISTRIBUTION
# =========================

plt.figure(figsize=(6,4))
plt.hist(dtheta, bins=120)
plt.title("Δθ Distribution — Halvorsen")
plt.xlabel("Δθ")
plt.ylabel("Frequency")
plt.tight_layout()

path2 = f"{OUTPUT_PATH}/halvorsen_phase_increment_hist.png"
plt.savefig(path2)
plt.close()

# =========================
# PLOT 3 — PHASE SPACE
# =========================

plt.figure(figsize=(5,5))
plt.scatter(xs, ys, s=1, alpha=0.3)
plt.title("Halvorsen Projection (x,y)")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()

path3 = f"{OUTPUT_PATH}/halvorsen_xy_projection.png"
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
If θ(t) is irregular:
→ fragmented structure

If Δθ is broad / multi-peaked:
→ multiple competing transitions

If mean Δθ ≠ 0:
→ weak directional drift exists
""")
