import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# GRID
# ============================================================

x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

# ============================================================
# POTENTIAL (wie vorher)
# ============================================================

def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X - x0)**2)/(2*sx**2) + ((Y - y0)**2)/(2*sy**2)))

V = (
    -2.0 * gauss(10, 25, 1.2, 1.0, 1.0)
    -2.5 * gauss(13.5, 26, 1.1, 1.0, 1.0)
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0)
    -1.0 * gauss(12, 24, 0.8, 0.9, 1.0)
)

# ============================================================
# GRADIENT FIELD (ziehen)
# ============================================================

dVy, dVx = np.gradient(V)
Ux = -dVx
Uy = -dVy

# ============================================================
# ROTATION FIELD (künstlich erzeugt)
# ============================================================

def rotational_field(X, Y, center, strength=1.0):
    cx, cy = center
    dx = X - cx
    dy = Y - cy
    r2 = dx**2 + dy**2 + 0.5
    return -strength * dy / r2, strength * dx / r2

Rx1, Ry1 = rotational_field(X, Y, (10, 25), 2.0)
Rx2, Ry2 = rotational_field(X, Y, (13.5, 26), -2.0)

# Gesamtrotation
Rx = Rx1 + Rx2
Ry = Ry1 + Ry2

# ============================================================
# KOMBINIERTES FELD
# ============================================================

Ux_total = Ux + Rx
Uy_total = Uy + Ry

# ============================================================
# FIGURE
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# ------------------------------------------------------------
# Q1 — Gradient only
# ------------------------------------------------------------
ax = axs[0, 0]
ax.set_title("Q1 — Gradient Field (inward pull)")

ax.contourf(X, Y, V, levels=50, cmap="viridis")
ax.streamplot(X, Y, Ux, Uy, color="white")

# ------------------------------------------------------------
# Q2 — Rotation only
# ------------------------------------------------------------
ax = axs[0, 1]
ax.set_title("Q2 — Rotation Field (orbital tendency)")

mag = np.sqrt(Rx**2 + Ry**2)
ax.contourf(X, Y, mag, levels=50, cmap="magma")
ax.streamplot(X, Y, Rx, Ry, color="white")

# ------------------------------------------------------------
# Q3 — Combined field
# ------------------------------------------------------------
ax = axs[1, 0]
ax.set_title("Q3 — Combined Field (real dynamics)")

ax.contourf(X, Y, V, levels=50, cmap="coolwarm")
ax.streamplot(X, Y, Ux_total, Uy_total, color="white")

# ------------------------------------------------------------
# Q4 — Trajectories
# ------------------------------------------------------------
ax = axs[1, 1]
ax.set_title("Q4 — Trajectories (with momentum)")

ax.contourf(X, Y, V, levels=50, cmap="viridis", alpha=0.7)

def simulate(x0, y0, steps=300, dt=0.1):
    x, y = x0, y0
    xs, ys = [x], [y]
    
    for _ in range(steps):
        ix = np.argmin(np.abs(X[0] - x))
        iy = np.argmin(np.abs(Y[:,0] - y))
        
        vx = Ux_total[iy, ix]
        vy = Uy_total[iy, ix]
        
        x += vx * dt
        y += vy * dt
        
        xs.append(x)
        ys.append(y)
    
    return xs, ys

starts = [(8,29), (15,29), (9,23)]

for s in starts:
    xs, ys = simulate(*s)
    ax.plot(xs, ys, linewidth=2)

plt.suptitle("NEXAH V5 — Gradient vs Rotation → Orbit Formation", fontsize=14)
plt.tight_layout()
# =========================
# NEXAH SAVE BLOCK
# =========================

import os
import matplotlib.pyplot as plt
from datetime import datetime

SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
OUTDIR = os.path.join("ENGINE/analysis/field_decomposition/outputs", SCRIPT_NAME)

os.makedirs(OUTDIR, exist_ok=True)

# --- Save figure ---
outfile = os.path.join(OUTDIR, f"{SCRIPT_NAME}.png")

try:
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"✓ saved figure → {outfile}")
except Exception as e:
    print("⚠️ could not save figure:", e)

# --- Save run info ---
info_path = os.path.join(OUTDIR, "run_info.txt")
with open(info_path, "w") as f:
    f.write(f"script: {SCRIPT_NAME}\n")
    f.write(f"time: {datetime.now()}\n")

# --- Close plot ---
plt.close()
