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

GRID_RES = 40
FPS = 20
FRAME_SKIP = 2
MAX_FRAMES = 500
PRED_STEPS = 35

STEP = 0.03

# weights
A_LEARN = 0.7
A_RETURN = 0.1
A_PHASE = 0.4
A_GATE = 0.6
A_TARGET = 1.1
A_AVOID = 1.2

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
# HELPERS
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
# VECTOR FIELD
# ----------------------------

def field_vec(p, target):

    i, near = nearest(p)
    t = tangent(i)

    ret = near - p

    dens = density(p)
    gate = 1 - dens

    mismatch = abs(omega[i] - omega_mean)

    perp = np.array([-t[1], t[0]])

    gate_vec = gate * perp
    phase_vec = mismatch * perp

    control = target - p

    # gate avoidance
    avoid = gate * (unit(near - p))

    v = (
        A_LEARN * t
        + A_RETURN * ret
        + A_PHASE * phase_vec
        + A_GATE * gate_vec
        + A_TARGET * control
        + A_AVOID * avoid
    )

    return unit(v), gate * mismatch

# ----------------------------
# SIMULATION
# ----------------------------

def simulate(start, target):
    p = start.copy()
    path = [p.copy()]
    danger = []

    for _ in range(PRED_STEPS):
        v, d = field_vec(p, target)
        p = p + STEP * v
        path.append(p.copy())
        danger.append(d)

    return np.array(path), np.array(danger)

# ----------------------------
# GRID
# ----------------------------

xmin, xmax = cloud["c"].min(), cloud["c"].max()
ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

xs = np.linspace(xmin, xmax, GRID_RES)
ys = np.linspace(ymin, ymax, GRID_RES)
X, Y = np.meshgrid(xs, ys)

# ----------------------------
# TARGET
# ----------------------------

target = np.array([
    xmin + 0.7*(xmax-xmin),
    ymin + 0.6*(ymax-ymin)
])

# ----------------------------
# PLOT
# ----------------------------

fig, ax = plt.subplots(figsize=(7,7))
ax.set_facecolor("black")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xticks([]); ax.set_yticks([])

heat = ax.imshow(
    np.zeros_like(X),
    origin="lower",
    cmap="inferno",
    alpha=0.7,
    extent=[xmin,xmax,ymin,ymax]
)

trail, = ax.plot([], [], "w-", lw=2)
safe, = ax.plot([], [], "c-", lw=2)
naive, = ax.plot([], [], "orange", lw=1, linestyle="--")

dot = ax.scatter([], [], color="white", s=40)
ax.scatter(*target, color="red", s=80)

title = ax.text(0.5,1.02,"", transform=ax.transAxes, ha="center", color="white")

# ----------------------------
# UPDATE
# ----------------------------

def update(frame):

    idx = min(frame*FRAME_SKIP+30, len(traj)-1)
    sub = traj[:idx]

    trail.set_data(sub[:,0], sub[:,1])

    current = sub[-1]

    path, danger = simulate(current, target)

    safe.set_data(path[:,0], path[:,1])

    # naive straight line
    naive_path = np.linspace(current, target, PRED_STEPS)
    naive.set_data(naive_path[:,0], naive_path[:,1])

    dot.set_offsets([current])

    # heatmap
    A = np.zeros_like(X)
    for i in range(GRID_RES):
        for j in range(GRID_RES):
            _, d = field_vec(np.array([X[i,j], Y[i,j]]), target)
            A[i,j] = d

    A = A/(np.max(A)+1e-8)
    heat.set_data(A)

    title.set_text(f"NEXAH V9 — Gate-aware Control · t={idx}")

    return trail, safe, naive, dot, heat, title

# ----------------------------
# RUN
# ----------------------------

frames = min(len(traj)//FRAME_SKIP, MAX_FRAMES)

anim = FuncAnimation(fig, update, frames=frames, interval=40)

out = BASE_PATH / f"{CASE}_v9_transition_field.gif"
anim.save(out, writer="pillow", fps=FPS)

print(f"[OK] saved → {out}")
