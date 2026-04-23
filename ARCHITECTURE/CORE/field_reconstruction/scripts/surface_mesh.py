import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

print("⚡ NEXAH Surface Reconstruction (Mesh)")

# deine echten Punkte einsetzen
points = np.loadtxt("your_points.txt")  # oder aus deinem Script

# nur α, β Projektion für triangulation
xy = points[:, :2]

tri = Delaunay(xy)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_trisurf(points[:,0], points[:,1], points[:,2],
                triangles=tri.simplices,
                cmap='viridis', alpha=0.7)

ax.scatter(points[:,0], points[:,1], points[:,2],
           s=5, color='black')

ax.set_title("Reconstructed Surface (Sheet)")

plt.savefig("outputs/demo/nexah_surface_mesh.png", dpi=200)

print("✔ Saved → outputs/demo/nexah_surface_mesh.png")
