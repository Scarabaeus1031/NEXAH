import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ----------------------------
# Field
# ----------------------------
def F(x, y):
    return np.array([y, -x - 0.3*y])

# ----------------------------
# Coherence
# ----------------------------
def coherence(x, dx):
    f = F(x[0], x[1])
    return np.dot(dx, f) / (np.linalg.norm(dx) * np.linalg.norm(f) + 1e-8)

# ----------------------------
# Simulation
# ----------------------------
dt = 0.05
steps = 100
trajectory = []
coherence_values = []

x = np.array([-2.0, -1.5])

for _ in range(steps):
    dx = F(x[0], x[1])

    c = coherence(x, dx)
    coherence_values.append(c)

    trajectory.append(x.copy())

    # Control (leicht!)
    if c < 0.3:
        u = np.array([0.0, 0.4])
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (dx + u)

trajectory = np.array(trajectory)
coherence_values = np.array(coherence_values)

# ----------------------------
# Plot
# ----------------------------
fig, ax = plt.subplots()

x_vals = np.linspace(-3, 3, 20)
y_vals = np.linspace(-3, 3, 20)
X, Y = np.meshgrid(x_vals, y_vals)

U = Y
V = -X - 0.3*Y

ax.streamplot(X, Y, U, V)

line = ax.scatter([], [], c=[], cmap='RdYlGn', vmin=-1, vmax=1)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_title("Coherence Visualization")

def update(frame):
    pts = trajectory[:frame]
    colors = coherence_values[:frame]

    line.set_offsets(pts)
    line.set_array(colors)

    return (line,)

anim = FuncAnimation(fig, update, frames=len(trajectory), interval=80)

gif_path = "FRAMEWORK/visuals/output/nexah_v2_coherence.gif"
anim.save(gif_path, writer=PillowWriter(fps=12))

print("Saved:", gif_path)
