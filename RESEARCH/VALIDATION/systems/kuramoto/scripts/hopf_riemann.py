import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Hopf-Fibration: einfache Faser auf der Sphere
def hopf_fiber(theta, alpha=0.0):
    """Eine einzelne Faser (Kreis) auf der Riemann-Sphäre"""
    x = np.cos(theta) * np.cos(alpha)
    y = np.cos(theta) * np.sin(alpha)
    z = np.sin(theta)
    return x, y, z

# Riemann-Sphäre (Basis)
theta = np.linspace(0, 2*np.pi, 200)
phi = np.linspace(0, np.pi, 100)
phi, theta = np.meshgrid(phi, theta)
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Beispiel: mehrere Fasern um die pinke Achse
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Riemann-Sphäre (transparent)
ax.plot_wireframe(x, y, z, color='lightblue', alpha=0.3)

# Pinke Achse (Yugo)
ax.plot([0,0], [0,0], [-1,1], color='magenta', linewidth=4, label='Pinke Achse (Yugo)')

# Beispiel-Fasern (Theta, Tao, Dao, Iota)
for i, alpha in enumerate([0, np.pi/4, np.pi/2, 3*np.pi/4]):
    fx, fy, fz = hopf_fiber(theta, alpha)
    color = ['cyan', 'orange', 'green', 'red'][i]
    label = ['Theta', 'Tao (Zopf)', 'Dao', 'Iota'][i]
    ax.plot(fx, fy, fz, color=color, linewidth=2, label=label)

ax.set_title('Hopf-Fibration + Pinke Achse + Vier Spheres (NEXAH)')
ax.legend()
plt.show()
