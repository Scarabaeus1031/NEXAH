# FIELD_LAYER/field_decomposition/scripts/v9_7b_transport_map.py

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_7b")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

channels = np.load(os.path.join(BASE, "v9_5", "orbit_entry_channels.npy"))
density = np.load(os.path.join(BASE, "v9_2", "unique_density.npy"))

# ============================================================
# FLOW FIELD
# ============================================================

gy, gx = np.gradient(density)
dx = -gy
dy = gx

mag = np.sqrt(dx**2 + dy**2) + 1e-8
dx /= mag
dy /= mag

ny, nx = density.shape

# ============================================================
# SIMULATION
# ============================================================

def simulate(px, py, steps=300, dt=1.0):
    path = []

    for _ in range(steps):
        ix = int(np.clip(px, 0, nx-1))
        iy = int(np.clip(py, 0, ny-1))

        vx = dx[iy, ix]
        vy = dy[iy, ix]

        # ----------------------------
        # 🔥 SYMMETRY BREAK
        # ----------------------------
        cx, cy = nx / 2, ny / 2
        rx = px - cx
        ry = py - cy

        # inward + slight instability
        vx += -0.03 * rx
        vy += -0.03 * ry

        # small anisotropic noise
        vx += np.random.randn() * 0.01
        vy += np.random.randn() * 0.008

        px += vx * dt
        py += vy * dt

        path.append((px, py))

        # escape condition
        if px < 0 or px >= nx or py < 0 or py >= ny:
            return path, "escape"

    # classification
    r = np.sqrt((px - nx/2)**2 + (py - ny/2)**2)

    if r < 18:
        return path, "core"
    elif r < 65:
        return path, "orbit"
    else:
        return path, "escape"

# ============================================================
# RUN
# ============================================================

mask = channels > 0
y_idx, x_idx = np.where(mask)

paths = []
labels = []

for i in range(len(x_idx)):
    px = float(x_idx[i])
    py = float(y_idx[i])

    path, label = simulate(px, py)

    paths.append(path)
    labels.append(label)

print("✓ trajectories:", len(paths))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 8))
plt.imshow(density, cmap="gray", alpha=0.3)

for path, label in zip(paths, labels):
    path = np.array(path)

    if label == "orbit":
        color = "green"
    elif label == "core":
        color = "red"
    else:
        color = "blue"

    plt.plot(path[:, 0], path[:, 1], color=color, alpha=0.4)

plt.title("NEXAH V9.7b — Transport Map (Symmetry Broken)")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_7b_transport_map.png"), dpi=150)

np.save(os.path.join(OUTDIR, "transport_labels.npy"), np.array(labels))

print("✓ V9.7b done →", OUTDIR)
