# FIELD_LAYER/field_decomposition/scripts/v9_8_multi_regime_field.py

import os
import numpy as np
import matplotlib.pyplot as plt

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_8")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

channels = np.load(os.path.join(BASE, "v9_5", "orbit_entry_channels.npy"))
density = np.load(os.path.join(BASE, "v9_2", "unique_density.npy"))

gy, gx = np.gradient(density)

ny, nx = density.shape
cx, cy = nx / 2, ny / 2

# ============================================================
# FIELD COMPONENTS
# ============================================================

def get_field(px, py):

    ix = int(np.clip(px, 0, nx-1))
    iy = int(np.clip(py, 0, ny-1))

    # base swirl
    fx = -gy[iy, ix]
    fy = gx[iy, ix]

    # normalize
    n = np.sqrt(fx**2 + fy**2) + 1e-8
    fx /= n
    fy /= n

    # radial
    rx = px - cx
    ry = py - cy
    r = np.sqrt(rx**2 + ry**2) + 1e-8

    # ----------------------------
    # REGIME SYSTEM
    # ----------------------------

    # inner attractor
    if r < 25:
        fx += -0.05 * rx
        fy += -0.05 * ry

    # orbit band
    elif r < 70:
        fx += -0.01 * rx
        fy += -0.01 * ry

    # outer repulsion
    else:
        fx += 0.06 * rx
        fy += 0.06 * ry

    return fx, fy

# ============================================================
# SIMULATION
# ============================================================

def simulate(px, py, steps=350):
    path = []

    for _ in range(steps):

        vx, vy = get_field(px, py)

        # small noise
        vx += np.random.randn() * 0.01
        vy += np.random.randn() * 0.01

        px += vx
        py += vy

        path.append((px, py))

        if px < 0 or px >= nx or py < 0 or py >= ny:
            return path, "escape"

    r = np.sqrt((px - cx)**2 + (py - cy)**2)

    if r < 20:
        return path, "core"
    elif r < 70:
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

    if label == "core":
        color = "red"
    elif label == "orbit":
        color = "green"
    else:
        color = "blue"

    plt.plot(path[:, 0], path[:, 1], color=color, alpha=0.4)

plt.title("NEXAH V9.8 — Multi-Regime Transport")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_8_transport_map.png"), dpi=150)

np.save(os.path.join(OUTDIR, "transport_labels.npy"), np.array(labels))

print("✓ V9.8 done →", OUTDIR)
