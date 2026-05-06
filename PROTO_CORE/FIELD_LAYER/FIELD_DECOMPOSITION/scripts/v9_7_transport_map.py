# FIELD_LAYER/field_decomposition/scripts/v9_7_transport_map.py

"""
NEXAH V9.7 — Transport Map

Goal:
→ simulate trajectories starting from entry channels
→ determine where they end up

Result:
→ classification of channels:
   - orbit
   - core
   - escape
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_7")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

channels = np.load(os.path.join(BASE, "v9_5", "orbit_entry_channels.npy"))
density = np.load(os.path.join(BASE, "v9_2", "unique_density.npy"))

# ============================================================
# FLOW FIELD (same as V9.6)
# ============================================================

gy, gx = np.gradient(density)
dx = -gy
dy = gx

# normalize field
mag = np.sqrt(dx**2 + dy**2) + 1e-8
dx /= mag
dy /= mag

ny, nx = density.shape

# ============================================================
# TRAJECTORY SIMULATION
# ============================================================

def simulate(px, py, steps=300, dt=1.0):
    path = []

    for _ in range(steps):
        ix = int(np.clip(px, 0, nx-1))
        iy = int(np.clip(py, 0, ny-1))

        vx = dx[iy, ix]
        vy = dy[iy, ix]

        px += vx * dt
        py += vy * dt

        path.append((px, py))

        # stop if leaving domain
        if px < 0 or px >= nx or py < 0 or py >= ny:
            return path, "escape"

    # classify by final position
    center_dist = np.sqrt((px - nx/2)**2 + (py - ny/2)**2)

    if center_dist < 20:
        return path, "core"
    elif center_dist < 60:
        return path, "orbit"
    else:
        return path, "escape"

# ============================================================
# RUN SIMULATION
# ============================================================

mask = channels > 0
y_idx, x_idx = np.where(mask)

results = []
paths = []

for i in range(len(x_idx)):
    px = float(x_idx[i])
    py = float(y_idx[i])

    path, label = simulate(px, py)
    results.append(label)
    paths.append(path)

print("✓ trajectories:", len(paths))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 8))

# background
plt.imshow(density, cmap="gray", alpha=0.3)

# plot trajectories
for path, label in zip(paths, results):
    path = np.array(path)

    if label == "orbit":
        color = "green"
    elif label == "core":
        color = "red"
    else:
        color = "blue"

    plt.plot(path[:, 0], path[:, 1], color=color, alpha=0.4)

plt.title("NEXAH V9.7 — Transport Map (Entry → Outcome)")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_7_transport_map.png"), dpi=150)

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "transport_labels.npy"), np.array(results))

print("✓ V9.7 done →", OUTDIR)
