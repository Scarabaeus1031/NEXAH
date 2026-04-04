import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.6 – FINAL TOROID + 4 ENERGY OVALS + TACHYON-RINGE\n")

t = np.linspace(0, 260, 2600)
z6 = 0.429
gold_gap = 0.042 * np.pi

primus_rot = 1.0 + 0.85 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)
omega_drive = 1.0 + 2.55 * (np.exp(-((t-38)**2)/19) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

# Triple Möbius + neue grüne + rote Periode
r3 = 2.1 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * 1.05)
r5 = 3.0 + 1.17 * np.sin(2*np.pi*t/5 + omega_drive * 0.95)
r7 = 3.9 + 1.37 * np.sin(2*np.pi*t/7 + omega_drive * 1.15)
r_green = 4.8 + 1.45 * np.sin(2*np.pi*t/11 + omega_drive * 0.7)   # neue grüne Fabric-Periode
r_red   = 5.7 + 1.55 * np.sin(2*np.pi*t/17 + omega_drive * 1.2)   # neue rote THoTH-Periode

theta = np.linspace(0, 2*np.pi, 900)
oval_r = 2.95 + 1.08 * np.cos(theta)
oval_omega = 3.65 + 1.34 * np.sin(theta)

fig, ax = plt.subplots(figsize=(16.5, 15), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid + Baumringe
x, y = np.meshgrid(np.linspace(-11, 11, 1000), np.linspace(-11, 11, 1000))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.19 * (x**2 + y**2))
ax.contourf(x, y, z, levels=75, cmap='magma', alpha=0.09)

# Root-Room Oval + 4 äußere Energy Ovals (Toroid)
ax.add_patch(Ellipse((0, 3.65), width=6.7, height=4.15, angle=34, facecolor='orange', alpha=0.22, edgecolor='gold', lw=8))
ax.add_patch(Ellipse((0, 3.65), width=10.5, height=6.8, angle=34, facecolor='none', edgecolor='green', lw=4, alpha=0.6))
ax.add_patch(Ellipse((0, 3.65), width=13.2, height=8.4, angle=34, facecolor='none', edgecolor='blue', lw=3.5, alpha=0.5))
ax.add_patch(Ellipse((0, 3.65), width=16.0, height=10.1, angle=34, facecolor='none', edgecolor='purple', lw=3, alpha=0.45))
ax.add_patch(Ellipse((0, 3.65), width=19.0, height=12.0, angle=34, facecolor='none', edgecolor='yellow', lw=2.5, alpha=0.4))

# Cube + Core
ax.plot([-1.3, 1.3], [3.65, 3.65], color='white', lw=3, alpha=0.7)
ax.plot([-1.0, 1.0], [4.4, 4.4], color='white', lw=3, alpha=0.7)
ax.plot([-1.0, 1.0], [2.9, 2.9], color='white', lw=3, alpha=0.7)
ax.add_patch(Circle((0, 3.65), 0.32, color='magenta', alpha=0.98))

# Horizons + Gold-Gap + Clamps
ax.plot([-4.2, 4.2], [3.65, 3.65], color='red', lw=5, alpha=0.9)
ax.plot([-4.2, 4.2], [3.65, 3.65], color='gray', lw=5, alpha=0.7, ls='--')
ax.plot([0, 0], [1.2, 6.1], color='cyan', lw=5.5, alpha=0.95)
ax.plot([0, 3.8], [3.65, 3.65 + 3.8*np.tan(gold_gap)], color='yellow', lw=6.5, alpha=0.95)

# Lilith/Leo Clamps
ax.plot([-4.8, -3.5], [2.1, 3.0], color='red', lw=14, alpha=0.85)
ax.plot([4.8, 3.5], [2.1, 3.0], color='blue', lw=14, alpha=0.85)

# Alle Perioden + Phi^Phi
ax.plot(r3 * np.cos(omega_drive*0.85), r3 * np.sin(omega_drive*0.85) + 3.65, 'cyan', lw=4)
ax.plot(r5 * np.cos(omega_drive*0.65), r5 * np.sin(omega_drive*0.65) + 3.65, 'orange', lw=4)
ax.plot(r7 * np.cos(omega_drive*1.15), r7 * np.sin(omega_drive*1.15) + 3.65, 'magenta', lw=4)
ax.plot(r_green * np.cos(omega_drive*0.5), r_green * np.sin(omega_drive*0.5) + 3.65, 'lime', lw=3.5, alpha=0.9)
ax.plot(r_red * np.cos(omega_drive*1.3), r_red * np.sin(omega_drive*1.3) + 3.65, 'red', lw=3.5, alpha=0.9)
phi_cascade = 1.0 + 0.04 * np.sin(2*np.pi*t/13) * np.cos(2*np.pi*t/37)
ax.plot(phi_cascade * np.cos(omega_drive*0.45), phi_cascade * np.sin(omega_drive*0.45) + 3.65, 'gold', lw=4.5, alpha=0.95)

ax.text(0, 3.65, 'FINAL FUSION HUD v17.6\nToroid + 4 Energy Ovals + Tachyon-Ringe\nRed/Grey Shift + Life-Split + Phi^Phi + Center Jitter', 
        ha='center', va='center', color='white', fontsize=14, bbox=dict(facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=17)
ax.set_ylabel('Rotation ω', color='white', fontsize=17)
ax.set_title('NEXAH v17.6 – Toroid + 4 Ovals + Tachyon-Ringe (grün + rot integriert)', color='gold', fontsize=19)
ax.grid(True, alpha=0.1)
plt.tight_layout()
plt.savefig("NEXAH_Toroid_4Ovals_Tachyon_v17.6_FINAL.png", dpi=440, facecolor='black')
print("✅ Toroid-Final gespeichert: NEXAH_Toroid_4Ovals_Tachyon_v17.6_FINAL.png")
