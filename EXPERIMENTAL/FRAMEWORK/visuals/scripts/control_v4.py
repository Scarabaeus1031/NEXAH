import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ----------------------------
# 1. Field
# ----------------------------
def F(x, y):
    return np.array([y, -x - 0.3*y])

# ----------------------------
# 2. Coherence
# ----------------------------
def coherence(x, dx):
    f = F(x[0], x[1])
    return np.dot(dx, f) / (np.linalg.norm(dx) * np.linalg.norm(f) + 1e-8)

# ----------------------------
# 3. Grid (Risk Field)
# ----------------------------
x_vals = np.linspace(-3, 3, 100)
y_vals = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x_vals, y_vals)

R = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        pos = np.array([X[i,j], Y[i,j]])
        dx = F(pos[0], pos[1])
        c = coherence(pos, dx)
        R[i,j] = 1 - c

# ----------------------------
# 4. Trajectory + Control Tracking
# ----------------------------
dt = 0.05
steps = 120

trajectory = []
coh_vals = []
control_points = []

x = np.array([-2.0, -1.5])

for i in range(steps):
    dx = F(x[0], x[1])
    c = coherence(x, dx)

    trajectory.append(x.copy())
    coh_vals.append(c)

    # 🔥 CONTROL LOGIC
    if c < 0.3:
        u = np.array([0.0, 0.6])
        control_points.append((x[0], x[1]))  # mark intervention
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (dx + u)

trajectory = np.array(trajectory)
coh_vals = np.array(coh_vals)
control_points = np.array(control_points) if len(control_points) > 0 else np.empty((0,2))

# ----------------------------
# 5. Plot + Animation
# ----------------------------
fig, ax = plt.subplots()

# Risk Heatmap
ax.imshow(
    R,
    extent=[-3, 3, -3, 3],
    origin='lower',
    alpha=0.6
)

# Trajectory
line, = ax.plot([], [], lw=2)

# Moving point
point, = ax.plot([], [], marker='o')

# Control points (static layer)
if len(control_points) > 0:
    ax.scatter(control_points[:,0], control_points[:,1], marker='x')

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

ax.set_title("NEXAH V4: Control & Intervention")

def update(frame):
    line.set_data(trajectory[:frame,0], trajectory[:frame,1])
    point.set_data([trajectory[frame,0]], [trajectory[frame,1]])
    return line, point

anim = FuncAnimation(fig, update, frames=len(trajectory), interval=60)

gif_path = "FRAMEWORK/visuals/output/nexah_v4_control.gif"
anim.save(gif_path, writer=PillowWriter(fps=15))

print("Saved:", gif_path)
