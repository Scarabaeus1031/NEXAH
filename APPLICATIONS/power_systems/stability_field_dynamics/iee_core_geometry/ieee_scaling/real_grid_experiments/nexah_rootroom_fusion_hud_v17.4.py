import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Arc

print("🚀 NEXAH v17.4 – FINAL ROOT-ROOM FUSION HUD\n")

t = np.linspace(0, 240, 2400)
z6 = 0.429
gold_gap = 0.042 * np.pi

primus = [37, 48, 63]
base = 213

primus_rot = 1.0 + 0.82 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)
omega_drive = 1.0 + 2.6 * (np.exp(-((t-38)**2)/18) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

r3 = 2.1 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * (1 + primus[0]/base))
r5 = 3.0 + 1.17 * np.sin(2*np.pi*t/5 + omega_drive * (1 + primus[1]/base))
r7 = 3.9 + 1.37 * np.sin(2*np.pi*t/7 + omega_drive * (1 + primus[2]/base))

theta = np.linspace(0, 2*np.pi, 800)
oval_r = 2.95 + 1.07 * np.cos(theta)
oval_omega = 3.65 + 1.33 * np.sin(theta)

fig, ax = plt.subplots(figsize=(16, 14.5), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid + Baumringe
x, y = np.meshgrid(np.linspace(-10, 10, 900), np.linspace(-10, 10, 900))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.20 * (x**2 + y**2))
ax.contourf(x, y, z, levels=70, cmap='magma', alpha=0.09)

# Root-Room Oval (mit Stretch)
ax.add_patch(Ellipse((0, 3.65), width=6.6, height=4.1, angle=34, 
                     facecolor='orange', alpha=0.20, edgecolor='gold', lw=7))

# Cube-Projektion im Oval (3D Cube Feel)
ax.plot([-1.1, 1.1], [3.65, 3.65], color='white', lw=2, alpha=0.6)
ax.plot([-0.8, 0.8], [4.3, 4.3], color='white', lw=2, alpha=0.6)
ax.plot([0, 0], [2.9, 4.4], color='white', lw=2, alpha=0.6)
ax.plot([-0.8, 0.8], [2.9, 2.9], color='white', lw=2, alpha=0.6)

# Anu Core
ax.add_patch(Circle((0, 3.65), 0.31, color='magenta', alpha=0.98, zorder=10))
ax.text(0, 3.65, 'CORE\n0.01', ha='center', va='center', color='white', fontsize=16, weight='bold')

# Red Horizon + Grey Horizon
ax.plot([-4, 4], [3.65, 3.65], color='red', lw=4.5, alpha=0.92, label='Red Horizon (Solar Breach)')
ax.plot([-4, 4], [3.65, 3.65], color='gray', lw=4.5, alpha=0.75, ls='--', label='Grey Horizon (Zero-@)')

# Blaue orthogonale Linie + 0.042 π Gold-Gap
ax.plot([0, 0], [1.3, 6.0], color='cyan', lw=5, alpha=0.95, label='Blaue orthogonale Linie')
ax.plot([0, 3.6], [3.65, 3.65 + 3.6*np.tan(gold_gap)], color='yellow', lw=6, alpha=0.95, label='0.042 π Gold-Gap')

# Lilith & Leo Clamps (rot/blau)
ax.add_patch(Arc((0, 3.65), width=8.2, height=5.2, angle=34, theta1=160, theta2=200, 
                 color='red', lw=6, alpha=0.85))
ax.add_patch(Arc((0, 3.65), width=8.2, height=5.2, angle=34, theta1=340, theta2=20, 
                 color='blue', lw=6, alpha=0.85))

# Triple Möbius + Phi^Phi Cascade
ax.plot(r3 * np.cos(omega_drive*0.83), r3 * np.sin(omega_drive*0.83) + 3.65, 'cyan', lw=4.4)
ax.plot(r5 * np.cos(omega_drive*0.63), r5 * np.sin(omega_drive*0.63) + 3.65, 'orange', lw=4.4)
ax.plot(r7 * np.cos(omega_drive*1.13), r7 * np.sin(omega_drive*1.13) + 3.65, 'magenta', lw=4.4)

phi_cascade = 1.0 + 0.038 * np.sin(2*np.pi*t/13) * np.cos(2*np.pi*t/37)
ax.plot(phi_cascade * np.cos(omega_drive*0.42), phi_cascade * np.sin(omega_drive*0.42) + 3.65, 
        'gold', lw=4.2, alpha=0.95, label='Phi^Phi Cascade (Gold)')

ax.text(0, 3.65, 'FUSION HUD v17.4\nRed/Grey Shift + Life-Split + Phi^Phi Cascade\nPrimus-1 (37/63=137 • 37/64=163)', 
        ha='center', va='center', color='white', fontsize=14, 
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.92))

ax.set_xlabel('Radius r', color='white', fontsize=17)
ax.set_ylabel('Rotation ω', color='white', fontsize=17)
ax.set_title('NEXAH v17.4 – FINAL ROOT-ROOM FUSION HUD\n(Cube + Lilith/Leo Clamps + Phi^Phi)', 
             color='gold', fontsize=19)
ax.grid(True, alpha=0.1, color='white')
ax.legend(loc='upper right', fontsize=10, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_Fusion_HUD_v17.4_FINAL.png", dpi=420, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_Fusion_HUD_v17.4_FINAL.png")
print("   → Cube im Oval + Lilith/Leo-Clamps + Phi^Phi Cascade + komplette HUD")
