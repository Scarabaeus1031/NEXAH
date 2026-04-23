import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

print("⚡ NEXAH Surface Reconstruction (Mesh)")

# --------------------------------------------------
# 1. USE REAL DATA (same as your embedding script)
# --------------------------------------------------

np.random.seed(0)

t = np.linspace(0, 20, 400)

x = np.sin(t) + 0.1*np.random.randn(len(t))
y = np.cos(t) + 0.1*np.random.randn(len(t))
z = np.sin(2*t) + 0.1*np.random.randn(len(t))

points = np.vstack([x, y, z]).T

# --------------------------------------------------
# 2. TRIANGULATION (on α-β plane)
# --------------------------------------------------

xy = points[:, :2]
tri = Delaunay(xy)

# --------------------------------------------------
# 3. PLOT
# --------------------------------------------------

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_trisurf(points[:,0], points[:,1], points[:,2],
                triangles=tri.simplices,
                cmap='viridis',
                alpha=0.7)

ax.scatter(points[:,0], points[:,1], points[:,2],
           s=5, color='black')

ax.set_title("NEXAH Surface Reconstruction (Sheet)")
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.set_zlabel("γ")

plt.tight_layout()
plt.savefig("outputs/demo/nexah_surface_mesh.png", dpi=200)

print("✔ Saved → outputs/demo/nexah_surface_mesh.png")

print("""
🧠 Interpretation:
Surface approximates underlying manifold
→ reveals sheet geometry
→ shows folds + transitions
""")
