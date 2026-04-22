"""
NEXAH V6.6 — AXIOM → FIELD Translation

Goal:
Translate dual AXIOM-0 (orientation overlap) + drift into a dynamic field model.

This is NOT a physics claim.
It is a structural simulation to explore:
- emergent trajectories
- orbit-like behavior
- boundary formation

Core idea:
dx/dt = -∇V + ε * Drift
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------
# 1. GRID
# ------------------------
x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

# ------------------------
# 2. POTENTIAL (Dual AXIOM-0)
# ------------------------
def gaussian(x0, y0, strength=1.0, sigma=1.2):
    return strength * np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2))

# Two minima (dual orientation centers)
V = (
    -2.0 * gaussian(10.5, 25.0)  # C0
    -2.0 * gaussian(13.5, 26.0)  # C2
    +1.5 * gaussian(11.5, 28.5)  # "source" / peak
)

# ------------------------
# 3. GRADIENT FIELD
# ------------------------
dVdx, dVdy = np.gradient(V, x, y)

# ------------------------
# 4. DRIFT TERM (AXIOM DRIFT)
# ------------------------
epsilon = 0.08  # small asymmetry

# simple directional drift (can evolve later)
Dx = np.ones_like(X) * 0.5
Dy = np.zeros_like(Y)

# total vector field
Fx = -dVdx + epsilon * Dx
Fy = -dVdy + epsilon * Dy

# ------------------------
# 5. TRAJECTORY INTEGRATION
# ------------------------
def simulate(x0, y0, steps=300, dt=0.05):
    traj = []
    x, y = x0, y0

    for _ in range(steps):
        ix = np.argmin(np.abs(x - x_vals))
        iy = np.argmin(np.abs(y - y_vals))

        vx = Fx[iy, ix]
        vy = Fy[iy, ix]

        x += vx * dt
        y += vy * dt

        traj.append((x, y))

    return np.array(traj)

x_vals = x
y_vals = y

# starting points
starts = [
    (8, 29),
    (12, 27),
    (15, 29),
    (9, 23)
]

trajectories = [simulate(sx, sy) for sx, sy in starts]

# ------------------------
# 6. VISUALIZATION
# ------------------------
plt.figure(figsize=(12, 5))

# Field
plt.subplot(1, 2, 1)
plt.contourf(X, Y, V, levels=40, cmap="viridis")
plt.streamplot(X, Y, Fx, Fy, color="white", density=1.2)
plt.title("Field (Dual AXIOM + Drift)")

# Trajectories
plt.subplot(1, 2, 2)
plt.contourf(X, Y, V, levels=40, cmap="cividis")

for traj in trajectories:
    plt.plot(traj[:,0], traj[:,1])

plt.title("Emergent Trajectories")

plt.tight_layout()
plt.show()
