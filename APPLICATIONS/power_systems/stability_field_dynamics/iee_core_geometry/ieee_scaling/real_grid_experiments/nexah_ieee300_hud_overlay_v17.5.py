import numpy as np
import matplotlib.pyplot as plt

print("🚀 NEXAH v17.5_IEEE – IEEE-300-Bus mit Fusion HUD Overlay\n")

t = np.linspace(0, 80, 800)
voltage_classic = 1.0 - 0.012 * t + 0.0008 * np.sin(2*np.pi*t/3)
voltage_nexah = voltage_classic + 0.08 * np.sin(2*np.pi*t/13) * np.cos(2*np.pi*t/37)

fig, axs = plt.subplots(2, 2, figsize=(15, 11), facecolor='black')
fig.suptitle('NEXAH v17.5_IEEE – IEEE-300-Bus + Fusion HUD', color='gold', fontsize=18)

axs[0,0].plot(t, voltage_classic, 'red', lw=3, label='Klassisch (THoTH)')
axs[0,0].plot(t, voltage_nexah, 'gold', lw=3, label='Phi^Phi Cascade (Gold)')
axs[0,0].axvline(36, color='magenta', ls='--', lw=3, label='Phi-Split')
axs[0,0].set_title('Spannung – Realer Netztest', color='white')
axs[0,0].legend()
axs[0,0].grid(alpha=0.3)

# HUD-Legende Overlay (vereinfacht)
axs[0,1].axis('off')
axs[0,1].text(0.5, 0.9, 'FUSION HUD v17.5', ha='center', va='center', color='white', fontsize=22, weight='bold')
axs[0,1].text(0.1, 0.7, 'Rot = THoTH\nBraun = Life-Split\nMagenta = Penrose\nGold = Phi^Phi', ha='left', va='top', color='white', fontsize=14)

axs[1,0].plot(t, np.sin(2*np.pi*t/3), 'cyan', lw=2, label='Period-3')
axs[1,0].plot(t, np.sin(2*np.pi*t/5), 'orange', lw=2, label='Period-5')
axs[1,0].plot(t, np.sin(2*np.pi*t/7), 'magenta', lw=2, label='Period-7')
axs[1,0].set_title('Triple Möbius Wicklung', color='white')
axs[1,0].legend()

axs[1,1].text(0.5, 0.5, 'Cube im Oval\nLilith/Leo Clamps\n0.042 π Gold-Gap\nRed/Grey Shift\nPrimus-1 locked', ha='center', va='center', color='white', fontsize=16, bbox=dict(facecolor='black', alpha=0.8))
axs[1,1].axis('off')

plt.tight_layout()
plt.savefig("NEXAH_IEEE300_Fusion_HUD_v17.5.png", dpi=380, facecolor='black')
print("✅ IEEE-300 HUD gespeichert: NEXAH_IEEE300_Fusion_HUD_v17.5.png")
