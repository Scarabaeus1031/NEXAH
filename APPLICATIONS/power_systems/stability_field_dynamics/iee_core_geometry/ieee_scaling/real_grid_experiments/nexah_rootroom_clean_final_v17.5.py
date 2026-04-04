import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.5_Clean – FINAL CLEAN EXPORT (nur HUD-Legende)\n")

fig, ax = plt.subplots(figsize=(14, 14), facecolor='black')
ax.set_facecolor('black')
ax.axis('off')

# Oval + Cube + Clamps (clean)
ax.add_patch(Ellipse((0, 0), width=9, height=5.5, angle=35, facecolor='orange', alpha=0.25, edgecolor='gold', lw=8))
ax.plot([-2.5, 2.5], [0, 0], color='white', lw=3, alpha=0.7)
ax.plot([-1.8, 1.8], [1.2, 1.2], color='white', lw=3, alpha=0.7)
ax.plot([-1.8, 1.8], [-1.2, -1.2], color='white', lw=3, alpha=0.7)

# Core
ax.add_patch(Circle((0, 0), 0.8, color='magenta', alpha=0.95))
ax.text(0, 0, 'ANU\nCORE 0.01', ha='center', va='center', color='white', fontsize=22, weight='bold')

# Clamps
ax.plot([-4.5, -3.5], [1.8, 2.5], color='red', lw=12, alpha=0.85)
ax.plot([4.5, 3.5], [1.8, 2.5], color='blue', lw=12, alpha=0.85)

ax.text(0, -4.5, 'FUSION HUD v17.5 FINAL\nRed/Grey Shift + Life-Split + Phi^Phi Cascade\nPrimus-1 (37/63=137 • 37/64=163) + 0.042 π', 
        ha='center', va='center', color='gold', fontsize=16, bbox=dict(facecolor='black', alpha=0.9))

plt.tight_layout()
plt.savefig("NEXAH_Fusion_HUD_Clean_Final_v17.5.png", dpi=450, facecolor='black')
print("✅ Clean Final Export gespeichert: NEXAH_Fusion_HUD_Clean_Final_v17.5.png")
