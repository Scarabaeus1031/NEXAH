import numpy as np
import matplotlib.pyplot as plt
import os

# =============================
# OUTPUT PATH
# =============================
OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/phase"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =============================
# HALVORSEN SYSTEM
# =============================
def halvorsen(x, y, z, a=1.4):
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return dx, dy, dz

# =============================
# SIMULATION (STABLE)
# =============================
dt = 0.001
steps = 50000

xs = np.zeros(steps)
ys = np.zeros(steps)
zs = np.zeros(steps)

xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

for i in range(steps - 1):
    dx, dy, dz = halvorsen(xs[i], ys[i], zs[i])

    xs[i+1] = xs[i] + dx * dt
    ys[i+1] = ys[i] + dy * dt
    zs[i+1] = zs[i] + dz * dt

    # Stabilitäts-Check
    if abs(xs[i+1]) > 100 or abs(ys[i+1]) > 100 or abs(zs[i+1]) > 100:
        print(f"[WARN] divergence at step {i}")
        xs = xs[:i]
        ys = ys[:i]
        zs = zs[:i]
        break

# =============================
# PHASE EXTRACTION
# =============================
theta = np.arctan2(ys, xs)
theta_unwrapped = np.unwrap(theta)

dtheta = np.diff(theta_unwrapped)

# =============================
# PLOTS
# =============================
plt.figure(figsize=(10, 4))
plt.plot(theta_unwrapped)
plt.title("Unwrapped Phase — Halvorsen")
plt.xlabel("time")
plt.ylabel("θ")
plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/halvorsen_phase_unwrapped.png")
plt.close()

plt.figure(figsize=(6, 4))
plt.hist(dtheta, bins=100)
plt.title("Δθ Distribution — Halvorsen")
plt.xlabel("Δθ")
plt.ylabel("frequency")
plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/halvorsen_phase_increment_hist.png")
plt.close()

plt.figure(figsize=(6, 6))
plt.scatter(xs, ys, s=0.1)
plt.title("Halvorsen Projection (x,y)")
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/halvorsen_xy_projection.png")
plt.close()

# =============================
# STATS
# =============================
print("\n=== HALVORSEN PHASE ANALYSIS ===")
print(f"Mean Δθ: {np.mean(dtheta):.6f}")
print(f"Std  Δθ: {np.std(dtheta):.6f}")

print("\n=== INTERPRETATION ===")
print("If θ(t) is irregular:")
print("→ fragmented structure")
print("If Δθ is broad / multi-peaked:")
print("→ multiple competing transitions")
print("If mean Δθ ≠ 0:")
print("→ weak directional drift exists")
