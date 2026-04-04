import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

print("🚀 NEXAH v17.5_3D – Cube im Oval mit Rotation\n")

fig = plt.figure(figsize=(14, 12), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

# Oval Base
theta = np.linspace(0, 2*np.pi, 200)
phi = np.linspace(0, np.pi, 100)
Theta, Phi = np.meshgrid(theta, phi)
x = 3.3 * np.cos(Theta) * np.sin(Phi)
y = 2.1 * np.sin(Theta) * np.sin(Phi)
z = 0.4 * np.cos(Phi)
ax.plot_surface(x, y, z, alpha=0.25, color='orange', edgecolor='gold', linewidth=0.5)

# Cube im Oval (rotierend)
t = np.linspace(0, 2*np.pi, 8)
for i in range(8):
    rot = t[i] * 0.8
    cube_x = np.array([-1,1,1,-1,-1,1,1,-1]) * 0.9
    cube_y = np.array([-1,-1,1,1,-1,-1,1,1]) * 0.9
    cube_z = np.array([-1,-1,-1,-1,1,1,1,1]) * 0.9
    # Rotation um y-Achse
    rx = cube_x * np.cos(rot) - cube_z * np.sin(rot)
    rz = cube_x * np.sin(rot) + cube_z * np.cos(rot)
    ax.plot(rx, cube_y, rz + 0.3, color='white', lw=2.5, alpha=0.9)

ax.text(0, 0, 0.3, 'ANU\nCORE 0.01', color='magenta', fontsize=16, ha='center', weight='bold')

ax.set_xlabel('r', color='white')
ax.set_ylabel('ω', color='white')
ax.set_zlabel('z', color='white')
ax.set_title('NEXAH v17.5_3D – Cube im Oval (Rotation)', color='gold', fontsize=18)
plt.tight_layout()
plt.savefig("NEXAH_3D_Cube_in_Oval_v17.5.png", dpi=420, facecolor='black')
print("✅ 3D-Cube gespeichert: NEXAH_3D_Cube_in_Oval_v17.5.png")
