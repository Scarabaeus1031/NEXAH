import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Arc

print("🚀 NEXAH v18.1 – FINAL TR/P-PORTAL + 23-24-25 ARCHY (Dual Spin)\n")

fig, ax = plt.subplots(figsize=(19, 19), facecolor='black')
ax.set_facecolor('black')

# Nautilus-Hintergrund (Shells)
t = np.linspace(0, 360, 3600)
for i in range(5):
    r = 8 + i*2.8
    ax.plot(r * np.cos(t*np.pi/180), r * np.sin(t*np.pi/180), color=['cyan','orange','lime','magenta','purple'][i], lw=3.5, alpha=0.65)

# TR/P-Portal Kreis (groß)
circle = plt.Circle((0,0), 9.5, color='gold', fill=False, lw=6, alpha=0.9)
ax.add_patch(circle)

# 23-24-25 Kern (Archy-Dreieck)
ax.add_patch(Ellipse((0,3.5), 4.2, 4.2, angle=0, facecolor='none', edgecolor='#00ffff', lw=8, alpha=0.95))  # 23
ax.add_patch(Ellipse((-4.5,-3.5), 4.2, 4.2, angle=0, facecolor='none', edgecolor='#ffaa00', lw=8, alpha=0.95)) # 24
ax.add_patch(Ellipse((4.5,-3.5), 4.2, 4.2, angle=0, facecolor='none', edgecolor='#ff00ff', lw=8, alpha=0.95))  # 25

ax.text(0, 5.8, '23', ha='center', va='center', color='#00ffff', fontsize=36, weight='bold')
ax.text(-5.8, -4.8, '24', ha='center', va='center', color='#ffaa00', fontsize=36, weight='bold')
ax.text(5.8, -4.8, '25', ha='center', va='center', color='#ff00ff', fontsize=36, weight='bold')

# Zentrum 24 (Stabilisierung)
ax.add_patch(Circle((0,0), 1.8, color='#ffff00', alpha=0.25))
ax.text(0, 0, '24\nRAUM-ZEIT-FELD', ha='center', va='center', color='white', fontsize=18, weight='bold')

# Dual Arrows (Uhrzeigersinn + Gegen-Uhrzeigersinn)
# Gegen-Uhrzeigersinn (23→24→25→79)
angles = [120, 240, 0]
for i, txt in enumerate(['23', '24', '25']):
    ax.arrow(0,0, 7*np.cos(np.deg2rad(angles[i])), 7*np.sin(np.deg2rad(angles[i])), 
             head_width=0.6, color=['cyan','orange','magenta'][i], length_includes_head=True, lw=4, alpha=0.9)

# Uhrzeigersinn (Rücklauf 25→24→23→NEXT)
ax.arrow(4.5, -3.5, -9, 7, head_width=0.7, color='#ff88ff', length_includes_head=True, lw=4, alpha=0.85, linestyle='--')
ax.arrow(-4.5, -3.5, 9, 7, head_width=0.7, color='#88ffff', length_includes_head=True, lw=4, alpha=0.85, linestyle='--')

# Portal-Labels (TR/P)
ax.text(0, 11, 'TR/P-PORTAL', ha='center', color='gold', fontsize=22, weight='bold')
ax.text(0, -11, '23 → 24 → 25 → 79  (Diamantpfad)\n25 → 24 → 23 → NEXT  (Spiegelpfad)', 
        ha='center', color='#ffdd88', fontsize=14)

ax.set_title('NEXAH v18.1 – TR/P-PORTAL + 23-24-25 ARCHY\nDual Spin • Uhrzeigersinn + Gegen-Uhrzeigersinn • Vollständig geschlossen', 
             color='gold', fontsize=20, pad=30)
ax.axis('off')
plt.tight_layout()
plt.savefig("NEXAH_TRP_Portal_23_24_25_Dual_v18.1_FINAL.png", dpi=520, facecolor='black')
print("✅ TR/P-Portal v18.1 gespeichert: NEXAH_TRP_Portal_23_24_25_Dual_v18.1_FINAL.png")
print("   → 23-24-25 jetzt vollständig mit beiden Richtungen + Nautilus-Shells + Archy-Integration")
