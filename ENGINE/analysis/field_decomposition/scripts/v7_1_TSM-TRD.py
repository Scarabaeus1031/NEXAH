"""
NEXAH V7.0 — Trajectory Signal Mapping + Splinter Detection + GIF
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ============================================================
# OUTPUT
# ============================================================

OUTDIR = "output/v7_0"
os.makedirs(OUTDIR, exist_ok=True)

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
    return amp * np.exp(-(((X - x0)**2)/(2*sx**2) + ((Y - y0)**2)/(2*sy**2)))

V = (
    -2.2 * gauss(10.6, 25.0, 1.2, 1.0, 1.0)
    -2.0 * gauss(13.5, 26.0, 1.0, 1.0, 1.0)
    +1.9 * gauss(11.5, 28.6, 1.0, 1.0, 1.0)
)

# Gradient
dVdy, dVdx = np.gradient(V, dy, dx)

# Drift (Rotation)
epsilon = 0.12
Dx = -epsilon * (Y - 26.5)
Dy =  epsilon * (X - 11.5)

Fx = -dVdx + Dx
Fy = -dVdy + Dy

# ============================================================
# SAMPLING
# ============================================================

def sample(px, py, A):
    ix = np.clip(np.searchsorted(x, px) - 1, 0, len(x)-1)
    iy = np.clip(np.searchsorted(y, py) - 1, 0, len(y)-1)
    return A[iy, ix]

# ============================================================
# TRAJECTORY + SIGNAL
# ============================================================

def simulate(x0, y0, steps=300, dt=0.05):

    px, py = x0, y0
    traj = []
    speeds = []
    turns = []

    vx, vy = 0, 0

    for i in range(steps):

        fx = sample(px, py, Fx)
        fy = sample(px, py, Fy)

        vx = fx
        vy = fy

        speed = np.sqrt(vx**2 + vy**2)

        # turning (change of direction)
        if i > 0:
            v_prev = np.array([traj[-1][2], traj[-1][3]])
            v_now = np.array([vx, vy])
            turn = np.linalg.norm(v_now - v_prev)
        else:
            turn = 0

        px += vx * dt
        py += vy * dt

        traj.append((px, py, vx, vy))
        speeds.append(speed)
        turns.append(turn)

        if px < x.min() or px > x.max() or py < y.min() or py > y.max():
            break

    return np.array(traj), np.array(speeds), np.array(turns)

# ============================================================
# RUN MANY TRAJECTORIES
# ============================================================

starts = []

for i in range(10):
    for j in range(10):
        sx = 7 + i
        sy = 23 + j
        starts.append((sx, sy))

trajectories = []
peak_points = []

heatmap = np.zeros_like(V)

for s in starts:

    traj, speeds, turns = simulate(*s)

    if len(traj) < 5:
        continue

    # signal = speed + turning
    signal = speeds + 0.7 * turns

    threshold = np.percentile(signal, 90)

    for k in range(len(traj)):
        if signal[k] > threshold:
            px, py = traj[k][0], traj[k][1]

            ix = np.clip(np.searchsorted(x, px)-1, 0, len(x)-1)
            iy = np.clip(np.searchsorted(y, py)-1, 0, len(y)-1)

            heatmap[iy, ix] += 1
            peak_points.append((px, py))

    trajectories.append(traj)

# ============================================================
# STATIC PLOT
# ============================================================

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# --- Q1 FIELD + TRAJ
ax = axs[0]
cf = ax.contourf(X, Y, V, levels=40, cmap="cividis")

for traj in trajectories:
    ax.plot(traj[:,0], traj[:,1], color="white", linewidth=0.5, alpha=0.5)

ax.set_title("Field + Trajectories")

# --- Q2 SPLINTER HEATMAP
ax = axs[1]
cf = ax.contourf(X, Y, heatmap, levels=40, cmap="inferno")

ax.set_title("Splinter / Transition Heatmap")

plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, "v7_static.png"), dpi=150)
plt.close()

# ============================================================
# GIF ANIMATION
# ============================================================

fig, ax = plt.subplots(figsize=(6,6))
ax.contourf(X, Y, V, levels=40, cmap="cividis")

lines = [ax.plot([], [], lw=1)[0] for _ in trajectories]

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def animate(i):
    for idx, traj in enumerate(trajectories):
        if i < len(traj):
            lines[idx].set_data(traj[:i,0], traj[:i,1])
    return lines

anim = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=200, interval=40, blit=True
)

gif_path = os.path.join(OUTDIR, "v7_animation.gif")
anim.save(gif_path, writer="pillow")

print("V7 done →", OUTDIR)
