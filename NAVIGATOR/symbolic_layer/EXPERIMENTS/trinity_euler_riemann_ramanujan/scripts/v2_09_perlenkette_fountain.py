"""
NEXAH Trinity Experiment - Version 2.09
Perlenkette Fountain + Taxicab Regulator
12 pink pearls rise, spiral and fall around the Golden Axis
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../outputs")
os.makedirs(output_dir, exist_ok=True)

plt.style.use('dark_background')
fig = plt.figure(figsize=(14, 11), dpi=140, facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

ax.set_title("NEXAH Root Cube v2.09 — Perlenkette Fountain\n"
             "Golden Axis • Taxicab 1729 Regulator • 292 NCS Switch", 
             fontsize=14, pad=40, color='white')

ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_zlim(-1.8, 1.8)

# Stable Root Cube (big field)
for s in [-1.6, 1.6]:
    ax.plot([s, s], [-1.6, 1.6], [-1.6, 1.6], color='gray', alpha=0.25, lw=0.8)
    ax.plot([-1.6, 1.6], [s, s], [-1.6, 1.6], color='gray', alpha=0.25, lw=0.8)
    ax.plot([-1.6, 1.6], [-1.6, 1.6], [s, s], color='gray', alpha=0.25, lw=0.8)

# Golden / F-Axis
t = np.linspace(-1.7, 1.7, 600)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=7, label='Golden Axis (F-Axis)')

ax.text(0.1, 0.1, 0.45, '0', color='white', fontsize=20, weight='bold')

# Gauss + Riemann on Axis
ax.scatter(0.0, 0.0, 0.18, color='red', s=180)
ax.text(0.28, 0.28, 0.32, 'Riemann', color='red', fontsize=12, weight='bold')
ax.scatter(0.75, 0.75, 0.2, color='orange', s=220, marker='o')
ax.text(0.88, 0.88, 0.35, 'Gauss\n(Handle)', color='orange', fontsize=11)

# Taxicab 1729 Regulator (Fountain origin)
ax.scatter(0.0, 0.0, 0.0, color='magenta', s=200, marker='D')
ax.text(0.15, 0.15, 0.1, '1729\n(Taxicab Regulator)', color='magenta', fontsize=10)

# 292 NCS Switch (the pump)
ax.scatter(0.0, 0.0, 0.6, color='magenta', s=140, marker='s')
ax.text(0.12, 0.12, 0.7, '292 NCS\nSwitch', color='magenta', fontsize=11, weight='bold')

# ----------------------------- Perlenkette (12 pearls) -----------------------------
num_pearls = 12
pearl_z_base = np.linspace(0.1, 1.6, num_pearls)
scat_pearls = ax.scatter(np.zeros(num_pearls), np.zeros(num_pearls), pearl_z_base,
                         color='magenta', s=85, label='Perlenkette (Fountain)')

# Animation
def update(frame):
    t = frame * 0.035                     # sehr langsame, elegante Geschwindigkeit
    
    # Perlen bewegen sich wie eine aufsteigende / rotierende / fallende Kette
    angle = t + np.arange(num_pearls) * (2*np.pi / num_pearls)
    radius = 0.95 + 0.15 * np.sin(t * 1.2)   # leichte Pulsation
    
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    
    # Z-Höhe: aufsteigen, oben drehen, dann langsam abfallen
    z = 0.3 + 1.6 * (np.sin(t * 0.8 + np.arange(num_pearls) * 0.6) + 1) / 2
    
    scat_pearls._offsets3d = (x, y, z)
    return scat_pearls,

ani = FuncAnimation(fig, update, frames=240, interval=50, blit=False)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=35, azim=40)

plt.tight_layout()

# Save
static_path = os.path.join(output_dir, "v2_09_perlenkette_fountain_static.png")
gif_path    = os.path.join(output_dir, "v2_09_perlenkette_fountain_animation.gif")

fig.savefig(static_path, dpi=210, bbox_inches='tight')
print(f"✓ Static saved: {static_path}")

print("Saving GIF (ca. 25 Sekunden)...")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved: {gif_path}")

plt.show()
