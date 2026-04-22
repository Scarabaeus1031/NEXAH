import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# FIELD SETUP (gleich wie bei dir)
# ============================================================

x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X - x0)**2)/(2*sx**2) + ((Y - y0)**2)/(2*sy**2)))

# Potential
V = (
    -2.0 * gauss(10, 25, 1.2, 1.0, 1.0)   # C0
    -2.5 * gauss(13.5, 26, 1.1, 1.0, 1.0) # C2
    +2.0 * gauss(11.2, 28.5, 1.0, 1.0, 1.0) # Source M0
    -1.0 * gauss(12, 24, 0.8, 0.9, 1.0)   # C1
)

# Gradient
dVy, dVx = np.gradient(V)
U = -dVx
V_flow = -dVy

# ============================================================
# FIGURE
# ============================================================

fig, axs = plt.subplots(2, 2, figsize=(14, 12))

# ============================================================
# Q1 — Klassische Sicht (Forces / Physics)
# ============================================================

ax = axs[0, 0]

ax.set_title("Q1 — Classical View (Forces)")

# Kräftefeld (nur Pfeile)
skip = 8
ax.quiver(
    X[::skip, ::skip],
    Y[::skip, ::skip],
    U[::skip, ::skip],
    V_flow[::skip, ::skip],
    color="black",
    alpha=0.6
)

# "Planeten"
points = [(10,25,"C0"), (12,24,"C1"), (13.5,26,"C2"), (11.2,28.5,"M0")]
for px, py, label in points:
    ax.scatter(px, py, s=100)
    ax.text(px+0.2, py+0.2, label)

ax.set_xlabel("α")
ax.set_ylabel("β")

# ============================================================
# Q2 — Feldsicht (NEXAH core)
# ============================================================

ax = axs[0, 1]

ax.set_title("Q2 — Field View (Potential + Flow)")

contour = ax.contourf(X, Y, V, levels=50, cmap="viridis")
ax.streamplot(X, Y, U, V_flow, color="white", density=1.2)

for px, py, label in points:
    ax.scatter(px, py, s=100, edgecolor="black")
    ax.text(px+0.2, py+0.2, label, color="white")

ax.set_xlabel("α")
ax.set_ylabel("β")

# ============================================================
# Q3 — Struktur (Basins + Boundary)
# ============================================================

ax = axs[1, 0]

ax.set_title("Q3 — Structure (Basins / Boundary)")

# Approx boundary via gradient magnitude
grad_mag = np.sqrt(dVx**2 + dVy**2)
boundary = grad_mag > np.percentile(grad_mag, 85)

ax.contourf(X, Y, V, levels=40, cmap="coolwarm", alpha=0.6)
ax.contour(X, Y, boundary, levels=[0.5], colors="magenta", linewidths=2)

# Gate (approx)
gate = (12.5, 25)
ax.scatter(*gate, color="white", marker="X", s=120)
ax.text(gate[0]+0.2, gate[1]+0.2, "GATE", color="white")

for px, py, label in points:
    ax.scatter(px, py, s=100)
    ax.text(px+0.2, py+0.2, label)

ax.set_xlabel("α")
ax.set_ylabel("β")

# ============================================================
# Q4 — Navigation (Trajectories)
# ============================================================

ax = axs[1, 1]

ax.set_title("Q4 — Navigation (Trajectories)")

ax.contourf(X, Y, V, levels=50, cmap="viridis", alpha=0.8)

# Beispiel-Trajektorien
def simulate(x0, y0, steps=200, dt=0.1):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    
    for _ in range(steps):
        ix = np.argmin(np.abs(X[0] - x))
        iy = np.argmin(np.abs(Y[:,0] - y))
        
        vx = U[iy, ix]
        vy = V_flow[iy, ix]
        
        x += vx * dt
        y += vy * dt
        
        xs.append(x)
        ys.append(y)
    
    return xs, ys

starts = [(8,29), (15,29), (9,23)]

for sx, sy in starts:
    xs, ys = simulate(sx, sy)
    ax.plot(xs, ys, linewidth=2)

for px, py, label in points:
    ax.scatter(px, py, s=100, edgecolor="black")
    ax.text(px+0.2, py+0.2, label, color="white")

ax.set_xlabel("α")
ax.set_ylabel("β")

# ============================================================
# FINAL
# ============================================================

plt.suptitle("NEXAH V4 — Unified Perspective (Physics → Field → Structure → Navigation)", fontsize=14)

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
