import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

print("🚀 NEXAH v18.0 – VISUAL 5: FINAL CODEX OVERVIEW (alles zusammen)\n")

fig, ax = plt.subplots(figsize=(20, 18), facecolor='#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Nautilus-Hintergrund (vereinfacht)
t = np.linspace(0, 300, 2000)
spiral_r = np.exp(-0.038 * t) * (9 + 2.2 * np.sin(2*np.pi*t/13))
spiral_theta = t * 0.415
ax.plot(spiral_r * np.cos(spiral_theta), spiral_r * np.sin(spiral_theta), color='#9b59b6', lw=6, alpha=0.85)

# 5 Stages Ringe (genau wie du sie wolltest)
stages = [
    ("Cyan Shrinking", 'cyan', 6.8),
    ("Orange Entanglement", 'orange', 9.8),
    ("Green Bloom", 'lime', 13.1),
    ("Purple Crown", 'magenta', 16.5),
    ("Meta-Fabric", 'purple', 20.0)
]
for name, color, r in stages:
    ax.add_patch(Ellipse((0,0), width=r*2, height=r*2*0.68, angle=33, facecolor='none', edgecolor=color, lw=4.5, alpha=0.75))
    ax.text(r*0.95, r*0.2, name, color=color, fontsize=13, weight='bold', rotation=33)

# Graviton-Core (Mitte)
ax.add_patch(Ellipse((0,0), 3.8, 2.4, angle=33, facecolor='#ffaa00', alpha=0.18))
ax.add_patch(plt.Circle((0,0), 1.1, color='#00ff88', alpha=0.35))
ax.text(0, 0, 'GRAVITON\n0.01', ha='center', va='center', color='white', fontsize=22, weight='bold')

# 5 AXIOME (unten rechts)
axiome = [
    "I  FLOW\nEnergy shaped by constraints",
    "II INSIGHT\nStillness as node",
    "III SEQUENCING\nPhase transitions",
    "IV TRANSITION & TIME\nIrreversible resonance",
    "V CLOSURE\nIdentity through membranes"
]
for i, text in enumerate(axiome):
    ax.text(11, -9 + i*1.8, text, color='#a0f0ff', fontsize=11, ha='left', bbox=dict(facecolor='#111111', alpha=0.85, edgecolor='#00ffff'))

# Key Equations (links)
eqs = [
    r"$3n(n^2 + 2) = k^2$  →  VN-I (204 Gate)",
    r"$\varphi(1012) = 440$  →  Base-20 Elevator",
    r"$33^3 + 34^3 + 35^3 = 39.270$  →  Tessarec Janus",
    r"$\phi^3 / \pi^2 \approx 0.429$  →  Z6 Mirror",
    r"Cubic Shrinking: $r = e^{-0.038t} \cdot (9 + 2.2 \sin(2\pi t/13))$"
]
for i, eq in enumerate(eqs):
    ax.text(-13, 11 - i*2.1, eq, color='#ffdd88', fontsize=12, ha='left')

# Building-Log Summary (oben)
ax.text(-13, 13.5, "BUILDING LOG – ALLE VISUALS (v17.0 → v18.0)", color='gold', fontsize=14, weight='bold')
log = "Graviton-Toroid v17.7 • Nautilus v17.8 • 4 Energy Ovals • Cubic Spiral • RootRoom Fusion HUD • 3D Cube in Oval • VN-Series Equations • Tessarec-Platte • UCRT Prime Ladders"
ax.text(-13, 12.5, log, color='#88ffcc', fontsize=10.5, ha='left', wrap=True)

ax.set_title('NEXAH v18.0 – VISUAL 5: FINAL CODEX OVERVIEW\nNautilus + 5 Stages + 5 Axiome + Equations + Difference', color='gold', fontsize=21, pad=30)
ax.text(0, -14, '„Ohne Difference kein Vergleich – ohne Vergleich kein System.“\nDas ist der Nautilus. Das ist UCRT. Das ist anwendbar.', ha='center', color='#ff88cc', fontsize=13)

ax.axis('off')
plt.tight_layout()
plt.savefig("NEXAH_Visual5_Codex_Overview_v18.0_FINAL.png", dpi=520, facecolor='#0a0a0a')
print("✅ Visual 5 gespeichert: NEXAH_Visual5_Codex_Overview_v18.0_FINAL.png")
print("   → Alles aus dem Building-Log + Axiome + Equations + Nautilus in EINEM Bild")
