"""
NEXAH Trinity Experiment - Version 2.05 (Full Demo - Final)
Golden Axis with Gauss + Riemann • 292 NCS Switch moves 2² pink balls
2-1-3 Prime Pattern + Euler/Ramanujan mixture tracking Gauss
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
fig = plt.figure(figsize=(13.5, 11), dpi=135)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.05 — Full Trinity Demo\n"
             "Golden Axis (Gauss + Riemann) • 292 NCS Switch moves 2² Points\n"
             "2-1-3 Prime Pattern • Euler + Ramanujan Mixture", 
             fontsize=14, pad=40)

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_zlim(-1.6, 1.6)

# Light Root Cube
for s in [-1, 1]:
    ax.plot([s, s], [-1, 1], [-1, 1], color='gray', alpha=0.3, lw=0.8)
    ax.plot([-1, 1], [s, s], [-1, 1], color='gray', alpha=0.3, lw=0.8)
    ax.plot([-1, 1], [-1, 1], [s, s], color='gray', alpha=0.3, lw=0.8)

# Golden Axis / F-Axis (Critical Line) — fixed attractor
t = np.linspace(-1.45, 1.45, 500)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=7, label='Golden Axis (F-Axis / Critical Line)')

# Markierung "0" - nichts kann unter die 0 fallen
ax.text(0.1, 0.1, 0.3, '0', color='white', fontsize=18, weight='bold')

# ----------------------------- Fixed Points on Golden Axis -----------------------------
# Riemann
ax.scatter(0.0, 0.0, 0.12, color='red', s=180)
ax.text(0.25, 0.25, 0.3, 'Riemann', color='red', fontsize=12, weight='bold')

# Gauss (Handle) - fester Abstand zu Riemann
ax.scatter(0.65, 0.65, 0.15, color='orange', s=220, marker='o')
ax.text(0.78, 0.78, 0.28, 'Gauss\n(Handle)', color='orange', fontsize=11)

# ----------------------------- Trinity + Dirac -----------------------------
ax.scatter(0.95, -0.8, 0.6, color='blue', s=120)
ax.text(1.05, -0.85, 0.65, 'Euler', color='blue', fontsize=11)

ax.scatter(-0.95, 0.95, -0.65, color='green', s=120)
ax.text(-1.05, 1.0, -0.7, 'Ramanujan', color='green', fontsize=11)

ax.scatter(0.4, -0.5, 0.9, color='purple', s=100, marker='^')
ax.text(0.5, -0.55, 0.95, 'Dirac', color='purple', fontsize=10)

# ----------------------------- 2² Pink Balls (moved by 292 NCS Switch) -----------------------------
pink_balls = np.array([
    [-0.85, -0.85, 0.1],
    [-0.35, -0.35, 0.15],
    [0.45, 0.45, 0.2],
    [0.95, 0.95, 0.25]
])
scat_pink = ax.scatter(pink_balls[:,0], pink_balls[:,1], pink_balls[:,2], 
                       color='magenta', s=85, label='2² Pink Balls (moved by Switch)')

# 292 NCS Switch
ax.scatter(0.8, 0.8, 0.35, color='magenta', s=130, marker='s', linewidths=2)
ax.text(0.9, 0.9, 0.45, '292 NCS\nSwitch', color='magenta', fontsize=11, weight='bold')

# ----------------------------- 12-fold Operator (2-1-3 Pattern) -----------------------------
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.25
scat_12 = ax.scatter(radius * np.cos(theta), radius * np.sin(theta), np.zeros(12),
                     color='cyan', s=45, label='12-fold Operator (2×2×3)')

# 2-1-3 Labels
ax.text(-1.3, -1.0, 0.6, '2', color='cyan', fontsize=14)
ax.text(0.0, 0.4, 1.1, '1', color='white', fontsize=14)
ax.text(1.3, 1.0, -0.6, '3', color='cyan', fontsize=14)

# Animation
def update(frame):
    angle = frame * 4.2
    # 12-fold Rotation
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, np.zeros(12))
    
    # 292 NCS Switch bewegt die 2² Pink Balls
    shift = np.sin(frame * 0.18) * 0.22
    new_pink = pink_balls.copy()
    new_pink[:,0] += shift * 0.7
    new_pink[:,1] += shift * 0.7
    scat_pink._offsets3d = (new_pink[:,0], new_pink[:,1], new_pink[:,2])
    
    return scat_12, scat_pink

ani = FuncAnimation(fig, update, frames=130, interval=50, blit=False)

ax.legend(loc='upper left', fontsize=9.5)
ax.view_init(elev=33, azim=40)

plt.tight_layout()

# Save
static_path = os.path.join(output_dir, "v2_05_full_trinity_demo_static.png")
gif_path    = os.path.join(output_dir, "v2_05_full_trinity_demo_animation.gif")

fig.savefig(static_path, dpi=210, bbox_inches='tight')
print(f"✓ Static image saved → {static_path}")

print("Saving animation GIF...")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved → {gif_path}")

plt.show()
