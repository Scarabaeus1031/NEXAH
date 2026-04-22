# FIELD_LAYER/field_decomposition/scripts/v8_2_decision_delay_map.py

"""
NEXAH V8.2 — Decision Delay Map

Goal:
→ measure how long trajectories "hesitate"
→ detect real transition / gate regions
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "FIELD_LAYER/field_decomposition/outputs/v8_2"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# LOAD FIELD (from V8.1)
# ============================================================

nx, ny = 200, 200
x = np.linspace(6, 17, nx)
y = np.linspace(22, 31, ny)
X, Y = np.meshgrid(x, y)

# reload field (recompute for consistency)
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
# TARGET BASINS (centers)
# ============================================================

A1 = np.array([10.5, 25.0])
A2 = np.array([14.5, 26.5])

def classify(px, py):
    d1 = np.linalg.norm([px - A1[0], py - A1[1]])
    d2 = np.linalg.norm([px - A2[0], py - A2[1]])
    return 1 if d1 < d2 else 2

# ============================================================
# SIMULATION
# ============================================================

def simulate_delay(x0, y0, steps=400, dt=0.08, radius=0.5):

    px, py = x0, y0
    initial_class = None

    for t in range(steps):

        ix = np.clip(np.searchsorted(x, px) - 1, 0, nx - 1)
        iy = np.clip(np.searchsorted(y, py) - 1, 0, ny - 1)

        vx = Fx_total[iy, ix]
        vy = Fy_total[iy, ix]

        px += vx * dt
        py += vy * dt

        c = classify(px, py)

        # detect stable basin entry
        if c == 1:
            if np.linalg.norm([px - A1[0], py - A1[1]]) < radius:
                return t
        if c == 2:
            if np.linalg.norm([px - A2[0], py - A2[1]]) < radius:
                return t

    return steps  # max = long delay

# ============================================================
# COMPUTE MAP
# ============================================================

delay_map = np.zeros((ny, nx))

for i in range(nx):
    for j in range(ny):

        px = x[i]
        py = y[j]

        delay_map[j, i] = simulate_delay(px, py)

print("✓ delay computed")

# normalize for visualization
delay_norm = delay_map / np.max(delay_map)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 7))

plt.contourf(X, Y, delay_norm, levels=50, cmap="plasma")

plt.colorbar(label="Decision Delay (normalized)")

plt.title("NEXAH V8.2 — Decision Delay Map")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v8_2_delay_map.png"), dpi=150)
plt.close()

# ============================================================
# SAVE
# ============================================================

np.save(os.path.join(OUTDIR, "delay_map.npy"), delay_map)

print("✓ V8.2 done →", OUTDIR)
