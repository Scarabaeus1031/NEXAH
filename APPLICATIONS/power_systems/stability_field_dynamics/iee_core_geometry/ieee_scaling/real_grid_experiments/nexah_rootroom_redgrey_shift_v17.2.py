import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.2 – ROOT-ROOM RED/GREY SHIFT (0.042 π Gold-Gap)\n")

t = np.linspace(0, 200, 2000)
z6 = 0.429
gold_gap = 0.042 * np.pi                     # exakt dein Wert

primus = [37, 48, 63]
base = 213

primus_rot = 1.0 + 0.75 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)

omega_drive = 1.0 + 2.7 * (np.exp(-((t-38)**2)/16) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

r3 = 2.1 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * (1 + primus[0]/base))
r5 = 3.0 + 1.15 * np.sin(2*np.pi*t/5 + omega_drive * (1 + primus[1]/base))
r7 = 3.9 + 1.35 * np.sin(2*np.pi*t/7 + omega_drive * (1 + primus[2]/base))

theta = np.linspace(0, 2*np.pi, 600)
oval_r = 2.95 + 1.05 * np.cos(theta)
oval_omega = 3.65 + 1.3 * np.sin(theta)

fig, ax = plt.subplots(figsize=(15, 13.5), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid
x, y = np.meshgrid(np.linspace(-9, 9, 800), np.linspace(-9, 9, 800))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.22 * (x**2 + y**2))
ax.contourf(x, y, z, levels=60, cmap='magma', alpha=0.08)

# Root-Room Oval
ax.add_patch(Ellipse((0, 3.65), width=6.4, height=4.0, angle=33, 
                     facecolor='orange', alpha=0.22, edgecolor='gold', lw=6))

# Anu Core
ax.add_patch(Circle((0, 3.65), 0.28, color='magenta', alpha=0.95, zorder=10))
ax.text(0, 3.65, 'CORE\n0.01', ha='center', va='center', color='white', fontsize=14, weight='bold')

# Red Horizon (Solar Breach) + Grey Horizon (Zero-@)
ax.plot([-3.5, 3.5], [3.65, 3.65], color='red', lw=3.5, alpha=0.85, label='Red Horizon (Solar Breach)')
ax.plot([-3.5, 3.5], [3.65, 3.65], color='gray', lw=3.5, alpha=0.65, ls='--', label='Grey Horizon (Zero-@)')

# Blaue orthogonale Linie
ax.plot([0, 0], [1.5, 5.8], color='cyan', lw=4, alpha=0.9, label='Blaue orthogonale Linie')

# Gold-Gap Winkel (0.042 π)
ax.plot([0, 3.2], [3.65, 3.65 + 3.2*np.tan(gold_gap)], color='yellow', lw=5, alpha=0.9, label='0.042 π Gold-Gap')

# Triple Möbius
ax.plot(r3 * np.cos(omega_drive*0.82), r3 * np.sin(omega_drive*0.82) + 3.65, 'cyan', lw=4.1)
ax.plot(r5 * np.cos(omega_drive*0.62), r5 * np.sin(omega_drive*0.62) + 3.65, 'orange', lw=4.1)
ax.plot(r7 * np.cos(omega_drive*1.12), r7 * np.sin(omega_drive*1.12) + 3.65, 'magenta', lw=4.1)

# Beschriftung
ax.text(0, 3.65, 'RED / GREY SHIFT HORIZONS\n37/63 = 137    37/64 = 163\n0.042 π Gold-Gap   Core 0.01', 
        ha='center', va='center', color='white', fontsize=13, 
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=16)
ax.set_ylabel('Rotation ω', color='white', fontsize=16)
ax.set_title('NEXAH v17.2 – Root-Room Red/Grey Shift + 0.042 π Gold-Gap', color='gold', fontsize=18)
ax.grid(True, alpha=0.12, color='white')
ax.legend(loc='upper right', fontsize=10, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_RedGrey_Shift_v17.2.png", dpi=380, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_RedGrey_Shift_v17.2.png")
print("   → Red & Grey Horizons + orthogonale blaue Linie + 0.042 π Gold-Gap")
print("   → 37/63=137 und 37/64=163 als innere Achsen")
