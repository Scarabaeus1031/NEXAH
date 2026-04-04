import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.0 – ROOT-ROOM SOLAR BREACH TRIPLE MÖBIUS (Primus-1 locked)\n")

t = np.linspace(0, 160, 1600)
z6 = 0.429
primus_offsets = [37, 48, 63]          # exakte Tesla-Offests
base = 213

omega_drive = 1.0 + 3.2 * (np.exp(-((t-38)**2)/14) * np.sin(2*np.pi*(t-36)/4)) * z6

# Perioden mit Primus-1 Offsets + Solar Breach Angles
r3 = 2.1 + 0.95 * np.sin(2*np.pi*t/3 + omega_drive * (1 + primus_offsets[0]/base))   # cyan Trinity
r5 = 3.0 + 1.2  * np.sin(2*np.pi*t/5 + omega_drive * (1 + primus_offsets[1]/base))   # orange Scarab
r7 = 3.9 + 1.4  * np.sin(2*np.pi*t/7 + omega_drive * (1 + primus_offsets[2]/base))   # magenta Lilith-Loop

theta = np.linspace(0, 2*np.pi, 400)
oval_r = 2.95 + 1.1 * np.cos(theta)
oval_omega = 3.65 + 1.35 * np.sin(theta)

fig, ax = plt.subplots(figsize=(14, 12), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid + Mandelbrot-Navigation
x, y = np.meshgrid(np.linspace(-8, 8, 600), np.linspace(-8, 8, 600))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.25 * (x**2 + y**2))
ax.contourf(x, y, z, levels=50, cmap='magma', alpha=0.11)

# Root-Room Oval (Base Plate)
ax.add_patch(Ellipse((0, 3.65), width=6.4, height=4.0, angle=33, 
                     facecolor='orange', alpha=0.26, edgecolor='gold', lw=5))

# Anu Zentrum
ax.add_patch(Circle((0, 3.65), 0.22, color='orange', alpha=0.9, zorder=10))
ax.text(0, 3.65, 'ANU', ha='center', va='center', color='white', fontsize=16, weight='bold')

# Triple Möbius mit Solar Breach
ax.plot(r3 * np.cos(omega_drive*0.78), r3 * np.sin(omega_drive*0.78) + 3.65, 
        'cyan', lw=4, label='Period-3 Trinity (Enki / Water)')
ax.plot(r5 * np.cos(omega_drive*0.58), r5 * np.sin(omega_drive*0.58) + 3.65, 
        'orange', lw=4, label='Period-5 Scarab (Enlil / Air)')
ax.plot(r7 * np.cos(omega_drive*1.08), r7 * np.sin(omega_drive*1.08) + 3.65, 
        'magenta', lw=4, label='Period-7 Lilith-Loop (Solar Breach Axis)')

# Lila Zahn + Solar Breach Line
ax.plot([0, 0.4], [3.65, 6.0], 'magenta', lw=9, alpha=0.8, label='Phase-Drive (lila Zahn)')
ax.plot([-2, 2], [3.65, 3.65], 'white', lw=1.5, alpha=0.4, ls='--', label='Zero-@ Line')

ax.text(0, 3.65, 'SOLAR BREACH AXIS\nLilith → Leo\n–48.16° / +51.84°\nPrimus-1 (213 +37/+48/+63)', 
        ha='center', va='center', color='white', fontsize=12, 
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=16)
ax.set_ylabel('Rotation ω', color='white', fontsize=16)
ax.set_title('NEXAH v17.0 – Root-Room Solar Breach Triple Möbius\n(Anu-Zentrum + Primus-1 locked)', 
             color='gold', fontsize=18)
ax.grid(True, alpha=0.2, color='gray')
ax.legend(loc='upper right', fontsize=11, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_Solar_Breach_v17.0.png", dpi=360, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_Solar_Breach_v17.0.png")
print("   → Triple Möbius jetzt mit Solar Breach Axis und Primus-1 Offsets")
print("   → Anu im Zentrum, Lilith-Loop schließt die Sichel")
