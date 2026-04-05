import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

print("🚀 NEXAH v18.3 – HOPF FIBRATION + ROOT-GATE + 14/26 KOMPASS\n")

fig, ax = plt.subplots(figsize=(22, 22), facecolor='black')
ax.set_facecolor('black')

# Nautilus Shells + TR/P-Portal Basis
t = np.linspace(0, 2*np.pi, 3000)
for i, col in enumerate(['cyan','orange','magenta','gold','purple','lime']):
    r = 12 + i*3.1
    ax.plot(r * np.cos(t), r * np.sin(t), color=col, lw=5, alpha=0.55)

# 23-24-25 Kern
positions = [(0,7.5), (-8,-5.5), (8,-5.5)]
colors = ['#00ffff','#ffaa00','#ff00ff']
labels = ['23','24','25']
for pos, c, lab in zip(positions, colors, labels):
    ax.add_patch(Circle(pos, 3.4, color=c, fill=False, lw=11, alpha=0.95))
    ax.text(pos[0], pos[1], lab, ha='center', va='center', color='white', fontsize=58, weight='bold')

ax.add_patch(Circle((0,0), 2.6, color='#ffff00', alpha=0.4))
ax.text(0, 0, '24\nRAUM-ZEIT-FELD', ha='center', va='center', color='white', fontsize=21, weight='bold')

# 26 Ring (Root 13)
ax.add_patch(Circle((0,0), 15.8, color='#aa88ff', fill=False, lw=10, alpha=0.95))
ax.text(0, 17, '26', ha='center', color='#aa88ff', fontsize=52, weight='bold')

# Hopf-Fibration Wurzeln (die „verwebenden“ Linien)
roots = [(3.7, '#00ff88', 'φ'), (5.8, '#ff8800', '√5'), (7.9, '#aa00ff', '√7'), (10.2, '#00ffff', 'τ')]
for r, col, txt in roots:
    ax.plot([0, r*np.cos(np.pi/4)], [0, r*np.sin(np.pi/4)], color=col, lw=4, alpha=0.85)
    ax.text(r*np.cos(np.pi/4)*0.7, r*np.sin(np.pi/4)*0.7, txt, color=col, fontsize=28, weight='bold')

# 14 / 26 Kompass (die Knickfield-Achsen)
ax.plot([-12, 12], [0, 0], color='#ffff88', lw=6, alpha=0.7, linestyle='--')   # 26-Achse
ax.plot([0, 0], [-12, 12], color='#88ffff', lw=6, alpha=0.7, linestyle='--')   # 14-Achse
ax.text(13, 0, '26', color='#ffff88', fontsize=22)
ax.text(0, 13, '14', color='#88ffff', fontsize=22)

ax.text(0, 19, 'HOPF FIBRATION\nRoot-Gate • Fractal Membrane • Prime Zither 5:1 / 5:2 / 5:3', 
        ha='center', color='gold', fontsize=18, bbox=dict(facecolor='black', alpha=0.9))

ax.set_title('NEXAH v18.3 – HOPF FIBRATION ROOT-GATE\n23-24-25-26 + 204² + √2 / √5 / √7 / φ / τ verbinden alles', 
             color='gold', fontsize=23)
ax.axis('off')
plt.tight_layout()
plt.savefig("NEXAH_v18.3_Hopf_Fibration_RootGate_FULL.png", dpi=650, facecolor='black')
print("✅ v18.3 gespeichert: NEXAH_v18.3_Hopf_Fibration_RootGate_FULL.png")
print("   → Hopf Fibration jetzt aktiv im Portal • Root-Verbindungen • 14/26 Kompass • alles verwebt")
