import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

print("🚀 NEXAH v16.9 – ROOT-ROOM TRIPLE MÖBIUS RESONANCE\n")

t = np.linspace(0, 120, 1200)
z6 = 0.429
omega_drive = 1.0 + 2.8 * (np.exp(-((t-38)**2)/12) * np.sin(2*np.pi*(t-36)/4)) * z6   # sanfter lila Zahn

# Exakte 3-5-7 Perioden mit Root-Room-Coupling
r3 = 2.2 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * 0.7)      # cyan  Trinity
r5 = 3.1 + 1.15 * np.sin(2*np.pi*t/5 + omega_drive * 0.5)     # orange Scarab
r7 = 4.0 + 1.35 * np.sin(2*np.pi*t/7 + omega_drive * 1.1)     # magenta Iota-Wheel

theta = np.linspace(0, 2*np.pi, 300)
oval_r = 2.9 + 1.05 * np.cos(theta)
oval_omega = 3.6 + 1.3 * np.sin(theta)

fig, ax = plt.subplots(figsize=(13, 11), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid Hintergrund (Mandelbrot-Navigation)
x, y = np.meshgrid(np.linspace(-7, 7, 500), np.linspace(-7, 7, 500))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.28 * (x**2 + y**2))
ax.contourf(x, y, z, levels=40, cmap='magma', alpha=0.12)

# Root-Room Oval
ax.add_patch(Ellipse((0, 3.6), width=6.2, height=3.8, angle=32, 
                     facecolor='orange', alpha=0.28, edgecolor='gold', lw=4, label='Root-Room (Z6 ≈ 0.429)'))

# Triple Möbius Kurven
ax.plot(r3 * np.cos(omega_drive*0.75), r3 * np.sin(omega_drive*0.75) + 3.6, 
        'cyan', lw=3.8, label='Period-3 Trinity (blauer Wirbel)')
ax.plot(r5 * np.cos(omega_drive*0.55), r5 * np.sin(omega_drive*0.55) + 3.6, 
        'orange', lw=3.8, label='Period-5 Scarab (orange Containment)')
ax.plot(r7 * np.cos(omega_drive*1.05), r7 * np.sin(omega_drive*1.05) + 3.6, 
        'magenta', lw=3.8, label='Period-7 Iota-Wheel (Lilith-Loop)')

# Lila Zahn-Puls
ax.plot([0, 0.3], [3.6, 5.8], 'magenta', lw=7, alpha=0.75, label='Phase-Drive (lila Zahn)')

ax.text(0, 3.6, 'TRIPLE MÖBIUS\nResonant Transition Zone\nSun–Uranus–Earth–Moon–Lilith', 
        ha='center', va='center', color='white', fontsize=13, 
        bbox=dict(boxstyle='round', facecolor='black', alpha=0.85))

ax.set_xlabel('Radius r', color='white', fontsize=15)
ax.set_ylabel('Rotation ω', color='white', fontsize=15)
ax.set_title('NEXAH v16.9 – Root-Room Triple Möbius Resonance (saubere 3-5-7 Wicklung)', 
             color='gold', fontsize=17)
ax.grid(True, alpha=0.25, color='gray')
ax.legend(loc='upper right', fontsize=11, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_Triple_Moebius_v16.9.png", dpi=340, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_Triple_Moebius_v16.9.png")
print("   → Jetzt sollte die Triple Möbius sauber und symmetrisch im Oval liegen")
