# FIELD_LAYER/field_decomposition/scripts/v9_9_dynamic_regime_field.py

"""
NEXAH V9.9 — Dynamic Regime Field

Goal:
→ regimes are NOT predefined (radius-based)
→ regimes emerge from:
    - density
    - gradient magnitude
    - curvature

Result:
→ self-organizing transport zones
→ dynamic regime switching
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v9_9")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

channels = np.load(os.path.join(BASE, "v9_5", "orbit_entry_channels.npy"))
density = np.load(os.path.join(BASE, "v9_2", "unique_density.npy"))

ny, nx = density.shape

# ============================================================
# FLOW FIELD
# ============================================================

gy, gx = np.gradient(density)

dx = -gy
dy = gx

mag = np.sqrt(dx**2 + dy**2) + 1e-8
dx /= mag
dy /= mag

# ============================================================
# FIELD FEATURES (NEW)
# ============================================================

grad_mag = np.sqrt(gx**2 + gy**2)

# curvature approximation
gxx = np.gradient(gx, axis=1)
gyy = np.gradient(gy, axis=0)
curvature = gxx + gyy

# normalize features
grad_norm = grad_mag / (np.max(grad_mag) + 1e-8)
curv_norm = np.abs(curvature) / (np.max(np.abs(curvature)) + 1e-8)
dens_norm = density / (np.max(density) + 1e-8)

# ============================================================
# DYNAMIC REGIME FUNCTION
# ============================================================

def get_regime(px, py):
    ix = int(np.clip(px, 0, nx - 1))
    iy = int(np.clip(py, 0, ny - 1))

    g = grad_norm[iy, ix]
    c = curv_norm[iy, ix]
    d = dens_norm[iy, ix]

    # ----------------------------
    # emergent regimes
    # ----------------------------

    if d > 0.6 and c < 0.3:
        return "core"

    if g > 0.4 and c < 0.6:
        return "orbit"

    if c > 0.6:
        return "shear"

    if g < 0.2 and d < 0.2:
        return "escape"

    return "drift"

# ============================================================
# TRAJECTORY SIMULATION
# ============================================================

def simulate(px, py, steps=400, dt=1.0):

    path = []
    regimes = []

    for _ in range(steps):

        ix = int(np.clip(px, 0, nx - 1))
        iy = int(np.clip(py, 0, ny - 1))

        vx = dx[iy, ix]
        vy = dy[iy, ix]

        regime = get_regime(px, py)
        regimes.append(regime)

        # ----------------------------
        # regime-dependent behavior
        # ----------------------------

        if regime == "core":
            vx *= 0.3
            vy *= 0.3

        elif regime == "orbit":
            pass  # pure flow

        elif regime == "shear":
            vx, vy = -vy, vx  # rotate

        elif regime == "escape":
            vx *= 1.5
            vy *= 1.5

        elif regime == "drift":
            vx *= 0.7
            vy *= 0.7

        px += vx * dt
        py += vy * dt

        path.append((px, py))

        if px < 0 or px >= nx or py < 0 or py >= ny:
            return path, regimes, "escape"

    # final classification = dominant regime
    final_label = max(set(regimes), key=regimes.count)

    return path, regimes, final_label

# ============================================================
# RUN SIMULATION
# ============================================================

mask = channels > 0
y_idx, x_idx = np.where(mask)

paths = []
labels = []

for i in range(len(x_idx)):
    px = float(x_idx[i])
    py = float(y_idx[i])

    path, regimes, label = simulate(px, py)

    paths.append(path)
    labels.append(label)

print("✓ trajectories:", len(paths))

# ============================================================
# COLOR MAP
# ============================================================

color_map = {
    "core": "red",
    "orbit": "green",
    "shear": "orange",
    "escape": "blue",
    "drift": "purple"
}

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 8))

plt.imshow(density, cmap="gray", alpha=0.3)

for path, label in zip(paths, labels):
    path = np.array(path)
    plt.plot(path[:, 0], path[:, 1],
             color=color_map.get(label, "black"),
             alpha=0.35)

plt.title("NEXAH V9.9 — Dynamic Regime Field")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_9_dynamic_regime_field.png"), dpi=150)

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "dynamic_labels.npy"), np.array(labels))

print("✓ V9.9 done →", OUTDIR)
