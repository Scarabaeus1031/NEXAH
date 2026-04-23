"""
NEXAH Trinity Experiment - Version 2.03
12-fold Operator Visualization
2 × 2 × 3 = 12  →  Prime Start Pattern 2-1-3
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
fig = plt.figure(figsize=(12, 10), dpi=140)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.03\n"
             "12-fold Operator • 2 × 2 × 3 = 12\n"
             "Prime Start Pattern 2-1-3 around the Elastic Axis", 
             fontsize=14, pad=30)

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.set_zlim(-1.4, 1.4)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Light Root Cube Grid
for s in [-1, 1]:
    ax.plot([s, s], [-1, 1], [-1, 1], color='gray', alpha=0.4, lw=0.8)
    ax.plot([-1, 1], [s, s], [-1, 1], color='gray', alpha=0.4, lw=0.8)
    ax.plot([-1, 1], [-1, 1], [s, s], color='gray', alpha=0.4, lw=0.8)

# Elastic Axis - Critical Line (Attractor)
t = np.linspace(-1.3, 1.3, 300)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=5, label='Elastic Axis (Critical Line)')

# 2-1-3 Prime Start Labels
ax.text(-1.15, -1.15, 0.4, '2', color='cyan', fontsize=14, weight='bold')
ax.text(0.05, 0.05, 0.6, '1', color='white', fontsize=14, weight='bold')
ax.text(1.15, 1.15, -0.4, '3', color='cyan', fontsize=14, weight='bold')

# ----------------------------- 12-fold Operator -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.12

x12 = radius * np.cos(theta)
y12 = radius * np.sin(theta)
z12 = np.zeros(12)

scat_12 = ax.scatter(x12, y12, z12, color='cyan', s=60, label='12-fold Operator')

# Markierung der 12
ax.text(0, 1.25, 0.1, '12', color='cyan', fontsize=13, alpha=0.9)

# ----------------------------- Trinity & Gauss (static) -----------------------------
# Riemann
ax.scatter(0, 0, 0.05, color='red', s=120)
ax.text(0.2, 0.2, 0.15, 'Riemann', color='red', fontsize=10)

# Euler
ax.scatter(0.85, -0.7, 0.4, color='blue', s=100)
ax.text(0.95, -0.75, 0.45, 'Euler', color='blue', fontsize=10)

# Ramanujan
ax.scatter(-0.75, 0.85, -0.5, color='green', s=100)
ax.text(-0.85, 0.9, -0.55, 'Ramanujan', color='green', fontsize=10)

# Gauss as Handle
ax.scatter(0.45, 0.45, 0.1, color='orange', s=180, marker='o')
ax.text(0.58, 0.58, 0.2, 'Gauss\n(Handle)', color='orange', fontsize=10)

# 292 NCS Switch
ax.scatter(0.7, 0.7, 0.25, color='magenta', s=90, marker='s')
ax.text(0.78, 0.78, 0.32, '292 NCS Switch', color='magenta', fontsize=9)

# Animation
def update(frame):
    angle = frame * 3.5
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, z12)
    return scat_12,

ani = FuncAnimation(fig, update, frames=100, interval=50, blit=False)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=28, azim=40)

plt.tight_layout()

# Save outputs
static_path = os.path.join(output_dir, "v2_03_12fold_operator_static.png")
gif_path    = os.path.join(output_dir, "v2_03_12fold_operator_animation.gif")

fig.savefig(static_path, dpi=220, bbox_inches='tight')
print(f"✓ Static image saved: {static_path}")

print("Saving animation GIF... (this may take ~15 seconds)")
ani.save(gif_path, writer='pillow', fps=20)
print(f"✓ Animation saved: {gif_path}")

plt.show()
