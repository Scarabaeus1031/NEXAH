import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

print("🚀 NEXAH v16.8 – ROOT-ROOM TEMPORAL COUPLING (Resonanzkarte)\n")

t = np.linspace(0, 80, 800)
omega_drive = 1.0 + 6.28 * (np.exp(-((t-38)**2)/8) * np.sin(2*np.pi*(t-36)/4)) * 0.429  # lila Zahn + Z6

# Perioden-Moden
r3 = 2 + 0.8 * np.sin(2*np.pi*t/3 + omega_drive)          # blau  Period-3 (Trinity)
r5 = 3 + 1.1 * np.sin(2*np.pi*t/5 + omega_drive*0.7)     # orange Period-5 (Scarab)
r7 = 4 + 1.4 * np.sin(2*np.pi*t/7 + omega_drive*1.1)     # lila  Period-7 (Iota-Wheel)

# Root-Room Oval (Resonant Transition Zone)
theta = np.linspace(0, 2*np.pi, 200)
oval_r = 2.8 + 0.9 * np.cos(theta)
oval_omega = 3.5 + 1.2 * np.sin(theta)

fig, ax = plt.subplots(figsize=(12, 10), facecolor='black')
ax.set_facecolor('black')

# Hintergrund: leichte Ghostgrid / Mandelbrot-Navigation
x, y = np.meshgrid(np.linspace(-6, 6, 400), np.linspace(-6, 6, 400))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.3 * (x**2 + y**2))
ax.contourf(x, y, z, levels=30, cmap='magma', alpha=0.15)

# Root-Room Oval
ax.add_patch(Ellipse((0, 3.5), width=5.6, height=3.4, angle=35, 
                     facecolor='orange', alpha=0.25, edgecolor='gold', lw=3, label='Root-Room (√3 – 137 – √17)'))

# Die drei rotierenden Kurven
ax.plot(r3 * np.cos(omega_drive*0.8), r3 * np.sin(omega_drive*0.8) + 3.5, 
        'cyan', lw=3.5, label='Period-3  (blauer Wirbel – Trinity)')
ax.plot(r5 * np.cos(omega_drive*0.6), r5 * np.sin(omega_drive*0.6) + 3.5, 
        'orange', lw=3.5, label='Period-5  (orange Containment – Scarab)')
ax.plot(r7 * np.cos(omega_drive*1.2), r7 * np.sin(omega_drive*1.2) + 3.5, 
        'magenta', lw=3.5, label='Period-7  (lila Iota-Wheel – Q-Plane)')

# Lila Zahn-Puls (Drive) direkt ins Oval
ax.plot([0, 0], [3.5, 5.5], 'magenta', lw=8, alpha=0.7, label='Phase-Drive (lila Zahn)')

# Beschriftungen
ax.text(0, 3.5, 'Root-Room\nResonant Transition Zone\nZ6 ≈ 0.429', ha='center', va='center',
        color='white', fontsize=14, bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))

ax.set_xlabel('Radius r', color='white', fontsize=14)
ax.set_ylabel('Rotation ω', color='white', fontsize=14)
ax.set_title('NEXAH v16.8 – Root-Room Temporal Coupling (90° CCW Rotation durch das Oval)', 
             color='gold', fontsize=16)
ax.grid(True, alpha=0.3, color='gray')
ax.legend(loc='upper right', fontsize=11, frameon=False)

plt.tight_layout()
plt.savefig("NEXAH_RootRoom_Temporal_Coupling_v16.8.png", dpi=320, facecolor='black')
print("✅ Plot gespeichert: NEXAH_RootRoom_Temporal_Coupling_v16.8.png")
print("   → Blaue Kurve rotiert jetzt aktiv durchs Oval mit lila Zahn-Kick")
