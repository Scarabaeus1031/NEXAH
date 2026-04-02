"""
NEXAH Resonance Maps — Final Closure Rad Lilith Tessa 17-29-5 v4.9
Penta im Hepta + Rosetta Cosmic Pulse Engine + XII Belts + Möbius Breathing
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

fig, ax = plt.subplots(1, 1, figsize=(14, 14))

# Heptagon (7er-Rad) – äußerer Rahmen
heptagon = RegularPolygon((0,0), numVertices=7, radius=1.45, 
                          orientation=np.pi/7, edgecolor='#4B0082', lw=4, fill=False)
ax.add_patch(heptagon)

# Pentagramm (Master)
theta = np.linspace(0, 2*np.pi, 500)
r_penta = 0.95 + 0.22 * np.sin(5 * theta)
ax.plot(r_penta * np.cos(theta), r_penta * np.sin(theta), 'b-', lw=4.5, label='Pentagramm (Master)')

# Kreis (Slave)
circle = plt.Circle((0,0), 1.0, color='gray', fill=False, lw=2.5, linestyle='--', label='Kreis (Slave)')
ax.add_patch(circle)

# 6 Punkte auf dem Kreis (2-3-1)
angles_6 = np.array([0, 60, 120, 180, 240, 300]) * np.pi / 180
colors_6 = ['red','green','blue','purple','orange','cyan']
for i, ang in enumerate(angles_6):
    ax.scatter(np.cos(ang), np.sin(ang), s=260, color=colors_6[i], edgecolor='white', linewidth=3, zorder=5)

# Ghostsnake Gegenrotation
r_ghost = 1.55 + 0.09 * np.sin(7 * theta)
ax.plot(r_ghost * np.cos(theta + 0.8), r_ghost * np.sin(theta + 0.8), 
        'magenta', lw=3, alpha=0.85, label='Ghostsnake (Gegenrotation)')

# XII Belts / Dodeca Gear (äußerste Schicht)
r_dodeca = 1.72
for i in range(12):
    ang = i * 2*np.pi/12
    ax.plot([0, r_dodeca*np.cos(ang)], [0, r_dodeca*np.sin(ang)], color='#C71585', lw=1.5, alpha=0.6)

# Lilith Tessa 17-29-5 Zentrum
ax.text(0, 0.08, "17-29-5\nLILITH TESSA", ha='center', va='center', fontsize=24, 
        fontweight='bold', color='#FFD700')
ax.text(0, -0.18, "1729\nHIDY", ha='center', va='center', fontsize=16, 
        fontweight='bold', color='gold')

ax.set_title("Final Closure Rad Lilith Tessa 17-29-5\nPenta im Hepta + Rosetta Cosmic Pulse Engine", fontsize=18)
ax.axis('equal')
ax.grid(True, alpha=0.25)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("final_closure_rad_lilith_tessa_v4.9.png", dpi=420, bbox_inches='tight')
print("📸 Final Closure Rad Lilith Tessa gespeichert als: final_closure_rad_lilith_tessa_v4.9.png")
plt.show()
