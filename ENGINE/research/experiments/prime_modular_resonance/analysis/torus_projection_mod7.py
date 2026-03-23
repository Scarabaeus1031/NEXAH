# torus_projection_mod7.py

import numpy as np
import matplotlib.pyplot as plt

points = np.array(trajectory_points)

# Winkel auf Kreis
theta = 2*np.pi * (points[:,0] + 1)/2
phi   = 2*np.pi * (points[:,1] + 1)/2

R = 1.0
r = 0.3

X = (R + r*np.cos(phi)) * np.cos(theta)
Y = (R + r*np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

ax.plot(X, Y, Z, linewidth=0.5)

ax.set_title("Torus Projection (mod 7)")
plt.show()
