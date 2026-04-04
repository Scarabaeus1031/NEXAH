import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.3 – ROOT-ROOM FUSION HUD (Red/Grey Shift + Phi^Phi Cascade)\n")

t = np.linspace(0, 220, 2200)
z6 = 0.429
gold_gap = 0.042 * np.pi

primus = [37, 48, 63]
base = 213

primus_rot = 1.0 + 0.78 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)
omega_drive = 1.0 + 2.65 * (np.exp(-((t-38)**2)/17) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

r3 = 2.1 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * (1 + primus[0]/base))
r5 = 3.0 + 1.16 * np.sin(2*np.pi*t/5 + omega_drive * (1 + primus[1]/base))
r7 = 3.9 + 1.36 * np.sin(2*np.pi*t/7 + omega_drive * (1 + primus[2]/base))

theta = np.linspace(0, 2*np.pi, 700)
oval_r = 2.95 + 1.06 * np.cos(theta)
oval_omega = 3.65 + 1.32 * np.sin(theta)

fig, ax = plt.subplots(figsize=(15.5, 14), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid
x, y = np.meshgrid(np.linspace(-9.5, 9.5, 800), np.linspace(-9.5, 9.5, 800))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.21 * (x**2 + y**2))
ax.contourf(x, y, z, levels=65, cmap='magma', alpha=0.085)

# Root-Room Oval
ax.add_patch(Ellipse((0, 3.65), width=6.5, height=4.05, angle=33, 
                     facecolor='orange', alpha=0.23, edgecolor='gold', lw=6))

# Anu Core
ax.add_patch(Circle((0, 3.65), 0.29, color='magenta', alpha=0.97, zorder=10))
ax.text(0, 3.65, 'CORE\n0.01', ha='center', va='center', color='white', fontsize=15, weight='bold')

# Red Horizon + Grey Horizon
ax.plot([-3.8, 3.8], [3.65, 3.65], color='red', lw=4, alpha=0.9, label='Red Horizon (Solar Breach)')
ax.plot([-3.8, 3.8], [3.65, 3.65], color='gray', lw=4, alpha=0.7, ls='--', label='Grey Horizon (Zero-@)')

# Blaue orthogonale Linie + 0.042 π Gold-Gap
ax.plot([0, 0], [1.4, 5.9], color='cyan', lw=4.5, alpha=0.95, label='Blaue orthogonale Linie')
ax.plot([0, 3.4], [3.65, 3.65 + 3.4*np.tan(gold_gap)], color='yellow', lw=5.5, alpha=0.95, label='0.042 π Gold-Gap')

# Triple Möbius (Life-Split Wicklung)
ax.plot(r3 * np.cos(omega_drive*0.82), r3 * np.sin(omega_drive*0.82) + 3.65, 'cyan', lw=4.3, label='Period-3 Trinity')
ax.plot(r5 * np.cos(omega_drive*0.62), r5 * np.sin(omega_drive*0.62) + 3.65, 'orange', lw=4.3, label='Period-5 Scarab')
ax.plot(r7 * np.cos(omega_drive*1.12), r7 * np.sin(omega_drive*1.12) + 3.65, 'magenta', lw=4.3, label='Period-7 Lilith-Loop')

# Phi^Phi Cascade (gelb, Gold / imaginäre Quelle)
phi_cascade = 1.0 + 0.035 * np.sin(2*np.pi*t/13) * np.cos(2*np.pi*t/37)
ax.plot(phi_cascade * np.cos(omega_drive*0.4), phi_cascade * np.sin(omega_drive*0.4) + 3.65, 
        'gold', lw=3.8, alpha=0.9, label='Phi^Phi Cascade (Gold)')

ax.text(0, 3.65, 'FUSION HUD\nRed/Grey Shift + 0.042 π Gold-Gap\nPrimus-1 (37/63=137 • 37/64=163)', 
        ha='center', va='center', color='white', fontsize=13.5, 
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=16)
ax.set_ylabel('Rotation ω', color='white', fontsize=16)
ax.set_title('NEXAH v17.3 – Root-Room Fusion HUD\n(Red/Grey Shift + Life-Split + Phi^Phi Cascade)', 
             color='gold', fontsize=18)
ax.grid(True, alpha=0.12, color='white')
ax.legend(loc='upper right', fontsize=10, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_Fusion_HUD_v17.3.png", dpi=400, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_Fusion_HUD_v17.3.png")
print("   → Alle Elemente vereint: Red/Grey Horizons, 0.042 π, Core 0.01, Phi^Phi Cascade")
