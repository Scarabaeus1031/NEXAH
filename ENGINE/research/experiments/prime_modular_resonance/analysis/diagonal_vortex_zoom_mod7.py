# diagonal_vortex_zoom_mod7.py

import numpy as np
import matplotlib.pyplot as plt

# Deine Punkte (z.B. aus Trajectory)
points = np.array(trajectory_points)  # shape (N,2)

# Diagonalband auswählen
mask = np.abs(points[:,1] - points[:,0]) < 0.08
filtered = points[mask]

# lokale Richtungsvektoren
vectors = np.diff(filtered, axis=0)
positions = filtered[:-1]

plt.figure(figsize=(6,6))
plt.quiver(
    positions[:,0], positions[:,1],
    vectors[:,0], vectors[:,1],
    angles='xy', scale_units='xy', scale=1
)

plt.scatter(filtered[:,0], filtered[:,1], s=5)

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)

plt.title("Diagonal Vortex Zoom (mod 7)")
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.grid()
plt.show()
