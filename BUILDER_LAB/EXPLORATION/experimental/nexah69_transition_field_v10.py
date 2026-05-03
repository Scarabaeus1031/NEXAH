import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASE = "ieee118"

FPS = 20
FRAME_SKIP = 2
MAX_FRAMES = 400
PRED_STEPS = 35
STEP = 0.03

# ----------------------------
# LOAD
# ----------------------------

df = pd.read_csv(BASE_PATH / f"{CASE}_v43_dataset.csv").dropna()
cloud = pd.read_csv(BASE_PATH / f"{CASE}_v68_off_manifold_cloud.csv").dropna()

def norm(x):
    m = np.max(np.abs(x))
    return x if m == 0 else x/m

c = norm(df["c"].values)
dc = norm(df["dc"].values)
traj = np.column_stack([c, dc])

# ----------------------------
# BASICS
# ----------------------------

def unit(v):
    n = np.linalg.norm(v)
    return v/n if n > 0 else np.zeros_like(v)

def nearest(p):
    d = traj - p
    i = np.argmin(np.sum(d*d, axis=1))
    return i, traj[i]

def tangent(i):
    if i <= 0: v = traj[1]-traj[0]
    elif i >= len(traj)-1: v = traj[-1]-traj[-2]
    else: v = traj[i+1]-traj[i-1]
    return unit(v)

def density(p):
    d = traj - p
    dist = np.sqrt(np.sum(d*d, axis=1))
    return np.exp(-np.mean(np.sort(dist)[:20]))

theta = np.unwrap(np.arctan2(traj[:,1], traj[:,0]))
omega = np.gradient(theta)
omega_mean = np.mean(omega)

# ----------------------------
# CONTROL MODES
# ----------------------------

def naive_vec(p, target):
    return unit(target - p)

def phase_vec(p, target):
    i, _ = nearest(p)
    t = tangent(i)
    return unit(0.7*t + 0.6*(target-p))

def nexah_vec(p, target):
    i, near = nearest(p)
    t = tangent(i)

    dens = density(p)
    gate = 1 - dens

    mismatch = abs(omega[i] - omega_mean)

    perp = np.array([-t[1], t[0]])

    v = (
        0.7*t
        + 0.1*(near - p)
        + 0.5*(gate*perp)
        + 0.4*(mismatch*perp)
        + 1.2*(target - p)
        + 1.0*(gate*unit(near - p))  # avoid
    )

    return unit(v)

# ----------------------------
# SIM
# ----------------------------

def simulate(start, target, mode):

    p = start.copy()
    path = [p.copy()]

    for _ in range(PRED_STEPS):

        if mode == "naive":
            v = naive_vec(p, target)
        elif mode == "phase":
            v = phase_vec(p, target)
        else:
            v = nexah_vec(p, target)

        p = p + STEP*v
        path.append(p.copy())

    return np.array(path)

# ----------------------------
# DOMAIN
# ----------------------------

xmin, xmax = cloud["c"].min(), cloud["c"].max()
ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

target = np.array([
    xmin + 0.7*(xmax-xmin),
    ymin + 0.6*(ymax-ymin)
])

# ----------------------------
# FIGURE (3 PANELS)
# ----------------------------

fig, axs = plt.subplots(1,3, figsize=(15,5))
titles = ["Naive Control", "Phase-Aware", "NEXAH Control"]

lines = []
dots = []

for ax, t in zip(axs, titles):
    ax.set_facecolor("black")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(t, color="white")

    l, = ax.plot([], [], lw=2)
    d = ax.scatter([], [], color="white", s=30)

    ax.scatter(*target, color="red", s=60)

    lines.append(l)
    dots.append(d)

# ----------------------------
# UPDATE
# ----------------------------

def update(frame):

    idx = min(frame*FRAME_SKIP + 40, len(traj)-1)
    sub = traj[:idx]
    current = sub[-1]

    modes = ["naive", "phase", "nexah"]

    for i, mode in enumerate(modes):
        path = simulate(current, target, mode)

        lines[i].set_data(path[:,0], path[:,1])
        dots[i].set_offsets([current])

    return lines + dots

# ----------------------------
# RUN
# ----------------------------

frames = min(len(traj)//FRAME_SKIP, MAX_FRAMES)

anim = FuncAnimation(fig, update, frames=frames, interval=40)

out = BASE_PATH / f"{CASE}_v10_comparison.gif"
anim.save(out, writer="pillow", fps=FPS)

print(f"[OK] saved → {out}")
