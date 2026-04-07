import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import Counter

# ============================================================
# NEXAH v7.7b — Semantic Lorenz Navigation Layer
# ============================================================

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------
steps = 12000
dt = 0.01

# Lorenz system
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

# ------------------------------------------------------------
# LORENZ SYSTEM
# ------------------------------------------------------------
def lorenz_step(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
xs = np.zeros(steps)
ys = np.zeros(steps)
zs = np.zeros(steps)

# initial condition
xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0

for i in range(steps - 1):
    dx, dy, dz = lorenz_step(xs[i], ys[i], zs[i])
    xs[i+1] = xs[i] + dx * dt
    ys[i+1] = ys[i] + dy * dt
    zs[i+1] = zs[i] + dz * dt

# ------------------------------------------------------------
# FTLE-LIKE INSTABILITY (simple proxy)
# ------------------------------------------------------------
vel = np.sqrt(np.diff(xs)**2 + np.diff(ys)**2 + np.diff(zs)**2)
ftle = np.zeros_like(xs)
ftle[1:] = np.log(vel + 1e-8)

# smooth a bit
window = 50
ftle_smooth = np.convolve(ftle, np.ones(window)/window, mode='same')

# ------------------------------------------------------------
# SEMANTIC REGION CLASSIFICATION
# ------------------------------------------------------------
def classify_region(x, y, z, ftle,
                    center=(0,0),
                    r_eye=4.0,
                    ftle_thresh=2.5):

    cx, cy = center
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)

    # 👁 Eye (central basin)
    if dist < r_eye:
        return "eye"

    # 🧵 Horizon (instability ridge)
    if ftle > ftle_thresh:
        return "horizon"

    # 🌙 Moon (left lobe)
    if x < 0:
        return "moon"

    # 🔥 Deris (right lobe)
    return "deris"

# ------------------------------------------------------------
# APPLY SEMANTIC LAYER
# ------------------------------------------------------------
region_colors = {
    "eye": "green",
    "moon": "blue",
    "deris": "red",
    "horizon": "yellow"
}

regions = []
colors = []

for i in range(len(xs)):
    r = classify_region(xs[i], ys[i], zs[i], ftle_smooth[i])
    regions.append(r)
    colors.append(region_colors[r])

# ------------------------------------------------------------
# REGION STATISTICS
# ------------------------------------------------------------
counts = Counter(regions)

print("\n=== NEXAH v7.7b Summary ===")
for k, v in counts.items():
    print(f"{k}: {v}")

# ------------------------------------------------------------
# 1. SEMANTIC TRAJECTORY (2D)
# ------------------------------------------------------------
plt.figure(figsize=(8,8))

for i in range(len(xs)-1):
    plt.plot(xs[i:i+2], ys[i:i+2], color=colors[i], alpha=0.5)

plt.scatter(xs[::100], ys[::100], c=[colors[i] for i in range(0,len(xs),100)], s=10)

plt.title("NEXAH v7.7b — Semantic Navigation Map")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)

# ------------------------------------------------------------
# 2. FTLE MAP
# ------------------------------------------------------------
plt.figure(figsize=(8,6))
plt.scatter(xs, ys, c=ftle_smooth, cmap='inferno', s=1)
plt.colorbar(label="FTLE proxy")
plt.title("FTLE-like Instability Map")
plt.xlabel("X")
plt.ylabel("Y")

# ------------------------------------------------------------
# 3. 3D ATTRACTOR WITH SEMANTICS
# ------------------------------------------------------------
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

for i in range(0, len(xs), 5):
    ax.scatter(xs[i], ys[i], zs[i], color=colors[i], s=2)

ax.set_title("3D Lorenz Attractor — Semantic Layer")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# ------------------------------------------------------------
# 4. REGION TIMELINE
# ------------------------------------------------------------
region_map = {"eye":0, "moon":1, "deris":2, "horizon":3}
region_series = [region_map[r] for r in regions]

plt.figure(figsize=(10,3))
plt.plot(region_series, linewidth=1)
plt.title("Region Timeline")
plt.yticks([0,1,2,3], ["eye","moon","deris","horizon"])
plt.xlabel("time step")

# ------------------------------------------------------------
# SHOW ALL
# ------------------------------------------------------------
plt.show()
