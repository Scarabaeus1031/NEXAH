"""
NEXAH Trinity Experiment - Version 2.06
3 Cubes + Taxicab 1729 Regulator + Prime Generator (2-1-3 +1)
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
fig = plt.figure(figsize=(14, 11), dpi=135)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.06\n"
             "3 Cubes + Taxicab 1729 Regulator • 2-1-3 Prime Generator", 
             fontsize=14, pad=40)

ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_zlim(-1.8, 1.8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Light Root Cube Grid (big hexagon field)
for s in [-1.5, 1.5]:
    ax.plot([s, s], [-1.5, 1.5], [-1.5, 1.5], color='gray', alpha=0.25, lw=0.6)
    ax.plot([-1.5, 1.5], [s, s], [-1.5, 1.5], color='gray', alpha=0.25, lw=0.6)
    ax.plot([-1.5, 1.5], [-1.5, 1.5], [s, s], color='gray', alpha=0.25, lw=0.6)

# Golden Axis / F-Axis (Critical Line)
t = np.linspace(-1.6, 1.6, 500)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=7, label='Golden Axis (F-Axis)')

ax.text(0.1, 0.1, 0.4, '0', color='white', fontsize=18, weight='bold')

# ----------------------------- 3 Cubes ( +1 Regulator ) -----------------------------
cube_sizes = [0.6, 1.0, 1.45]
colors = ['lightblue', 'lightgreen', 'orange']

for i, size in enumerate(cube_sizes):
    # Draw simple cube edges
    for s in [-size, size]:
        ax.plot([s, s], [-size, size], [-size, size], color=colors[i], alpha=0.6, lw=1.2)
        ax.plot([-size, size], [s, s], [-size, size], color=colors[i], alpha=0.6, lw=1.2)
        ax.plot([-size, size], [-size, size], [s, s], color=colors[i], alpha=0.6, lw=1.2)

# ----------------------------- Fixed Points on Golden Axis -----------------------------
# Riemann
ax.scatter(0.0, 0.0, 0.15, color='red', s=180)
ax.text(0.25, 0.25, 0.3, 'Riemann', color='red', fontsize=12, weight='bold')

# Gauss (Handle)
ax.scatter(0.72, 0.72, 0.18, color='orange', s=220, marker='o')
ax.text(0.85, 0.85, 0.3, 'Gauss\n(Handle)', color='orange', fontsize=11)

# ----------------------------- Taxicab 1729 Regulator -----------------------------
ax.scatter(0.35, 0.35, 0.4, color='magenta', s=180, marker='D')
ax.text(0.48, 0.48, 0.5, '1729\n(Taxicab Regulator)', color='magenta', fontsize=10, ha='left')

# ----------------------------- 2² Pink Balls (moved by 292 NCS Switch) -----------------------------
pink_balls = np.array([
    [-1.1, -1.1, 0.1],
    [-0.5, -0.5, 0.2],
    [0.6, 0.6, 0.25],
    [1.15, 1.15, 0.3]
])
scat_pink = ax.scatter(pink_balls[:,0], pink_balls[:,1], pink_balls[:,2], 
                       color='magenta', s=90, label='2² Pink Balls')

# 292 NCS Switch
ax.scatter(0.9, 0.9, 0.4, color='magenta', s=140, marker='s', linewidths=2)
ax.text(1.0, 1.0, 0.5, '292 NCS Switch', color='magenta', fontsize=11, weight='bold')

# ----------------------------- 12-fold Operator + 2-1-3 -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.4
scat_12 = ax.scatter(radius * np.cos(theta), radius * np.sin(theta), np.zeros(12),
                     color='cyan', s=50, label='12-fold Operator')

# 2-1-3 Labels
ax.text(-1.5, -1.2, 0.8, '2', color='cyan', fontsize=15)
ax.text(0.0, 0.6, 1.2, '1', color='white', fontsize=15)
ax.text(1.5, 1.2, -0.8, '3', color='cyan', fontsize=15)

# Animation
def update(frame):
    angle = frame * 4.0
    # 12-fold Rotation
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, np.zeros(12))
    
    # 292 NCS Switch bewegt die 2² Pink Balls
    shift = np.sin(frame * 0.16) * 0.28
    new_pink = pink_balls.copy()
    new_pink[:,0] += shift * 0.8
    new_pink[:,1] += shift * 0.8
    scat_pink._offsets3d = (new_pink[:,0], new_pink[:,1], new_pink[:,2])
    
    return scat_12, scat_pink

ani = FuncAnimation(fig, update, frames=140, interval=50, blit=False)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=32, azim=35)

plt.tight_layout()

# Save
static_path = os.path.join(output_dir, "v2_06_3_cubes_taxicab_regulator_static.png")
gif_path    = os.path.join(output_dir, "v2_06_3_cubes_taxicab_regulator_animation.gif")

fig.savefig(static_path, dpi=210, bbox_inches='tight')
print(f"✓ Static image saved: {static_path}")

print("Saving animation GIF...")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved: {gif_path}")

plt.show()
