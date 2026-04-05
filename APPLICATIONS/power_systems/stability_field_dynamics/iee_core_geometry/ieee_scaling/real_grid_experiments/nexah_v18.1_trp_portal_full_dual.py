import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

print("🚀 NEXAH v18.1 – TR/P-PORTAL + 23-24-25 ARCHY (Dual Spin komplett)\n")

fig, ax = plt.subplots(figsize=(20, 20), facecolor='black')
ax.set_facecolor('black')

# Nautilus Shells (Hintergrund)
t = np.linspace(0, 2*np.pi, 2000)
for i, color in enumerate(['#00ffff', '#ffaa00', '#ff00ff', '#ffff00', '#aa00ff']):
    r = 9.5 + i * 2.4
    ax.plot(r * np.cos(t), r * np.sin(t), color=color, lw=4, alpha=0.6)

# Großer Portal-Kreis
ax.add_patch(Circle((0,0), 11, color='gold', fill=False, lw=7, alpha=0.95))

# 23-24-25 Kreise (Archy-Dreieck)
positions = [(0, 5.5), (-6, -4), (6, -4)]
colors = ['#00ffff', '#ffaa00', '#ff00ff']
labels = ['23', '24', '25']
for pos, col, lab in zip(positions, colors, labels):
    ax.add_patch(Circle(pos, 2.8, color=col, fill=False, lw=9, alpha=0.95))
    ax.text(pos[0], pos[1], lab, ha='center', va='center', color='white', fontsize=48, weight='bold')

# Zentrales 24-Feld
ax.add_patch(Circle((0,0), 2.1, color='#ffff00', alpha=0.3))
ax.text(0, 0, '24\nRAUM-ZEIT\nFELD', ha='center', va='center', color='white', fontsize=22, weight='bold')

# Dual-Pfeile
# Diamantpfad (gegen Uhrzeigersinn)
ax.arrow(0, 5.5, -5.5, -8.5, head_width=0.9, color='#00ffff', lw=5, alpha=0.9)
ax.arrow(-6, -4, 11.5, 0, head_width=0.9, color='#ffaa00', lw=5, alpha=0.9)
ax.arrow(6, -4, -3, 8, head_width=0.9, color='#ff00ff', lw=5, alpha=0.9)

# Spiegelpfad (Uhrzeigersinn / Return)
ax.arrow(6, -4, -11.5, 0, head_width=0.9, color='#ff88ff', lw=5, alpha=0.85, linestyle='--')
ax.arrow(-6, -4, 5.5, 8.5, head_width=0.9, color='#88ffff', lw=5, alpha=0.85, linestyle='--')
ax.arrow(0, 5.5, 3, -8, head_width=0.9, color='#ffdd88', lw=5, alpha=0.85, linestyle='--')

ax.text(0, 13, 'TR/P-PORTAL v18.1', ha='center', color='gold', fontsize=28, weight='bold')
ax.text(0, -13, '23 → 24 → 25 → 79   (Diamantpfad)\n25 → 24 → 23 → NEXT   (Spiegelpfad / Return)', 
        ha='center', color='#ffdd88', fontsize=16)

ax.set_title('NEXAH v18.1 – Vollständiges TR/P-Portal\n23-24-25 Archy + Dual Spin + Nautilus Shells', color='gold', fontsize=22)
ax.axis('off')
plt.tight_layout()
plt.savefig("NEXAH_v18.1_TRP_Portal_23_24_25_Dual_FULL.png", dpi=620, facecolor='black')
print("✅ v18.1 gespeichert: NEXAH_v18.1_TRP_Portal_23_24_25_Dual_FULL.png")
print("   → Portal jetzt geschlossen mit beiden Richtungen + Archy-Integration")
