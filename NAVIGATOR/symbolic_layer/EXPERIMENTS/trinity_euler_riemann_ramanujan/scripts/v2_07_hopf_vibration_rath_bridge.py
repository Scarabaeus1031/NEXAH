"""
NEXAH Trinity Experiment - Version 2.07
Full Demo with Hopf Vibration + RATH Bridge
3 Cubes + Taxicab 1729 Regulator + Prime Generator
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../outputs")
os.makedirs(output_dir, exist_ok=True)

fig = plt.figure(figsize=(14, 11), dpi=135)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.07 — Hopf Vibration + RATH Bridge\n"
             "F-Axis + 3 Cubes + Taxicab Regulator • 2-1-3 Prime Generator", 
             fontsize=14, pad=40)

ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-2.0, 2.0)
ax.set_zlim(-2.0, 2.0)

# Light big hexagon field (Root Cube)
for s in [-1.6, 1.6]:
    ax.plot([s, s], [-1.6, 1.6], [-1.6, 1.6], color='gray', alpha=0.25, lw=0.6)
    ax.plot([-1.6, 1.6], [s, s], [-1.6, 1.6], color='gray', alpha=0.25, lw=0.6)
    ax.plot([-1.6, 1.6], [-1.6, 1.6], [s, s], color='gray', alpha=0.25, lw=0.6)

# Golden / F-Axis
t = np.linspace(-1.7, 1.7, 600)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=7, label='F-Axis (Elastic Axis)')

# 0 Markierung
ax.text(0.1, 0.1, 0.4, '0', color='white', fontsize=20, weight='bold')

# 3 Cubes (klein → mittel → groß)
cube_sizes = [0.55, 1.05, 1.6]
for i, size in enumerate(cube_sizes):
    c = ['lightblue', 'lightgreen', 'orange'][i]
    for s in [-size, size]:
        ax.plot([s,s], [-size,size], [-size,size], color=c, alpha=0.7, lw=1.1)
        ax.plot([-size,size], [s,s], [-size,size], color=c, alpha=0.7, lw=1.1)
        ax.plot([-size,size], [-size,size], [s,s], color=c, alpha=0.7, lw=1.1)

# Gauss + Riemann on Axis
ax.scatter(0.0, 0.0, 0.2, color='red', s=180)
ax.text(0.3, 0.3, 0.35, 'Riemann', color='red', fontsize=12, weight='bold')
ax.scatter(0.75, 0.75, 0.22, color='orange', s=220, marker='o')
ax.text(0.9, 0.9, 0.35, 'Gauss (Handle)', color='orange', fontsize=11)

# Taxicab 1729 Regulator
ax.scatter(0.4, 0.4, 0.5, color='magenta', s=160, marker='D')
ax.text(0.55, 0.55, 0.6, '1729\n(Taxicab Regulator)', color='magenta', fontsize=10)

# 292 NCS Switch (bewegt die pink balls)
ax.scatter(0.95, 0.95, 0.45, color='magenta', s=140, marker='s')
ax.text(1.05, 1.05, 0.55, '292 NCS Switch', color='magenta', fontsize=11, weight='bold')

# 2² Pink Balls
pink_balls = np.array([[-1.2,-1.2,0.1], [-0.55,-0.55,0.2], [0.65,0.65,0.3], [1.25,1.25,0.35]])
scat_pink = ax.scatter(pink_balls[:,0], pink_balls[:,1], pink_balls[:,2], color='magenta', s=90)

# Hopf Vibration (die blaue "Fabrik" Schicht)
theta_h = np.linspace(0, 4*np.pi, 80)
hopf_x = 0.9 * np.cos(theta_h)
hopf_y = 0.9 * np.sin(theta_h)
hopf_z = 0.6 * np.sin(2*theta_h)   # klassische Hopf-Vibration
scat_hopf = ax.scatter(hopf_x, hopf_y, hopf_z, color='cyan', s=12, alpha=0.7, label='Hopf Vibration (RATH Bridge)')

# 12-fold Operator
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
radius = 1.55
scat_12 = ax.scatter(radius*np.cos(theta), radius*np.sin(theta), np.zeros(12), color='cyan', s=45)

# 2-1-3 Labels
ax.text(-1.7, -1.3, 0.9, '2', color='cyan', fontsize=16)
ax.text(0.0, 0.7, 1.4, '1', color='white', fontsize=16)
ax.text(1.7, 1.3, -0.9, '3', color='cyan', fontsize=16)

def update(frame):
    angle = frame * 4.5
    # 12-fold
    rot_x = radius * np.cos(theta + np.deg2rad(angle))
    rot_y = radius * np.sin(theta + np.deg2rad(angle))
    scat_12._offsets3d = (rot_x, rot_y, np.zeros(12))
    
    # Pink Balls Bewegung durch 292 Switch
    shift = np.sin(frame * 0.18) * 0.32
    new_pink = pink_balls.copy()
    new_pink[:,0] += shift
    new_pink[:,1] += shift
    scat_pink._offsets3d = (new_pink[:,0], new_pink[:,1], new_pink[:,2])
    
    # Hopf Vibration Rotation
    rot_h = frame * 0.12
    new_hopf_x = 0.9 * np.cos(theta_h + rot_h)
    new_hopf_y = 0.9 * np.sin(theta_h + rot_h)
    new_hopf_z = 0.6 * np.sin(2*theta_h + rot_h)
    scat_hopf._offsets3d = (new_hopf_x, new_hopf_y, new_hopf_z)
    
    return scat_12, scat_pink, scat_hopf

ani = FuncAnimation(fig, update, frames=160, interval=45, blit=False)

ax.legend(loc='upper left', fontsize=9.5)
ax.view_init(elev=35, azim=38)

plt.tight_layout()

static_path = os.path.join(output_dir, "v2_07_hopf_vibration_rath_bridge_static.png")
gif_path    = os.path.join(output_dir, "v2_07_hopf_vibration_rath_bridge_animation.gif")

fig.savefig(static_path, dpi=210, bbox_inches='tight')
print(f"✓ Static saved: {static_path}")

print("Saving GIF...")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved: {gif_path}")

plt.show()
