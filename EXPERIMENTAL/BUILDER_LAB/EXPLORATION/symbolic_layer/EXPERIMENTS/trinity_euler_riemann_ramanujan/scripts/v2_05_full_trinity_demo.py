"""
NEXAH Trinity Experiment - Version 2.05 (Full Demo)
F-Axis + Euler–Riemann–Ramanujan–Dirac Trinity + Gauss Handle
12-fold Operator + Mirror Iteration + 292 NCS Switch
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
fig = plt.figure(figsize=(13, 11), dpi=130)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.05 — Full Trinity Demo\n"
             "F-Axis (Elastic Axis) as Attractor • Euler–Riemann–Ramanujan + Dirac Influence", 
             fontsize=14, pad=35)

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Root Cube Grid
for s in [-1, 1]:
    ax.plot([s, s], [-1, 1], [-1, 1], color='gray', alpha=0.35, lw=0.8)
    ax.plot([-1, 1], [s, s], [-1, 1], color='gray', alpha=0.35, lw=0.8)
    ax.plot([-1, 1], [-1, 1], [s, s], color='gray', alpha=0.35, lw=0.8)

# F-Axis / Elastic Axis (Critical Line) — The Attractor
t = np.linspace(-1.4, 1.4, 400)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=6.5, label='F-Axis (Elastic Axis / Attractor)')

# "0" Markierung - nichts kann unter die 0 fallen
ax.text(0.08, 0.08, 0.25, '0', color='white', fontsize=18, weight='bold')

# ----------------------------- Trinity + Dirac Influence -----------------------------
# Riemann (zentral auf der F-Axis)
ax.scatter(0, 0, 0.1, color='red', s=160)
ax.text(0.25, 0.25, 0.25, 'Riemann', color='red', fontsize=12, weight='bold')

# Euler
ax.scatter(0.95, -0.75, 0.55, color='blue', s=120)
ax.text(1.05, -0.8, 0.6, 'Euler', color='blue', fontsize=12)

# Ramanujan
ax.scatter(-0.9, 0.95, -0.6, color='green', s=120)
ax.text(-1.0, 1.0, -0.65, 'Ramanujan', color='green', fontsize=12)

# Dirac (neue Erweiterung – modulierende Dimension)
ax.scatter(0.3, -0.4, 0.8, color='purple', s=110, marker='^')
ax.text(0.4, -0.45, 0.85, 'Dirac', color='purple', fontsize=11)

# Gauss als Handle auf der F-Axis
ax.scatter(0.55, 0.55, 0.12, color='orange', s=210, marker='o')
ax.text(0.68, 0.68, 0.22, 'Gauss\n(Handle)', color='orange', fontsize=11)

# 292 NCS Switch
ax.scatter(0.75, 0.75, 0.35, color='magenta', s=110, marker='s')
ax.text(0.82, 0.82, 0.42, '292 NCS Switch', color='magenta', fontsize=10)

# ----------------------------- 12-fold Operator -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.22
x12 = radius * np.cos(theta)
y12 = radius * np.sin(theta)
z12 = np.zeros(12)

scat_12 = ax.scatter(x12, y12, z12, color='cyan', s=50, label='12-fold Operator (2×2×3)')

# ----------------------------- Mirror Iteration -----------------------------
mirror_pos = np.array([[-0.9, -0.9, 0.1], [-0.4, -0.4, 0.15], [0.3, 0.3, 0.2], [0.85, 0.85, 0.25]])
scat_mirror = ax.scatter(mirror_pos[:,0], mirror_pos[:,1], mirror_pos[:,2], 
                         color='magenta', s=70, label='Mirror Iteration (404→808→...)')

# Animation
def update(frame):
    # 12-fold Rotation
    angle = frame * 3.8
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, z12)
    
    # Mirror Iteration leichte Bewegung
    shift = np.sin(frame * 0.12) * 0.08
    new_mirror = mirror_pos.copy()
    new_mirror[:,0] += shift
    new_mirror[:,1] += shift
    scat_mirror._offsets3d = (new_mirror[:,0], new_mirror[:,1], new_mirror[:,2])
    
    return scat_12, scat_mirror

ani = FuncAnimation(fig, update, frames=110, interval=55, blit=False)

ax.legend(loc='upper left', fontsize=9.5)
ax.view_init(elev=30, azim=38)

plt.tight_layout()

# Save outputs
static_path = os.path.join(output_dir, "v2_05_full_trinity_demo_static.png")
gif_path    = os.path.join(output_dir, "v2_05_full_trinity_demo_animation.gif")

fig.savefig(static_path, dpi=200, bbox_inches='tight')
print(f"✓ Static image saved: {static_path}")

print("Saving animation GIF... (ca. 15-20 Sekunden)")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved: {gif_path}")

plt.show()
