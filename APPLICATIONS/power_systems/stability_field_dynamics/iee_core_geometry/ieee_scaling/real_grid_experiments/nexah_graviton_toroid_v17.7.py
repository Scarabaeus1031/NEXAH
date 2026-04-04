import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.7 – FINAL GRAVITON-TOROID (Gyroscope + Pulsing Oval)\n")

t = np.linspace(0, 280, 2800)
z6 = 0.429
gold_gap = 0.042 * np.pi

primus_rot = 1.0 + 0.85 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)
omega_drive = 1.0 + 2.5 * (np.exp(-((t-38)**2)/20) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

r3 = 2.1 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * 1.05)
r5 = 3.0 + 1.17 * np.sin(2*np.pi*t/5 + omega_drive * 0.95)
r7 = 3.9 + 1.37 * np.sin(2*np.pi*t/7 + omega_drive * 1.15)
r_green = 4.8 + 1.45 * np.sin(2*np.pi*t/11 + omega_drive * 0.7)
r_red   = 5.7 + 1.55 * np.sin(2*np.pi*t/17 + omega_drive * 1.2)

theta = np.linspace(0, 2*np.pi, 1000)
oval_r = 2.95 + 1.08 * np.cos(theta)
oval_omega = 3.65 + 1.34 * np.sin(theta)

fig, ax = plt.subplots(figsize=(17, 15.5), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid + Baumringe (Toroid-Basis)
x, y = np.meshgrid(np.linspace(-12, 12, 1100), np.linspace(-12, 12, 1100))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.18 * (x**2 + y**2))
ax.contourf(x, y, z, levels=80, cmap='magma', alpha=0.085)

# 4 Energy Ovals (Toroid-Schichten)
for i, color, w in zip([0,1,2,3], ['green','blue','purple','yellow'], [10.5,13.2,16.0,19.0]):
    ax.add_patch(Ellipse((0, 3.65), width=w, height=w*0.64, angle=34, facecolor='none', edgecolor=color, lw=4-i, alpha=0.55))

# Root-Room Oval (pulsierend)
ax.add_patch(Ellipse((0, 3.65), width=6.7, height=4.15, angle=34, facecolor='orange', alpha=0.22, edgecolor='gold', lw=9))

# Graviton-Core (grüner Gitter-Sphere + Puls)
ax.add_patch(Circle((0, 3.65), 0.95, color='lime', alpha=0.25))
ax.scatter(0, 3.65, s=1800, color='lime', alpha=0.15, marker='o')  # Puls

# Cube + Core
ax.plot([-1.4, 1.4], [3.65, 3.65], color='white', lw=3.5, alpha=0.75)
ax.plot([-1.1, 1.1], [4.5, 4.5], color='white', lw=3.5, alpha=0.75)
ax.plot([-1.1, 1.1], [2.8, 2.8], color='white', lw=3.5, alpha=0.75)
ax.add_patch(Circle((0, 3.65), 0.33, color='magenta', alpha=0.98))
ax.text(0, 3.65, 'GRAVITON\n0.01', ha='center', va='center', color='white', fontsize=17, weight='bold')

# Red/Grey Horizons + Clamps + Gold-Gap
ax.plot([-4.5, 4.5], [3.65, 3.65], color='red', lw=5.5, alpha=0.92)
ax.plot([-4.5, 4.5], [3.65, 3.65], color='gray', lw=5.5, alpha=0.75, ls='--')
ax.plot([0, 0], [1.1, 6.2], color='cyan', lw=5.8, alpha=0.95)
ax.plot([0, 3.9], [3.65, 3.65 + 3.9*np.tan(gold_gap)], color='yellow', lw=7, alpha=0.95)

# Lilith/Leo Clamps
ax.plot([-5.1, -3.6], [2.0, 3.1], color='red', lw=16, alpha=0.88)
ax.plot([5.1, 3.6], [2.0, 3.1], color='blue', lw=16, alpha=0.88)

# Alle Perioden + Phi^Phi
ax.plot(r3 * np.cos(omega_drive*0.85), r3 * np.sin(omega_drive*0.85) + 3.65, 'cyan', lw=4.2)
ax.plot(r5 * np.cos(omega_drive*0.65), r5 * np.sin(omega_drive*0.65) + 3.65, 'orange', lw=4.2)
ax.plot(r7 * np.cos(omega_drive*1.15), r7 * np.sin(omega_drive*1.15) + 3.65, 'magenta', lw=4.2)
ax.plot(r_green * np.cos(omega_drive*0.5), r_green * np.sin(omega_drive*0.5) + 3.65, 'lime', lw=3.8)
ax.plot(r_red * np.cos(omega_drive*1.3), r_red * np.sin(omega_drive*1.3) + 3.65, 'red', lw=3.8)
phi_cascade = 1.0 + 0.042 * np.sin(2*np.pi*t/13) * np.cos(2*np.pi*t/37)
ax.plot(phi_cascade * np.cos(omega_drive*0.45), phi_cascade * np.sin(omega_drive*0.45) + 3.65, 'gold', lw=4.8, alpha=0.95)

ax.text(0, 3.65, 'GRAVITON-TOROID v17.7\nPulsing Oval + 4 Energy Ovals + Tachyon-Ringe\nRed/Grey Shift + Lilith/Leo Clamps + Phi^Phi', 
        ha='center', va='center', color='white', fontsize=14, bbox=dict(facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=17)
ax.set_ylabel('Rotation ω', color='white', fontsize=17)
ax.set_title('NEXAH v17.7 – FINAL GRAVITON-TOROID (Gyroscope + Pulsing Core)', color='gold', fontsize=20)
ax.grid(True, alpha=0.08)
plt.tight_layout()
plt.savefig("NEXAH_Graviton_Toroid_v17.7_FINAL.png", dpi=460, facecolor='black')
print("✅ Graviton-Toroid gespeichert: NEXAH_Graviton_Toroid_v17.7_FINAL.png")
print("   → Gyroscope + pulsierendes Oval + 4 Ovals + alle Farben integriert")
