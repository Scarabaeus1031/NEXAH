"""
NEXAH Trinity Experiment - Version 2.02
Root Cube + Elastic Axis + Euler–Riemann–Ramanujan Trinity + Gauss Handle
The Critical Line acts as the central attractor.
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
fig = plt.figure(figsize=(12, 10), dpi=140)
ax = fig.add_subplot(111, projection='3d')

ax.set_title("NEXAH Root Cube v2.02\n"
             "Elastic Axis (Critical Line) as Attractor\n"
             "Euler–Riemann–Ramanujan Trinity + Gauss Handle", 
             fontsize=14, pad=30)

ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.set_zlim(-1.4, 1.4)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Light Root Cube Grid
for s in [-1, 1]:
    ax.plot([s, s], [-1, 1], [-1, 1], color='gray', alpha=0.5, lw=0.8)
    ax.plot([-1, 1], [s, s], [-1, 1], color='gray', alpha=0.5, lw=0.8)
    ax.plot([-1, 1], [-1, 1], [s, s], color='gray', alpha=0.5, lw=0.8)

# Elastic Axis - Critical Line (45° Golden Line) → The Attractor
t = np.linspace(-1.3, 1.3, 300)
ax.plot(t, t, np.zeros_like(t), color='gold', linewidth=6, label='Elastic Axis / Critical Line (Attractor)')

# Markierung "0" auf der Achse (die Linie, unter die nichts fallen kann)
ax.text(0.05, 0.05, 0.15, '0', color='white', fontsize=14, weight='bold', ha='center')

# ----------------------------- Trinity -----------------------------
# Riemann — lies directly on the attractor (Critical Line)
ax.scatter(0, 0, 0.1, color='red', s=180, label='Riemann')
ax.text(0.2, 0.2, 0.2, 'Riemann', color='red', fontsize=12, weight='bold')

# Euler
ax.scatter(0.9, -0.65, 0.6, color='blue', s=140)
ax.text(0.95, -0.7, 0.65, 'Euler', color='blue', fontsize=12)

# Ramanujan
ax.scatter(-0.8, 0.9, -0.55, color='green', s=140)
ax.text(-0.9, 0.95, -0.6, 'Ramanujan', color='green', fontsize=12)

# Gauss as Handle — central stabilizing point on the attractor
ax.scatter(0.5, 0.5, 0.08, color='orange', s=220, marker='o', label='Gauss (Handle)')
ax.text(0.62, 0.62, 0.18, 'Gauss\n(Handle)', color='orange', fontsize=11, ha='left')

# Hinweis: "Nichts kann unter die 0 fallen"
ax.text(-1.2, -1.2, -1.0, '→ Critical Line as Attractor\n   Nothing falls below 0', 
        color='gold', fontsize=10, alpha=0.85)

# ----------------------------- 2-1-3 Prime Start Markierung -----------------------------
ax.text(-1.1, -0.3, 0.8, '2', color='cyan', fontsize=13, alpha=0.8)
ax.text(0.0, 0.3, 1.0, '1', color='white', fontsize=13, alpha=0.9)
ax.text(1.1, 0.4, -0.8, '3', color='cyan', fontsize=13, alpha=0.8)

ax.legend(loc='upper left', fontsize=10)
ax.view_init(elev=30, azim=45)

plt.tight_layout()

# Save
output_path = os.path.join(output_dir, "v2_02_trinity_gauss.png")
fig.savefig(output_path, dpi=220, bbox_inches='tight')
print(f"✓ Saved: {output_path}")

plt.show()
