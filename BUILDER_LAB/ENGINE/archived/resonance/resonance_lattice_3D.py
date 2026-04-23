import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
X_SIZE = 5  # X dimension of the grid
Y_SIZE = 5  # Y dimension of the grid

# Resonance function, for example, could be based on a sine function
def resonance_function(x, y):
    return np.sin(x) * np.cos(y)

# ---------------------------------------------------------
# FUNCTION TO GENERATE 3D RESONANCE LATTICE
# ---------------------------------------------------------
def generate_resonance_lattice(x_size, y_size):
    x = np.linspace(-5, 5, x_size)
    y = np.linspace(-5, 5, y_size)
    x, y = np.meshgrid(x, y)
    z = resonance_function(x, y)  # Apply resonance function to get z values
    return x, y, z

# ---------------------------------------------------------
# PLOT RESONANCE LATTICE (3D)
# ---------------------------------------------------------
x, y, z = generate_resonance_lattice(X_SIZE, Y_SIZE)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')

ax.set_title("Resonance Lattice (3D Resonance Grid)")
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z (Resonance Value)")
plt.tight_layout()
plt.savefig("Resonance_Lattice_3D.png")
plt.show()
