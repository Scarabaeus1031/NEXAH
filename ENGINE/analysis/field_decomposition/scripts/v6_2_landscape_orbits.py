import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# GRID
# ============================================================
x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# ============================================================
# FIELD
# ============================================================
def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X-x0)**2)/(2*sx**2) + ((Y-y0)**2)/(2*sy**2)))

V = (
    -2.0 * gauss(10.0, 25.0, 1.2, 1.0, 1.0)
    -2.3 * gauss(13.6, 26.0, 1.0, 1.0, 1.0)
    -1.0 * gauss(12.0, 24.0, 0.8, 0.9, 1.0)
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0)
)

# Gradient
dV_dy, dV_dx = np.gradient(V, dy, dx)
Fx = -dV_dx
Fy = -dV_dy

# ============================================================
# SAMPLE
# ============================================================
def sample(px, py, A):
    ix = np.argmin(np.abs(x - px))
    iy = np.argmin(np.abs(y - py))
    return A[iy, ix]

# ============================================================
# SIMULATION
# ============================================================
def simulate(x0, y0, vx0, vy0, steps=800, dt=0.02, damping=0.02):
    px, py = x0, y0
    vx, vy = vx0, vy0

    xs, ys = [px], [py]

    for _ in range(steps):
        fx = sample(px, py, Fx)
        fy = sample(px, py, Fy)

        vx += dt * (fx - damping * vx)
        vy += dt * (fy - damping * vy)

        px += dt * vx
        py += dt * vy

        xs.append(px)
        ys.append(py)

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(xs), np.array(ys)

starts = [
    (8.0, 29.0, 0.6, 0.0),
    (15.0, 29.0, -0.5, 0.0),
    (9.0, 23.0, 0.4, 0.5),
    (12.5, 27.0, 0.0, -0.7),
]

trajs = [simulate(*s) for s in starts]

# ============================================================
# 3D PLOT
# ============================================================
fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111, projection='3d')

# Landscape
ax.plot_surface(X, Y, V, cmap='viridis', alpha=0.8)

# Trajectories on surface
colors = ["cyan","orange","lime","magenta"]

for i,(xs,ys) in enumerate(trajs):
    zs = [sample(px, py, V) for px,py in zip(xs,ys)]
    ax.plot(xs, ys, zs, color=colors[i], linewidth=2)

# Mark centers
centers = [
    (10,25,"C0"),
    (12,24,"C1"),
    (13.6,26,"C2"),
    (11.2,28.5,"M0")
]

for px,py,label in centers:
    z = sample(px,py,V)
    ax.scatter(px,py,z, color="black", s=60)
    ax.text(px,py,z+0.3,label)

ax.set_title("NEXAH V6.2 — Trajectories on Potential Landscape")
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.set_zlabel("V")

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
