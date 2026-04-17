"""
NEXAH Trinity Experiment - Version 2.04
Mirror Iteration + 12-fold Operator around the Elastic Axis (F-Axis)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../outputs")
os.makedirs(output_dir, exist_ok=True)

# Figure
fig = plt.figure(figsize=(13, 10), dpi=140)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.04\n"
             "Mirror Iteration + 12-fold Operator\n"
             "F-Axis (Elastic Axis) as Attractor • Euler–Riemann–Ramanujan–Gauss", 
             fontsize=14, pad=30)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Light Root Cube
for s in [-1, 1]:
    ax.plot([s, s], [-1, 1], [-1, 1], color='gray', alpha=0.4, lw=0.8)
    ax.plot([-1, 1], [s, s], [-1, 1], color='gray', alpha=0.4, lw=0.8)
    ax.plot([-1, 1], [-1, 1], [s, s], color='gray', alpha=0.4, lw=0.8)

# Elastic Axis / F-Axis (Critical Line) – the Attractor
t = np.linspace(-1.4, 1.4, 400)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=6, label='F-Axis / Elastic Axis (Attractor)')

# "0" Markierung – nichts kann unter die 0 fallen
ax.text(0.1, 0.1, 0.2, '0', color='white', fontsize=16, weight='bold', ha='center')

# ----------------------------- Mirror Iteration (404 → 808 → ...) -----------------------------
mirror_points = []
mirror_values = [404, 808, 1616, 3232]
for i, val in enumerate(mirror_values):
    pos = (i - 1.5) * 0.6
    mirror_points.append((pos, pos, 0.1))

scat_mirror = ax.scatter(*zip(*mirror_points), color='magenta', s=80, label='Mirror Iteration (404→808→...)')

# ----------------------------- 12-fold Operator -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.18
x12 = radius * np.cos(theta)
y12 = radius * np.sin(theta)
z12 = np.zeros(12)

scat_12 = ax.scatter(x12, y12, z12, color='cyan', s=55, label='12-fold Operator (2×2×3)')

# ----------------------------- Trinity + Gauss -----------------------------
ax.scatter(0, 0, 0.15, color='red', s=140, label='Riemann')
ax.text(0.22, 0.22, 0.25, 'Riemann', color='red', fontsize=11)

ax.scatter(0.95, -0.7, 0.5, color='blue', s=110)
ax.text(1.05, -0.75, 0.55, 'Euler', color='blue', fontsize=11)

ax.scatter(-0.85, 0.9, -0.6, color='green', s=110)
ax.text(-0.95, 0.95, -0.65, 'Ramanujan', color='green', fontsize=11)

# Gauss als Handle auf der F-Axis
ax.scatter(0.5, 0.5, 0.12, color='orange', s=200, marker='o')
ax.text(0.62, 0.62, 0.22, 'Gauss\n(Handle)', color='orange', fontsize=11)

# 292 NCS Switch
ax.scatter(0.75, 0.75, 0.3, color='magenta', s=100, marker='s')
ax.text(0.82, 0.82, 0.38, '292 NCS Switch', color='magenta', fontsize=10)

# Animation
def update(frame):
    # 12-fold Rotation
    angle = frame * 4.0
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, z12)
    
    # Mirror Iteration Bewegung
    shift = np.sin(frame * 0.15) * 0.15
    new_pos = [(p[0] + shift, p[1] + shift, p[2]) for p in mirror_points]
    scat_mirror._offsets3d = tuple(zip(*new_pos))
    
    return scat_12, scat_mirror

ani = FuncAnimation(fig, update, frames=120, interval=50, blit=False)

ax.legend(loc='upper left', fontsize=9)
ax.view_init(elev=32, azim=42)

plt.tight_layout()

# Save
static_path = os.path.join(output_dir, "v2_04_mirror_iteration_static.png")
gif_path    = os.path.join(output_dir, "v2_04_mirror_iteration_animation.gif")

fig.savefig(static_path, dpi=220, bbox_inches='tight')
print(f"✓ Static image saved: {static_path}")

print("Saving animation GIF...")
ani.save(gif_path, writer='pillow', fps=20)
print(f"✓ Animation saved: {gif_path}")

plt.show()
