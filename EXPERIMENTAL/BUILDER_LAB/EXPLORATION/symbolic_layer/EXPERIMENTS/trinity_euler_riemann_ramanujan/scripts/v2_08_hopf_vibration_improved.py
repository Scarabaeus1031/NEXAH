"""
NEXAH Trinity Experiment - Version 2.08
Hopf Vibration Improved + RATH Bridge
Black background • Stable Cube • Dynamic inner movement
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

# Figure with black background
plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 11), dpi=135, facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

ax.set_title("NEXAH Root Cube v2.08 — Hopf Vibration + RATH Bridge\n"
             "Stable Field • Dynamic Inner Movement • F-Axis Attractor", 
             fontsize=14, pad=40, color='white')

ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_zlim(-1.8, 1.8)

# Light stable Root Cube (big hexagon field)
for s in [-1.6, 1.6]:
    ax.plot([s, s], [-1.6, 1.6], [-1.6, 1.6], color='gray', alpha=0.3, lw=0.8)
    ax.plot([-1.6, 1.6], [s, s], [-1.6, 1.6], color='gray', alpha=0.3, lw=0.8)
    ax.plot([-1.6, 1.6], [-1.6, 1.6], [s, s], color='gray', alpha=0.3, lw=0.8)

# Golden / F-Axis (stable attractor)
t = np.linspace(-1.7, 1.7, 600)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=7, label='F-Axis (Elastic Axis)')

# 0 Markierung
ax.text(0.1, 0.1, 0.4, '0', color='white', fontsize=20, weight='bold')

# 3 Cubes (stable, slight pulsation later in animation)
cube_sizes = [0.6, 1.05, 1.55]
for size in cube_sizes:
    for s in [-size, size]:
        ax.plot([s, s], [-size, size], [-size, size], color='lightgray', alpha=0.4, lw=1)
        ax.plot([-size, size], [s, s], [-size, size], color='lightgray', alpha=0.4, lw=1)
        ax.plot([-size, size], [-size, size], [s, s], color='lightgray', alpha=0.4, lw=1)

# Fixed points on Golden Axis
ax.scatter(0.0, 0.0, 0.15, color='red', s=180)
ax.text(0.28, 0.28, 0.3, 'Riemann', color='red', fontsize=12, weight='bold')

ax.scatter(0.75, 0.75, 0.18, color='orange', s=220, marker='o')
ax.text(0.88, 0.88, 0.32, 'Gauss\n(Handle)', color='orange', fontsize=11)

# Taxicab 1729 Regulator
ax.scatter(0.4, 0.4, 0.45, color='magenta', s=170, marker='D')
ax.text(0.55, 0.55, 0.55, '1729\n(Taxicab Regulator)', color='magenta', fontsize=10)

# 292 NCS Switch
ax.scatter(0.95, 0.95, 0.4, color='magenta', s=140, marker='s')
ax.text(1.05, 1.05, 0.5, '292 NCS Switch', color='magenta', fontsize=11, weight='bold')

# 2² Pink Balls (moved by switch)
pink_balls = np.array([[-1.1,-1.1,0.1], [-0.45,-0.45,0.2], [0.55,0.55,0.25], [1.15,1.15,0.3]])
scat_pink = ax.scatter(pink_balls[:,0], pink_balls[:,1], pink_balls[:,2], color='magenta', s=95)

# Hopf Vibration (dense, dynamic, twisting fibers)
theta_h = np.linspace(0, 6*np.pi, 120)
hopf_x = 1.15 * np.cos(theta_h)
hopf_y = 1.15 * np.sin(theta_h)
hopf_z = 0.75 * np.sin(3 * theta_h)          # stronger twisting
scat_hopf = ax.scatter(hopf_x, hopf_y, hopf_z, color='cyan', s=8, alpha=0.75, label='Hopf Vibration (RATH Bridge)')

# Animation
def update(frame):
    # Slight cube pulsation
    pulse = 1 + 0.03 * np.sin(frame * 0.1)
    
    # 292 NCS Switch moves pink balls
    shift = np.sin(frame * 0.22) * 0.35
    new_pink = pink_balls.copy()
    new_pink[:,0] += shift * 0.9
    new_pink[:,1] += shift * 0.9
    scat_pink._offsets3d = (new_pink[:,0], new_pink[:,1], new_pink[:,2])
    
    # Hopf Vibration – strong dynamic twisting
    rot = frame * 0.15
    new_hx = 1.15 * np.cos(theta_h + rot)
    new_hy = 1.15 * np.sin(theta_h + rot)
    new_hz = 0.75 * np.sin(3 * theta_h + rot * 1.8)
    scat_hopf._offsets3d = (new_hx, new_hy, new_hz)
    
    return scat_pink, scat_hopf

ani = FuncAnimation(fig, update, frames=180, interval=45, blit=False)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=32, azim=42)

plt.tight_layout()

# Save
static_path = os.path.join(output_dir, "v2_08_hopf_vibration_improved_static.png")
gif_path    = os.path.join(output_dir, "v2_08_hopf_vibration_improved_animation.gif")

fig.savefig(static_path, dpi=210, bbox_inches='tight')
print(f"✓ Static saved: {static_path}")

print("Saving GIF (this will take ~20 seconds)...")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved: {gif_path}")

plt.show()
