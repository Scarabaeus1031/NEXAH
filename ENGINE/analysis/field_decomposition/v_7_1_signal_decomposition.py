"""
NEXAH V7.1 — Signal Decomposition (Speed vs Turning)
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTDIR = "output/v7_1"
os.makedirs(OUTDIR, exist_ok=True)

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
x = np.linspace(6, 17, 200)
y = np.linspace(22, 31, 200)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

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
# TRAJECTORY
# ------------------------------------------------------------
def simulate(x0, y0, steps=300, dt=0.05):

    px, py = x0, y0
    traj = []

    for i in range(steps):

        fx = sample(px, py, Fx)
        fy = sample(px, py, Fy)

        vx, vy = fx, fy

        px += vx * dt
        py += vy * dt

        traj.append((px, py, vx, vy))

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(traj)

# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
starts = [(7+i, 23+j) for i in range(10) for j in range(10)]

speed_map = np.zeros_like(V)
turn_map  = np.zeros_like(V)

for s in starts:

    traj = simulate(*s)

    if len(traj) < 5:
        continue

    speeds = []
    turns  = []

    for i in range(len(traj)):
        vx, vy = traj[i][2], traj[i][3]
        speed = np.sqrt(vx**2 + vy**2)
        speeds.append(speed)

        if i > 0:
            v_prev = traj[i-1][2:4]
            v_now  = traj[i][2:4]
            turn = np.linalg.norm(v_now - v_prev)
        else:
            turn = 0

        turns.append(turn)

    speeds = np.array(speeds)
    turns  = np.array(turns)

    s_thresh = np.percentile(speeds, 90)
    t_thresh = np.percentile(turns, 90)

    for i in range(len(traj)):
        px, py = traj[i][0], traj[i][1]

        ix = np.clip(np.searchsorted(x, px)-1, 0, len(x)-1)
        iy = np.clip(np.searchsorted(y, py)-1, 0, len(y)-1)

        if speeds[i] > s_thresh:
            speed_map[iy, ix] += 1

        if turns[i] > t_thresh:
            turn_map[iy, ix] += 1

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

axs[0].contourf(X, Y, speed_map, levels=40, cmap="inferno")
axs[0].set_title("Speed Peaks (Pull / Energy)")

axs[1].contourf(X, Y, turn_map, levels=40, cmap="magma")
axs[1].set_title("Turning Peaks (Curvature / Transition)")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_1_maps.png"), dpi=150)
plt.close()

print("V7.1 done →", OUTDIR)
