# FIELD_LAYER/field_decomposition/scripts/v9_4_orbit_entry_map.py

"""
NEXAH V9.4 — Orbit Entry Map

Goal:
→ measure from where trajectories can enter the orbit ring
→ identify entry channels into the metastable region
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PATHS
# ============================================================

OUTDIR = "FIELD_LAYER/field_decomposition/outputs/v9_4"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# GRID
# ============================================================

nx, ny = 200, 200
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# ============================================================
# FIELD (same as V8/V9)
# ============================================================

def gaussian(x, y, cx, cy, sigma=1.5):
    return np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))

V = (
    -2.0 * gaussian(X, Y, 10.5, 25.0, sigma=1.8)
    -2.0 * gaussian(X, Y, 14.5, 26.5, sigma=1.8)
)

Vy, Vx = np.gradient(V)
Fx = -Vx
Fy = -Vy

def rotation(x, y, cx, cy):
    dx = x - cx
    dy = y - cy
    return -dy, dx

Rx1, Ry1 = rotation(X, Y, 10.5, 25.0)
Rx2, Ry2 = rotation(X, Y, 14.5, 26.5)

Rx = 0.6 * Rx1 + 0.6 * Rx2
Ry = 0.6 * Ry1 + 0.6 * Ry2

Fx_total = Fx + 0.3 * Rx
Fy_total = Fy + 0.3 * Ry

norm = np.sqrt(Fx_total**2 + Fy_total**2) + 1e-8
Fx_total /= norm
Fy_total /= norm

# ============================================================
# RING GEOMETRY
# ============================================================

CENTER = np.array([12.5, 25.8])
R_INNER = 1.1
R_OUTER = 2.7

def radius_from_center(px, py):
    return np.linalg.norm([px - CENTER[0], py - CENTER[1]])

def sample(px, py):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, nx - 1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, ny - 1)
    return Fx_total[iy, ix], Fy_total[iy, ix]

# ============================================================
# ENTRY TEST
# ============================================================

def enters_ring(x0, y0, steps=300, dt=0.08):
    px, py = x0, y0

    for _ in range(steps):
        vx, vy = sample(px, py)

        px += vx * dt
        py += vy * dt

        r = radius_from_center(px, py)

        if R_INNER <= r <= R_OUTER:
            return 1

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            return 0

    return 0

# ============================================================
# COMPUTE MAP
# ============================================================

entry_map = np.zeros((ny, nx))

for i in range(nx):
    for j in range(ny):
        entry_map[j, i] = enters_ring(x[i], y[j])

print("✓ orbit entry computed")
print("entries:", int(np.sum(entry_map)))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

plt.contourf(X, Y, entry_map, levels=2, cmap="coolwarm")
plt.colorbar(label="Orbit Entry (0 = no, 1 = yes)")

theta = np.linspace(0, 2*np.pi, 400)
plt.plot(
    CENTER[0] + R_INNER * np.cos(theta),
    CENTER[1] + R_INNER * np.sin(theta),
    color="white", linewidth=1.0, alpha=0.7
)
plt.plot(
    CENTER[0] + R_OUTER * np.cos(theta),
    CENTER[1] + R_OUTER * np.sin(theta),
    color="white", linewidth=1.0, alpha=0.7
)

plt.title("NEXAH V9.4 — Orbit Entry Map")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v9_4_orbit_entry.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "orbit_entry.npy"), entry_map)

print("✓ saved orbit_entry.npy")
print("✓ V9.4 done →", OUTDIR)
