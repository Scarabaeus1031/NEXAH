# FIELD_LAYER/field_decomposition/scripts/v10_0_regime_map.py

"""
NEXAH V10.0 — Regime Map Generator

Goal:
→ scan the field point-by-point
→ simulate short trajectories
→ assign each start point to a dominant regime

Output:
→ regime map
→ regime counts
→ first instrument-style measurement of the field
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

BASE = "FIELD_LAYER/field_decomposition/outputs"
OUTDIR = os.path.join(BASE, "v10_0")
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD
# ============================================================

density = np.load(os.path.join(BASE, "v9_2", "unique_density.npy"))

ny, nx = density.shape

# ============================================================
# BASE FIELD
# ============================================================

gy, gx = np.gradient(density)

# normalized rotational field
dx = -gy
dy = gx

mag = np.sqrt(dx**2 + dy**2) + 1e-8
dx /= mag
dy /= mag

# ============================================================
# FEATURES
# ============================================================

grad_mag = np.sqrt(gx**2 + gy**2)
gxx = np.gradient(gx, axis=1)
gyy = np.gradient(gy, axis=0)
curvature = gxx + gyy

dens_norm = density / (np.max(density) + 1e-8)
grad_norm = grad_mag / (np.max(grad_mag) + 1e-8)
curv_norm = np.abs(curvature) / (np.max(np.abs(curvature)) + 1e-8)

cx, cy = nx / 2, ny / 2

# ============================================================
# REGIME FUNCTION
# ============================================================

REGIME_TO_ID = {
    "core": 0,
    "orbit": 1,
    "shear": 2,
    "escape": 3,
    "drift": 4,
}

ID_TO_REGIME = {v: k for k, v in REGIME_TO_ID.items()}

def local_regime(px, py):
    ix = int(np.clip(px, 0, nx - 1))
    iy = int(np.clip(py, 0, ny - 1))

    d = dens_norm[iy, ix]
    g = grad_norm[iy, ix]
    c = curv_norm[iy, ix]

    # emergent regime rules
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
# SIMULATION
# ============================================================

def simulate(px, py, steps=120, dt=1.0):
    visited = []

    for _ in range(steps):
        ix = int(np.clip(px, 0, nx - 1))
        iy = int(np.clip(py, 0, ny - 1))

        vx = dx[iy, ix]
        vy = dy[iy, ix]

        # regime-aware modification
        regime = local_regime(px, py)
        visited.append(regime)

        rx = px - cx
        ry = py - cy

        if regime == "core":
            vx += -0.03 * rx
            vy += -0.03 * ry
            vx *= 0.5
            vy *= 0.5

        elif regime == "orbit":
            vx += -0.01 * rx
            vy += -0.01 * ry

        elif regime == "shear":
            vx, vy = -vy, vx

        elif regime == "escape":
            vx += 0.03 * rx
            vy += 0.03 * ry

        elif regime == "drift":
            vx *= 0.7
            vy *= 0.7

        px += vx * dt
        py += vy * dt

        if px < 0 or px >= nx or py < 0 or py >= ny:
            return "escape"

    # dominant regime along the path
    labels, counts = np.unique(visited, return_counts=True)
    return labels[np.argmax(counts)]

# ============================================================
# SCAN FIELD
# ============================================================

regime_map = np.zeros((ny, nx), dtype=int)

# use a stride for speed; can set to 1 later if desired
stride = 2

for iy in range(0, ny, stride):
    for ix in range(0, nx, stride):
        label = simulate(float(ix), float(iy))
        regime_map[iy, ix] = REGIME_TO_ID[label]

# fill missing pixels by nearest simple copy
for iy in range(ny):
    for ix in range(nx):
        if regime_map[iy, ix] == 0 and stride > 1:
            regime_map[iy, ix] = regime_map[(iy // stride) * stride, (ix // stride) * stride]

# ============================================================
# METRICS
# ============================================================

unique, counts = np.unique(regime_map, return_counts=True)
regime_counts = {ID_TO_REGIME[int(k)]: int(v) for k, v in zip(unique, counts)}

print("✓ regime counts:")
for k, v in regime_counts.items():
    print(f"  {k}: {v}")

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(8, 8))
plt.imshow(regime_map, cmap="tab10", origin="lower")
plt.title("NEXAH V10.0 — Regime Map")
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v10_0_regime_map.png"), dpi=160)

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "regime_map.npy"), regime_map)

with open(os.path.join(OUTDIR, "regime_counts.txt"), "w", encoding="utf-8") as f:
    for k, v in regime_counts.items():
        f.write(f"{k}: {v}\n")

print("✓ saved regime_map.npy")
print("✓ saved regime_counts.txt")
print("✓ V10.0 done →", OUTDIR)
