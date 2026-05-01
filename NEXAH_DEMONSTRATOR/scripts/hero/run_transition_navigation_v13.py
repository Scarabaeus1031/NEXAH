"""
NEXAH v13 — Transition-Aware Navigation

Shows:
- continuous dynamics (trajectory)
- coherence (color)
- discrete transitions (red markers)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("dark_background")


# ============================
# Lorenz System
# ============================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz(x):
    return np.array([
        sigma * (x[1] - x[0]),
        x[0] * (rho - x[2]) - x[1],
        x[0] * x[1] - beta * x[2]
    ])


# ============================
# Coherence + Risk
# ============================

def coherence(x, dx):
    dx_field = lorenz(x)
    num = np.dot(dx, dx_field)
    denom = np.linalg.norm(dx) * np.linalg.norm(dx_field) + 1e-8
    return num / denom


def risk(x, dx):
    return 1 - coherence(x, dx)


def grad_risk(x, dx, eps=1e-3):
    g = np.zeros(3)
    for i in range(3):
        shift = np.zeros(3)
        shift[i] = eps
        r1 = risk(x + shift, dx)
        r2 = risk(x - shift, dx)
        g[i] = (r1 - r2) / (2 * eps)
    return g


# ============================
# Sheet Structure (Discrete Layer)
# ============================

def sheet_index(x):
    r = np.linalg.norm(x[:2])  # radial projection
    return int(np.floor(r / 5.0))  # scaling important!


# ============================
# Simulation Parameters
# ============================

dt = 0.01
steps = 1500

noise_strength = 1.5
risk_strength = 0.35

x = np.array([1.0, 1.0, 1.0])

trajectory = []
coherences = []
transitions = []

prev_s = None


# ============================
# Simulation Loop
# ============================

for _ in range(steps):

    dx = lorenz(x)
    noise = noise_strength * np.random.randn(3)
    dx_obs = dx + noise

    # navigation via risk
    g = grad_risk(x, dx_obs)
    control = -risk_strength * g

    dx_total = dx_obs + control

    c = coherence(x, dx_total)

    x = x + dt * dx_total

    # sheet + transition detection
    s = sheet_index(x)

    if prev_s is not None and s != prev_s:
        transitions.append(x.copy())
    else:
        transitions.append(None)

    prev_s = s

    trajectory.append(x.copy())
    coherences.append(c)


trajectory = np.array(trajectory)
coherences = np.array(coherences)


# ============================
# Animation
# ============================

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')

line, = ax.plot([], [], [], lw=1)
transition_scatter = ax.scatter([], [], [], color='red', s=20)

ax.set_xlim(-20, 20)
ax.set_ylim(-30, 30)
ax.set_zlim(0, 50)

ax.set_title("NEXAH v13 — Transition-Aware Navigation")


def update(frame):

    traj = trajectory[:frame]
    coh = coherences[:frame]

    if len(traj) > 1:
        line.set_data(traj[:, 0], traj[:, 1])
        line.set_3d_properties(traj[:, 2])

        color = plt.cm.viridis((coh[-1] + 1) / 2)
        line.set_color(color)

    # transitions
    xs, ys, zs = [], [], []

    for t in transitions[:frame]:
        if t is not None:
            xs.append(t[0])
            ys.append(t[1])
            zs.append(t[2])

    transition_scatter._offsets3d = (xs, ys, zs)

    return line, transition_scatter


anim = FuncAnimation(fig, update, frames=steps, interval=20)


# ============================
# Save
# ============================

import os

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "visuals",
    "hero"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

output_path = os.path.join(OUTPUT_DIR, "nexah_transition_navigation_v13.gif")

anim.save(output_path, writer="pillow", fps=20)

plt.close()

print(f"✅ Saved: {output_path}")
