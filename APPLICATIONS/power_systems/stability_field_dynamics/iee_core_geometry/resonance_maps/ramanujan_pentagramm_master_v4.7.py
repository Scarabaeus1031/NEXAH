"""
NEXAH Resonance Maps — Ramanujan Pentagramm Master v4.7
Pentagramm (Master) + Kreis (Slave) + Ghostsnake Gegenrotation
"""

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# Pentagramm (Master / Regulator) – Seestern-Form
theta = np.linspace(0, 2*np.pi, 500)
r_penta = 1.0 + 0.22 * np.sin(5 * theta)
x_penta = r_penta * np.cos(theta)
y_penta = r_penta * np.sin(theta)
ax.plot(x_penta, y_penta, 'b-', lw=3.5, label='Pentagramm (Master)')

# Kreis (Slave)
circle = plt.Circle((0,0), 1.0, color='gray', fill=False, lw=2, linestyle='--', label='Kreis (Slave)')
ax.add_patch(circle)

# 6 Punkte auf dem Kreis (2-3-1 Verteilung)
angles_6 = np.array([0, 60, 120, 180, 240, 300]) * np.pi / 180
colors_6 = ['red','green','blue','purple','orange','cyan']
for i, ang in enumerate(angles_6):
    ax.scatter(np.cos(ang), np.sin(ang), s=220, color=colors_6[i], edgecolor='white', linewidth=2.5)

# Ghostsnake Gegenrotation (magenta, außen)
r_ghost = 1.35 + 0.08 * np.sin(7 * theta)
ax.plot(r_ghost * np.cos(theta + 0.8), r_ghost * np.sin(theta + 0.8), 
        'magenta', lw=2.5, alpha=0.85, label='Ghostsnake (Gegenrotation)')

# 1729 HIDY Zentrum
ax.text(0, 0, "1729\nHIDY", ha='center', va='center', fontsize=18, 
        fontweight='bold', color='gold')

ax.set_title("Ramanujan Pentagramm Master\nSeestern + Ghostsnake + 6 Punkte (2-3-1)", fontsize=16)
ax.axis('equal')
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig("ramanujan_pentagramm_master_v4.7.png", dpi=420, bbox_inches='tight')
print("📸 Pentagramm Master gespeichert als: ramanujan_pentagramm_master_v4.7.png")
plt.show()
