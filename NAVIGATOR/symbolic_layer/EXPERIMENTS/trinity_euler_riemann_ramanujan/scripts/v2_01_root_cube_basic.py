"""
NEXAH Trinity Experiment - Version 2.01
Basic Root Cube + Elastic Axis (Critical Line)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../outputs")
os.makedirs(output_dir, exist_ok=True)

# Figure
fig = plt.figure(figsize=(11, 9), dpi=140)
ax = fig.add_subplot(111, projection='3d')
ax.set_title("NEXAH Root Cube v2.01\nElastic Axis (45° Critical Line)", fontsize=14, pad=25)

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.set_zlim(-1.4, 1.4)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Light Cube Grid
for s in [-1, 1]:
    ax.plot([s, s], [-1, 1], [-1, 1], color='gray', alpha=0.5, lw=0.8)
    ax.plot([-1, 1], [s, s], [-1, 1], color='gray', alpha=0.5, lw=0.8)
    ax.plot([-1, 1], [-1, 1], [s, s], color='gray', alpha=0.5, lw=0.8)

# Elastic Axis - Critical Line (45° Golden Line)
t = np.linspace(-1.3, 1.3, 300)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=6, label='Elastic Axis (45° Critical Line)')

# Markierung 45°
ax.text(0.8, 0.8, 0.1, '45°', color='gold', fontsize=12, weight='bold')

# 2-1-3 Prime Start Hinweis (leichte Markierungen)
ax.text(-1.1, -1.1, 0.3, '2', color='cyan', fontsize=11)
ax.text(0.0, 0.0, 0.4, '1', color='white', fontsize=11)
ax.text(1.1, 1.1, -0.3, '3', color='cyan', fontsize=11)

ax.legend(loc='upper left')
ax.view_init(elev=28, azim=40)

# Save
output_path = os.path.join(output_dir, "v2_01_root_cube_basic.png")
fig.savefig(output_path, dpi=220, bbox_inches='tight')
print(f"✓ Saved: {output_path}")

plt.show()
