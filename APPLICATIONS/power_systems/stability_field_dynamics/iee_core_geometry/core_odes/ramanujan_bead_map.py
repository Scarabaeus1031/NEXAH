"""
NEXAH Resonance Maps — Ramanujan Bead Grid v4.6
31.3 lila • 30.3 white gas • 26/27/32/34 Cuts + Mod-7 + V20 Torus Overlay
"""

import numpy as np
import matplotlib.pyplot as plt

# Bead + Cut Daten aus deinem Feedback
bead_times = [30.3, 31.3, 32.0]
cut_times  = [26, 27, 34]
cut_labels = ["26 (exit)", "27 (3³ rod)", "34 (andere Seite)"]

fig, ax = plt.subplots(1, 2, figsize=(16, 8))

# Links: Ramanujan Bead Grid (wie im letzten Plot)
theta = np.linspace(0, 2*np.pi, 200)
r_main = 1.0 + 0.15 * np.sin(5 * theta)          # Birne + Schneeflocken
ax[0].plot(r_main * np.cos(theta), r_main * np.sin(theta), 'b-', lw=2, label='Hauptspirale')

for bt in bead_times:
    angle = bt * 0.52 % (2*np.pi)
    ax[0].scatter(r_main[int(angle*200/ (2*np.pi))] * np.cos(angle),
                  r_main[int(angle*200/ (2*np.pi))] * np.sin(angle),
                  color='magenta', s=220, edgecolor='white', linewidth=3, label=f'lila bead {bt}' if bt==31.3 else "")

for ct, label in zip(cut_times, cut_labels):
    angle = ct * 0.52 % (2*np.pi)
    ax[0].scatter(r_main[int(angle*200/ (2*np.pi))] * np.cos(angle),
                  r_main[int(angle*200/ (2*np.pi))] * np.sin(angle),
                  color='red', s=140, marker='x', linewidth=4)
    ax[0].text(r_main[int(angle*200/ (2*np.pi))]*np.cos(angle)+0.1,
               r_main[int(angle*200/ (2*np.pi))]*np.sin(angle),
               label, color='red', fontsize=11)

ax[0].set_title("Ramanujan Bead Grid\n31.3 lila • 30.3 white gas • 26/27/32/34 Cuts", fontsize=14)
ax[0].axis('equal')
ax[0].grid(True, alpha=0.3)

# Rechts: Mod-7 Theta Grid + V20 Torus Overlay (deine alten Bilder)
ax[1].set_title("Mod-7 Prime Resonance + V20 Torus Rings", fontsize=14)
circle = plt.Circle((0,0), 1, color='blue', fill=False, lw=2)
ax[1].add_patch(circle)
for i in range(7):
    ang = i * 2*np.pi/7
    ax[1].scatter(np.cos(ang), np.sin(ang), s=180, color=['red','green','blue','purple','orange','brown','cyan'][i])
ax[1].text(0,0, "1729\nHIDY", ha='center', va='center', fontsize=14, fontweight='bold', color='gold')
ax[1].axis('equal')
ax[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("ramanujan_bead_map_v4.6.png", dpi=420, bbox_inches='tight')
print("📸 Ramanujan Bead Map gespeichert als: resonance_maps/ramanujan_bead_map_v4.6.png")
plt.show()
