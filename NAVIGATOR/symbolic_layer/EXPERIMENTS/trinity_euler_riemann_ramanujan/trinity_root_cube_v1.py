import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# ----------------------------- Setup -----------------------------
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("NEXAH Root Cube - Euler–Riemann–Ramanujan Trinity\nElastic Axis (45°) + 12-fold Operator", 
             fontsize=14, pad=30)

# Cube limits
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# ----------------------------- Root Cube -----------------------------
# Einfache Cube-Kanten
cube_edges = [
    [(-1,-1,-1), (1,-1,-1)], [(-1,-1,-1), (-1,1,-1)], [(-1,-1,-1), (-1,-1,1)],
    [(1,1,1), (-1,1,1)], [(1,1,1), (1,-1,1)], [(1,1,1), (1,1,-1)],
    # weitere Kanten...
]
for edge in cube_edges:
    xs, ys, zs = zip(*edge)
    ax.plot(xs, ys, zs, color='gray', alpha=0.6, linewidth=1)

# ----------------------------- Elastic Axis (45° Golden Line) -----------------------------
t = np.linspace(-1.1, 1.1, 100)
x_axis = t
y_axis = t
z_axis = np.zeros_like(t)
ax.plot(x_axis, y_axis, z_axis, color='gold', linewidth=4, label='Elastic Axis (45° Critical Line)')

# ----------------------------- Trinity Points -----------------------------
# Riemann auf der Axis
ax.scatter(0, 0, 0, color='red', s=120, label='Riemann (Axis)')
ax.text(0.1, 0.1, 0.1, 'Riemann', color='red')

# Euler
ax.scatter(0.8, -0.6, 0.4, color='blue', s=100, label='Euler')
ax.text(0.85, -0.65, 0.45, 'Euler', color='blue')

# Ramanujan
ax.scatter(-0.7, 0.9, -0.5, color='green', s=100, label='Ramanujan')
ax.text(-0.75, 0.95, -0.55, 'Ramanujan', color='green')

# Gauss als Handle (auf der Axis)
ax.scatter(0.4, 0.4, 0, color='orange', s=150, marker='o', label='Gauss (Handle)')
ax.text(0.5, 0.5, 0.1, 'Gauss\nHandle', color='orange', fontsize=10)

# ----------------------------- 12-fold Operator (rotierende Punkte) -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
r = 0.9
x12 = r * np.cos(theta)
y12 = r * np.sin(theta)
z12 = np.zeros(12)

scat_12 = ax.scatter(x12, y12, z12, color='cyan', s=40, label='12-fold Operator')

# ----------------------------- 292 NCS Switch -----------------------------
ax.scatter(0.6, 0.6, 0.2, color='magenta', s=80, marker='s', label='292 NCS Switch')
ax.text(0.65, 0.65, 0.25, '292 NCS\nSwitch', color='magenta')

# ----------------------------- Animation -----------------------------
def update(frame):
    angle = frame * 3  # langsame Rotation
    rot_x = r * np.cos(theta + np.deg2rad(angle))
    rot_y = r * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, z12)
    return scat_12,

ani = FuncAnimation(fig, update, frames=120, interval=50, blit=False)

ax.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.show()

# Optional: ani.save('trinity_root_cube.gif', writer='pillow', fps=20)
