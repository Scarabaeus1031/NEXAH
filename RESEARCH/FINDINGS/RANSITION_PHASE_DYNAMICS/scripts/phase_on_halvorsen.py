import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/phase"
os.makedirs(OUTPUT_PATH, exist_ok=True)

def halvorsen(x, y, z, a=1.4):
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return dx, dy, dz

# =============================
# STABLE INTEGRATION
# =============================
dt = 0.0005
steps = 80000
burn_in = 20000

xs = np.zeros(steps)
ys = np.zeros(steps)
zs = np.zeros(steps)

xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

for i in range(steps - 1):
    dx, dy, dz = halvorsen(xs[i], ys[i], zs[i])

    xs[i+1] = xs[i] + dx * dt
    ys[i+1] = ys[i] + dy * dt
    zs[i+1] = zs[i] + dz * dt

    # HARD CLIP (wichtig!)
    if abs(xs[i+1]) > 50 or abs(ys[i+1]) > 50 or abs(zs[i+1]) > 50:
        xs[i+1] = np.sign(xs[i+1]) * 50
        ys[i+1] = np.sign(ys[i+1]) * 50
        zs[i+1] = np.sign(zs[i+1]) * 50

# =============================
# CUT TRANSIENT
# =============================
xs = xs[burn_in:]
ys = ys[burn_in:]
zs = zs[burn_in:]

# =============================
# PHASE
# =============================
theta = np.arctan2(ys, xs)
theta_unwrapped = np.unwrap(theta)

dtheta = np.diff(theta_unwrapped)
dtheta = dtheta[np.isfinite(dtheta)]  # remove nan

# =============================
# PLOTS
# =============================
plt.figure(figsize=(10,4))
plt.plot(theta_unwrapped)
plt.title("Unwrapped Phase — Halvorsen (stable)")
plt.savefig(f"{OUTPUT_PATH}/halvorsen_phase_unwrapped.png")
plt.close()

plt.figure(figsize=(6,4))
plt.hist(dtheta, bins=100)
plt.title("Δθ Distribution — Halvorsen (stable)")
plt.savefig(f"{OUTPUT_PATH}/halvorsen_phase_increment_hist.png")
plt.close()

plt.figure(figsize=(6,6))
plt.scatter(xs, ys, s=0.1)
plt.title("Halvorsen Projection (stable)")
plt.savefig(f"{OUTPUT_PATH}/halvorsen_xy_projection.png")
plt.close()

# =============================
# STATS
# =============================
print("\n=== HALVORSEN (STABLE) ===")
print(f"Mean Δθ: {np.mean(dtheta):.6f}")
print(f"Std  Δθ: {np.std(dtheta):.6f}")
