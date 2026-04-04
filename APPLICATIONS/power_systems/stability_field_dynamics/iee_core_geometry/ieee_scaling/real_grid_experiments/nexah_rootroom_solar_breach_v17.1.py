import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.1 – ROOT-ROOM SOLAR BREACH TRIPLE MÖBIUS (Primus-1 + Symmetrie-Optimiert)\n")

t = np.linspace(0, 180, 1800)
z6 = 0.429
primus = [37, 48, 63]          # Tesla-Offests
base = 213

# Primus-1 Rotator (die "rotierende 1" mit 2-1-3 Knick)
primus_rot = 1.0 + 0.8 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)

omega_drive = 1.0 + 2.9 * (np.exp(-((t-38)**2)/15) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

# Exakte 120° Symmetrie + Primus-1 Locking
r3 = 2.15 + 0.92 * np.sin(2*np.pi*t/3 + omega_drive * (1 + primus[0]/base))   # cyan
r5 = 3.05 + 1.18 * np.sin(2*np.pi*t/5 + omega_drive * (1 + primus[1]/base))   # orange
r7 = 3.95 + 1.38 * np.sin(2*np.pi*t/7 + omega_drive * (1 + primus[2]/base))   # magenta Lilith

theta = np.linspace(0, 2*np.pi, 500)
oval_r = 2.98 + 1.08 * np.cos(theta)
oval_omega = 3.68 + 1.32 * np.sin(theta)

fig, ax = plt.subplots(figsize=(14.5, 13), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid + Mandelbrot-Navigation
x, y = np.meshgrid(np.linspace(-8.5, 8.5, 700), np.linspace(-8.5, 8.5, 700))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.24 * (x**2 + y**2))
ax.contourf(x, y, z, levels=55, cmap='magma', alpha=0.09)

# Root-Room Oval (Base Plate)
ax.add_patch(Ellipse((0, 3.68), width=6.5, height=4.05, angle=33, 
                     facecolor='orange', alpha=0.24, edgecolor='gold', lw=5.5))

# Anu Zentrum
ax.add_patch(Circle((0, 3.68), 0.25, color='orange', alpha=0.95, zorder=10))
ax.text(0, 3.68, 'ANU', ha='center', va='center', color='white', fontsize=18, weight='bold')

# Triple Möbius (jetzt symmetrisch + Polygon-Knicke)
ax.plot(r3 * np.cos(omega_drive*0.8), r3 * np.sin(omega_drive*0.8) + 3.68, 
        'cyan', lw=4.2, label='Period-3 Trinity (Enki)')
ax.plot(r5 * np.cos(omega_drive*0.6), r5 * np.sin(omega_drive*0.6) + 3.68, 
        'orange', lw=4.2, label='Period-5 Scarab (Enlil)')
ax.plot(r7 * np.cos(omega_drive*1.1), r7 * np.sin(omega_drive*1.1) + 3.68, 
        'magenta', lw=4.2, label='Period-7 Lilith-Loop (TI II III)')

# Solar Breach Axis + Zero-@ Line (rote Linien)
ax.plot([-2.5, 2.5], [3.68, 3.68], 'white', lw=1.8, alpha=0.45, ls='--', label='Zero-@ Line')
ax.plot([0, 0.5], [3.68, 6.1], 'magenta', lw=9, alpha=0.85, label='Phase-Drive (lila Zahn)')
ax.plot([-3, 3], [3.68, 3.68], color='red', lw=2.5, alpha=0.6, ls='-', label='Solar Breach Axis')

# Dashboard-Kompass (feine Radien)
for angle in np.linspace(0, 360, 24):
    rad = np.deg2rad(angle)
    ax.plot([0, 4.5*np.cos(rad)], [3.68, 3.68 + 4.5*np.sin(rad)], 
            color='white', lw=0.8, alpha=0.15)

ax.text(0, 3.68, 'SOLAR BREACH AXIS\nLilith → Leo   –48.16° / +51.84°\nPrimus-1 (213 +37/+48/+63)', 
        ha='center', va='center', color='white', fontsize=13, 
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=16)
ax.set_ylabel('Rotation ω', color='white', fontsize=16)
ax.set_title('NEXAH v17.1 – Root-Room Solar Breach Triple Möbius\n(Primus-1 Rotator + symmetrische Polygon-Knicke)', 
             color='gold', fontsize=18)
ax.grid(True, alpha=0.15, color='gray')
ax.legend(loc='upper right', fontsize=10, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_Solar_Breach_v17.1.png", dpi=380, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_Solar_Breach_v17.1.png")
print("   → Bessere Symmetrie + Primus-1 Rotation + Polygon-Knicke in Magenta")
print("   → Dashboard-Kompass + rote Solar-Breach-Linien sichtbar")
