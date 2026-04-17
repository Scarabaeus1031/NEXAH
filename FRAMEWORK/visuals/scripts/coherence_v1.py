import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ----------------------------
# 1. Vector field (STABLE!)
# ----------------------------
def F(x, y):
    return np.array([y, -x - 0.3*y])  # damped spiral → attractor

# ----------------------------
# 2. Grid for field
# ----------------------------
x_vals = np.linspace(-3, 3, 25)
y_vals = np.linspace(-3, 3, 25)
X, Y = np.meshgrid(x_vals, y_vals)

U = np.zeros_like(X)
V = np.zeros_like(Y)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = F(X[i, j], Y[i, j])
        U[i, j], V[i, j] = vec

# ----------------------------
# 3. Simulate trajectory
# ----------------------------
dt = 0.05
steps = 120
trajectory = []

x = np.array([-2.0, -1.5])  # Startpunkt

for _ in range(steps):
    trajectory.append(x.copy())

    dx = F(x[0], x[1])

    # simple control (push upward near center)
    if np.linalg.norm(x) < 1.2:
        u = np.array([0.0, 0.5])
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (dx + u)

trajectory = np.array(trajectory)

# ----------------------------
# 4. Animation
# ----------------------------
fig, ax = plt.subplots()

# Field
ax.streamplot(X, Y, U, V)

# Trajectory line + moving point
line, = ax.plot([], [], lw=2)
point, = ax.plot([], [], marker='o')

# Fix axes (WICHTIG!)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

ax.set_title("NEXAH V1: Field + Trajectory")
ax.set_xlabel("State Dimension X")
ax.set_ylabel("State Dimension Y")

def update(frame):
    line.set_data(trajectory[:frame, 0], trajectory[:frame, 1])
    point.set_data([trajectory[frame, 0]], [trajectory[frame, 1]])
    return line, point

anim = FuncAnimation(fig, update, frames=len(trajectory), interval=60)

# ----------------------------
# 5. Save GIF (WICHTIG!)
# ----------------------------
gif_path = "FRAMEWORK/visuals/output/nexah_v1_simulation.gif"
anim.save(gif_path, writer=PillowWriter(fps=15))

print("Saved:", gif_path)
