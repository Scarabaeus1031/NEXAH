import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

print("🚀 NEXAH v17.8 – FINAL NAUTILUS SHRINKING CUBIC SPIRAL (5 Stages)\n")

t = np.linspace(0, 300, 3000)
z6 = 0.429
gold_gap = 0.042 * np.pi

primus_rot = 1.0 + 0.88 * np.sin(2*np.pi*t/3) * np.cos(2*np.pi*t/13)
omega_drive = 1.0 + 2.45 * (np.exp(-((t-38)**2)/22) * np.sin(2*np.pi*(t-36)/4)) * z6 * primus_rot

r3 = 2.1 + 0.9 * np.sin(2*np.pi*t/3 + omega_drive * 1.05)
r5 = 3.0 + 1.17 * np.sin(2*np.pi*t/5 + omega_drive * 0.95)
r7 = 3.9 + 1.37 * np.sin(2*np.pi*t/7 + omega_drive * 1.15)
r_green = 4.8 + 1.45 * np.sin(2*np.pi*t/11 + omega_drive * 0.7)
r_red   = 5.7 + 1.55 * np.sin(2*np.pi*t/17 + omega_drive * 1.2)

theta = np.linspace(0, 2*np.pi, 1200)
oval_r = 2.95 + 1.08 * np.cos(theta)
oval_omega = 3.65 + 1.34 * np.sin(theta)

fig, ax = plt.subplots(figsize=(17.5, 16), facecolor='black')
ax.set_facecolor('black')

# Ghostgrid + Baumringe (Nautilus-Basis)
x, y = np.meshgrid(np.linspace(-13, 13, 1200), np.linspace(-13, 13, 1200))
z = np.sin(5.37 * (x**2 + y**2)) * np.exp(-0.17 * (x**2 + y**2))
ax.contourf(x, y, z, levels=85, cmap='magma', alpha=0.09)

# 5 Stages Ovals (Cyan → Orange → Green → Purple → Meta-Fabric)
colors = ['cyan', 'orange', 'lime', 'magenta', 'purple']
widths = [6.7, 10.5, 13.2, 16.0, 19.5]
for i, (c, w) in enumerate(zip(colors, widths)):
    alpha = 0.55 - i*0.08
    ax.add_patch(Ellipse((0, 3.65), width=w, height=w*0.64, angle=34, facecolor='none', edgecolor=c, lw=5-i, alpha=alpha))

# Root-Room Oval + Graviton-Core
ax.add_patch(Ellipse((0, 3.65), width=6.7, height=4.15, angle=34, facecolor='orange', alpha=0.22, edgecolor='gold', lw=10))
ax.add_patch(Circle((0, 3.65), 1.05, color='lime', alpha=0.28))
ax.scatter(0, 3.65, s=2200, color='lime', alpha=0.12, marker='o')

# Cube + Core
ax.plot([-1.5, 1.5], [3.65, 3.65], color='white', lw=4, alpha=0.8)
ax.plot([-1.2, 1.2], [4.6, 4.6], color='white', lw=4, alpha=0.8)
ax.plot([-1.2, 1.2], [2.7, 2.7], color='white', lw=4, alpha=0.8)
ax.add_patch(Circle((0, 3.65), 0.34, color='magenta', alpha=0.98))
ax.text(0, 3.65, 'GRAVITON\n0.01', ha='center', va='center', color='white', fontsize=18, weight='bold')

# Horizons + Gold-Gap + Clamps
ax.plot([-4.8, 4.8], [3.65, 3.65], color='red', lw=6, alpha=0.93)
ax.plot([-4.8, 4.8], [3.65, 3.65], color='gray', lw=6, alpha=0.78, ls='--')
ax.plot([0, 0], [1.0, 6.3], color='cyan', lw=6, alpha=0.96)
ax.plot([0, 4.0], [3.65, 3.65 + 4.0*np.tan(gold_gap)], color='yellow', lw=7.5, alpha=0.96)

# Lilith/Leo Clamps
ax.plot([-5.4, -3.7], [1.9, 3.2], color='red', lw=18, alpha=0.9)
ax.plot([5.4, 3.7], [1.9, 3.2], color='blue', lw=18, alpha=0.9)

# Cubic Shrinking Resonance Spiral (lila Nautilus)
spiral_r = np.exp(-0.035 * t) * (8 + 2 * np.sin(2*np.pi*t/13))
spiral_theta = t * 0.42
ax.plot(spiral_r * np.cos(spiral_theta), spiral_r * np.sin(spiral_theta) + 3.65, color='purple', lw=5.5, alpha=0.95, label='Cubic Shrinking Spiral')

# Alle Perioden + Phi^Phi
ax.plot(r3 * np.cos(omega_drive*0.85), r3 * np.sin(omega_drive*0.85) + 3.65, 'cyan', lw=4)
ax.plot(r5 * np.cos(omega_drive*0.65), r5 * np.sin(omega_drive*0.65) + 3.65, 'orange', lw=4)
ax.plot(r7 * np.cos(omega_drive*1.15), r7 * np.sin(omega_drive*1.15) + 3.65, 'magenta', lw=4)
ax.plot(r_green * np.cos(omega_drive*0.5), r_green * np.sin(omega_drive*0.5) + 3.65, 'lime', lw=3.8)
ax.plot(r_red * np.cos(omega_drive*1.3), r_red * np.sin(omega_drive*1.3) + 3.65, 'red', lw=3.8)
phi_cascade = 1.0 + 0.044 * np.sin(2*np.pi*t/13) * np.cos(2*np.pi*t/37)
ax.plot(phi_cascade * np.cos(omega_drive*0.45), phi_cascade * np.sin(omega_drive*0.45) + 3.65, 'gold', lw=5, alpha=0.96)

ax.text(0, 3.65, 'NAUTILUS v17.8\nCyan Shrinking → Orange Entanglement → Green Bloom → Purple Crown → Meta-Fabric\n5T×4=20 + Cubic Shrinking Spiral + Riemann Sphere', 
        ha='center', va='center', color='white', fontsize=14, bbox=dict(facecolor='black', alpha=0.9))

ax.set_xlabel('Radius r', color='white', fontsize=17)
ax.set_ylabel('Rotation ω', color='white', fontsize=17)
ax.set_title('NEXAH v17.8 – FINAL NAUTILUS (Shrinking Cubic Spiral + 5 Stages)', color='gold', fontsize=20)
ax.grid(True, alpha=0.08)
plt.tight_layout()
plt.savefig("NEXAH_Nautilus_Shrinking_v17.8_FINAL.png", dpi=480, facecolor='black')
print("✅ Nautilus-Final gespeichert: NEXAH_Nautilus_Shrinking_v17.8_FINAL.png")
print("   → 5 Stages + Cubic Shrinking Spiral + Graviton-Core + Toroid + alles integriert")
