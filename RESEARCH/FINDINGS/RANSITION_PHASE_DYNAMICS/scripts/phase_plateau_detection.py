import numpy as np
import matplotlib.pyplot as plt
import os

# =============================
# PATHS
# =============================
OUTPUT_PATH = "RESEARCH/FINDINGS/TRANSITION_PHASE_DYNAMICS/figures/phase"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# =============================
# INPUT (reuse Halvorsen or load)
# =============================

# 👉 OPTION 1: direkt aus vorherigem Script kopieren
# (hier minimal integriert für Standalone)

def halvorsen(x, y, z, a=1.4):
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return dx, dy, dz

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

    if abs(xs[i+1]) > 50:
        xs[i+1] = np.sign(xs[i+1]) * 50
        ys[i+1] = np.sign(ys[i+1]) * 50
        zs[i+1] = np.sign(zs[i+1]) * 50

xs = xs[burn_in:]
ys = ys[burn_in:]

# =============================
# PHASE
# =============================
theta = np.arctan2(ys, xs)
theta_unwrapped = np.unwrap(theta)
dtheta = np.diff(theta_unwrapped)

# =============================
# PLATEAU DETECTION
# =============================

# Threshold: "fast vs slow phase movement"
threshold = np.percentile(np.abs(dtheta), 30)

plateaus = []
start = None

for i, val in enumerate(np.abs(dtheta)):
    if val < threshold:
        if start is None:
            start = i
    else:
        if start is not None:
            plateaus.append((start, i))
            start = None

# close last
if start is not None:
    plateaus.append((start, len(dtheta)))

# =============================
# ANALYSIS
# =============================
durations = [end - start for start, end in plateaus]

print("\n=== PLATEAU ANALYSIS ===")
print(f"Detected plateaus: {len(plateaus)}")
print(f"Mean duration: {np.mean(durations):.2f}")
print(f"Max duration: {np.max(durations)}")
print(f"Min duration: {np.min(durations)}")

# =============================
# VISUALIZATION
# =============================
plt.figure(figsize=(12, 4))
plt.plot(theta_unwrapped, label="θ (unwrapped)", alpha=0.7)

for start, end in plateaus:
    plt.axvspan(start, end, color='red', alpha=0.15)

plt.title("Phase Plateaus — Halvorsen")
plt.xlabel("time")
plt.ylabel("θ")
plt.legend()

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/halvorsen_plateau_detection.png")
plt.close()

# =============================
# HISTOGRAM
# =============================
plt.figure(figsize=(6,4))
plt.hist(durations, bins=30)
plt.title("Plateau Duration Distribution")
plt.xlabel("length")
plt.ylabel("count")

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/halvorsen_plateau_duration_hist.png")
plt.close()
