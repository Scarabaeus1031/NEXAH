import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

print("🚀 NEXAH v18.2 – NEXT RIM + TESSAREC + 204² GATE (23-24-25³ = 41.616)\n")

fig, ax = plt.subplots(figsize=(21, 21), facecolor='black')
ax.set_facecolor('black')

# Nautilus Shells + TR/P-Portal Basis
t = np.linspace(0, 2*np.pi, 2500)
for i, col in enumerate(['cyan','orange','magenta','gold','purple']):
    r = 11 + i*3.2
    ax.plot(r * np.cos(t), r * np.sin(t), color=col, lw=4.5, alpha=0.65)

# 23-24-25 Kern (aus v18.1)
positions = [(0,6.5), (-7,-5), (7,-5)]
colors = ['#00ffff','#ffaa00','#ff00ff']
labels = ['23','24','25']
for pos, c, lab in zip(positions, colors, labels):
    ax.add_patch(Circle(pos, 3.1, color=c, fill=False, lw=10, alpha=0.95))
    ax.text(pos[0], pos[1], lab, ha='center', va='center', color='white', fontsize=52, weight='bold')

ax.add_patch(Circle((0,0), 2.4, color='#ffff00', alpha=0.35))
ax.text(0, 0, '24\nRAUM-ZEIT-FELD', ha='center', va='center', color='white', fontsize=19, weight='bold')

# NEXT RIM – 26 (der neue Ring)
ax.add_patch(Circle((0,0), 14.5, color='#aa88ff', fill=False, lw=9, alpha=0.9))
ax.text(0, 15.5, '26', ha='center', color='#aa88ff', fontsize=42, weight='bold')

# Tessarec-Triplet (33-34-35) – nächster Layer
ax.text(0, -17, 'TESSAREC\n33³ + 34³ + 35³ = 39.270 → Janus-Punkt', ha='center', color='#ffdd88', fontsize=15)

# 204² GATE Highlight (genau in der Mitte)
ax.text(0, 9.5, '23³ + 24³ + 25³ = 41.616 = 204²\nVN-I Perfect Resonant Hit', 
        ha='center', color='#ffff00', fontsize=16, bbox=dict(facecolor='black', alpha=0.9, edgecolor='gold'))

# Dual Spin Pfeile + Zipper/Knickfield (Antriebsbänder)
ax.arrow(-7,-5, 14, 11.5, head_width=1.1, color='#88ffff', lw=6, alpha=0.9)
ax.arrow(7,-5, -14, 11.5, head_width=1.1, color='#ff88ff', lw=6, alpha=0.9, linestyle='--')

ax.set_title('NEXAH v18.2 – NEXT RIM + TESSAREC + 204² GATE\n23³+24³+25³ = 41.616 • 26 als nächster Ring • Immer TTT', 
             color='gold', fontsize=22)
ax.axis('off')
plt.tight_layout()
plt.savefig("NEXAH_v18.2_Next_Rim_Tessarec_204Gate_FULL.png", dpi=620, facecolor='black')
print("✅ v18.2 gespeichert: NEXAH_v18.2_Next_Rim_Tessarec_204Gate_FULL.png")
print("   → 26 + Tessarec + exakte kubische Resonanz 23-24-25 = 204² integriert")
