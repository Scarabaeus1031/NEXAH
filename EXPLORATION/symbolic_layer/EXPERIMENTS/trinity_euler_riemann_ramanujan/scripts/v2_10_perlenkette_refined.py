"""
NEXAH Trinity Experiment - Version 2.10
Perlenkette Refined + Ramanujan Sprung
Taxicab 1729 als klarer Ebenen-Sprung-Regulator
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

ax.set_title("NEXAH Root Cube v2.10 — Perlenkette + Ramanujan Sprung\n"
             "Taxicab 1729 als Regulator • Golden Axis Attractor", 
             fontsize=14, pad=40, color='white')

ax.set_xlim(-1.8, 1.8)
ax.set_ylim(-1.8, 1.8)
ax.set_zlim(-1.8, 1.8)

# Stable Root Cube
for s in [-1.6, 1.6]:
    ax.plot([s, s], [-1.6, 1.6], [-1.6, 1.6], color='gray', alpha=0.25, lw=0.8)
    ax.plot([-1.6, 1.6], [s, s], [-1.6, 1.6], color='gray', alpha=0.25, lw=0.8)
    ax.plot([-1.6, 1.6], [-1.6, 1.6], [s, s], color='gray', alpha=0.25, lw=0.8)

# Golden Axis
t = np.linspace(-1.7, 1.7, 600)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=7)

ax.text(0.1, 0.1, 0.4, '0', color='white', fontsize=20, weight='bold')

# Riemann + Gauss auf der Axis
ax.scatter(0.0, 0.0, 0.18, color='red', s=180)
ax.text(0.28, 0.28, 0.32, 'Riemann', color='red', fontsize=12, weight='bold')
ax.scatter(0.75, 0.75, 0.2, color='orange', s=220, marker='o')
ax.text(0.88, 0.88, 0.35, 'Gauss (Handle)', color='orange', fontsize=11)

# Taxicab 1729 Regulator (Ramanujan Sprung Punkt)
ax.scatter(0.0, 0.0, 0.0, color='magenta', s=220, marker='D')
ax.text(0.2, 0.2, 0.1, '1729\n(Ramanujan Sprung)', color='magenta', fontsize=10)

# 292 NCS Switch
ax.scatter(0.0, 0.0, 0.65, color='magenta', s=140, marker='s')
ax.text(0.15, 0.15, 0.75, '292 NCS Switch', color='magenta', fontsize=11, weight='bold')

# Euler (wieder sichtbar)
ax.scatter(0.95, -0.8, 0.6, color='blue', s=120)
ax.text(1.05, -0.85, 0.65, 'Euler', color='blue', fontsize=11)

# 12 Perlen (Perlenkette)
num_pearls = 12
scat_pearls = ax.scatter(np.zeros(num_pearls), np.zeros(num_pearls), np.zeros(num_pearls),
                         color='magenta', s=85, alpha=0.9)

def update(frame):
    t = frame * 0.028   # sehr langsame, elegante Geschwindigkeit
    
    angle = t + np.arange(num_pearls) * (2*np.pi / num_pearls)
    radius = 1.05 + 0.12 * np.sin(t * 0.9)
    
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    
    # Z-Höhe: Fountain-Effekt mit Ramanujan-Sprung
    z = 0.3 + 1.65 * (np.sin(t * 0.75 + np.arange(num_pearls) * 0.55) + 1) / 2
    
    # Ramanujan-Sprung: wenn eine Perle nah am Taxicab-Punkt (0,0,0) ist, springt sie höher
    for i in range(num_pearls):
        dist_to_regulator = np.sqrt(x[i]**2 + y[i]**2 + z[i]**2)
        if dist_to_regulator < 0.25:
            z[i] += 0.6   # klarer Sprung nach oben
    
    # Spiegelung / Transparenz beim Axis-Crossing
    alpha = np.where(z > 0.3, 0.95, 0.45)   # obere Hälfte heller, untere dunkler
    
    scat_pearls._offsets3d = (x, y, z)
    scat_pearls.set_alpha(alpha)
    
    return scat_pearls,

ani = FuncAnimation(fig, update, frames=280, interval=55, blit=False)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=36, azim=40)

plt.tight_layout()

static_path = os.path.join(output_dir, "v2_10_perlenkette_refined_static.png")
gif_path    = os.path.join(output_dir, "v2_10_perlenkette_refined_animation.gif")

fig.savefig(static_path, dpi=210, bbox_inches='tight')
print(f"✓ Static saved: {static_path}")

print("Saving GIF...")
ani.save(gif_path, writer='pillow', fps=18)
print(f"✓ Animation saved: {gif_path}")

plt.show()
