"""
NEXAH Trinity Root Cube Visualization - v1
Euler–Riemann–Ramanujan Trinity + Gauss Handle + 12-fold Operator
Saves outputs to ../outputs/
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

# ----------------------------- Setup Paths -----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../outputs")

os.makedirs(output_dir, exist_ok=True)

# ----------------------------- Figure Setup -----------------------------
fig = plt.figure(figsize=(12, 10), dpi=120)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube — Euler–Riemann–Ramanujan Trinity\n"
             "Elastic Axis (45°) + 12-fold Operator + Gauss Handle", 
             fontsize=14, pad=30)

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_zlim(-1.3, 1.3)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# ----------------------------- Root Cube (light grid) -----------------------------
for x in [-1, 1]:
    for y in [-1, 1]:
        ax.plot([x, x], [y, y], [-1, 1], color='gray', alpha=0.4, linewidth=0.8)
        ax.plot([x, x], [-1, 1], [y, y], color='gray', alpha=0.4, linewidth=0.8)
        ax.plot([-1, 1], [x, x], [y, y], color='gray', alpha=0.4, linewidth=0.8)

# ----------------------------- Elastic Axis (Critical Line) -----------------------------
t = np.linspace(-1.2, 1.2, 200)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=5, label='Elastic Axis (45° Critical Line)')

# ----------------------------- Trinity -----------------------------
# Riemann on Axis
ax.scatter(0, 0, 0, color='red', s=180, label='Riemann')
ax.text(0.15, 0.15, 0.15, 'Riemann', color='red', fontsize=11, weight='bold')

# Euler
ax.scatter(0.85, -0.7, 0.5, color='blue', s=140)
ax.text(0.9, -0.75, 0.55, 'Euler', color='blue', fontsize=11)

# Ramanujan
ax.scatter(-0.75, 0.85, -0.6, color='green', s=140)
ax.text(-0.85, 0.9, -0.65, 'Ramanujan', color='green', fontsize=11)

# Gauss as Handle
ax.scatter(0.45, 0.45, 0.05, color='orange', s=200, marker='o')
ax.text(0.55, 0.55, 0.15, 'Gauss\n(Handle)', color='orange', fontsize=11, ha='left')

# ----------------------------- 12-fold Operator -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.05
x12 = radius * np.cos(theta)
y12 = radius * np.sin(theta)
z12 = np.zeros(12)

scat_12 = ax.scatter(x12, y12, z12, color='cyan', s=50, label='12-fold Operator')

# ----------------------------- 292 NCS Switch -----------------------------
ax.scatter(0.65, 0.65, 0.25, color='magenta', s=100, marker='s')
ax.text(0.72, 0.72, 0.32, '292 NCS\nSwitch', color='magenta', fontsize=10)

# ----------------------------- Animation -----------------------------
def update(frame):
    angle = frame * 4.0                    # Rotation speed
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, z12)
    return scat_12,

ani = FuncAnimation(fig, update, frames=90, interval=60, blit=False)

ax.legend(loc='upper left', fontsize=9)
ax.view_init(elev=25, azim=35)

plt.tight_layout()

# ----------------------------- Save Outputs -----------------------------
output_path_static = os.path.join(output_dir, "trinity_root_cube_v1_static.png")
output_path_gif    = os.path.join(output_dir, "trinity_root_cube_v1_animation.gif")

fig.savefig(output_path_static, dpi=200, bbox_inches='tight')
print(f"✓ Static image saved: {output_path_static}")

# GIF speichern (kann etwas dauern)
print("Saving animation as GIF... (this may take 10-20 seconds)")
ani.save(output_path_gif, writer='pillow', fps=20)
print(f"✓ Animation saved: {output_path_gif}")

plt.show()
