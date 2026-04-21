"""
NEXAH V7.2 — Transition Cost Map (Target Navigation)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_2"
os.makedirs(OUTDIR, exist_ok=True)

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

TARGET = np.array([13.0, 26.0])

# ------------------------------------------------------------
# FIELD
# ------------------------------------------------------------
def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X - x0)**2)/(2*sx**2) + ((Y - y0)**2)/(2*sy**2)))

V = (
    -2.2 * gauss(10.6, 25.0, 1.2, 1.0, 1.0)
    -2.0 * gauss(13.5, 26.0, 1.0, 1.0, 1.0)
    +1.9 * gauss(11.5, 28.6, 1.0, 1.0, 1.0)
)

dVdy, dVdx = np.gradient(V, dy, dx)

epsilon = 0.12
Dx = -epsilon * (Y - 26.5)
Dy =  epsilon * (X - 11.5)

Fx = -dVdx + Dx
Fy = -dVdy + Dy

# ------------------------------------------------------------
# SAMPLING
# ------------------------------------------------------------
def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

# ------------------------------------------------------------
# TRAJECTORY + COST
# ------------------------------------------------------------
def simulate_cost(x0, y0, steps=300, dt=0.05):

    px, py = x0, y0
    cost = 0

    prev_v = None

    for i in range(steps):

        fx = sample(px, py, Fx)
        fy = sample(px, py, Fy)

        vx, vy = fx, fy

        speed = np.sqrt(vx**2 + vy**2)

        if prev_v is not None:
            turn = np.linalg.norm(np.array([vx,vy]) - prev_v)
        else:
            turn = 0

        # --- COST FUNCTION ---
        step_cost = speed + 0.7 * turn

        cost += step_cost * dt

        prev_v = np.array([vx,vy])

        px += vx * dt
        py += vy * dt

        # distance to target
        dist = np.linalg.norm(np.array([px,py]) - TARGET)

        # early stop if near target
        if dist < 0.2:
            return cost

        # out of bounds
        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            return cost + 50  # penalty

    return cost + 20  # didn't reach target

# ------------------------------------------------------------
# BUILD COST MAP
# ------------------------------------------------------------
cost_map = np.zeros_like(V)

for i in range(len(x)):
    for j in range(len(y)):

        px = x[i]
        py = y[j]

        c = simulate_cost(px, py)

        cost_map[j, i] = c

# normalize
cost_map = np.log1p(cost_map)

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
plt.figure(figsize=(7,6))

plt.contourf(X, Y, cost_map, levels=50, cmap="viridis")

# target marker
plt.scatter(TARGET[0], TARGET[1], color="white", s=50, label="Target")

plt.title("Transition Cost Map → Target (13, 26)")
plt.legend()

plt.tight_layout()

# save image
plt.savefig(os.path.join(OUTDIR, "v7_2_cost_map.png"), dpi=150)

plt.close()

# ------------------------------------------------------------
# 🔥 SAVE DATA (WICHTIG!)
# ------------------------------------------------------------
np.save(os.path.join(OUTDIR, "cost_map.npy"), cost_map)

# optional (empfohlen für spätere Pipeline)
np.save(os.path.join(OUTDIR, "grid_x.npy"), x)
np.save(os.path.join(OUTDIR, "grid_y.npy"), y)

print("V7.2 done →", OUTDIR)
