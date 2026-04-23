import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

print("⚡ NEXAH Boundary → Surface Sheet Reconstruction")

# --------------------------------------------------
# 1. LOAD DATA (reuse your existing boundary points)
# --------------------------------------------------

# 👉 hier ersetzen mit deinen echten Daten falls nötig
# Beispiel: α, β, γ aus bestehendem Script

np.random.seed(0)

# Fake structure (ersetzt durch deine echten Daten)
t = np.linspace(0, 20, 400)
x = np.sin(t) + 0.1 * np.random.randn(len(t))
y = np.cos(t) + 0.1 * np.random.randn(len(t))
z = np.sin(2*t) + 0.1 * np.random.randn(len(t))

points = np.vstack([x, y, z]).T

# --------------------------------------------------
# 2. LOCAL SURFACE ESTIMATION (PCA)
# --------------------------------------------------

nbrs = NearestNeighbors(n_neighbors=15).fit(points)
distances, indices = nbrs.kneighbors(points)

normals = []
curvature = []

for i in range(len(points)):
    neighborhood = points[indices[i]]

    pca = PCA(n_components=3)
    pca.fit(neighborhood)

    normal = pca.components_[-1]
    normals.append(normal)

    # curvature ~ smallest eigenvalue
    curvature.append(pca.explained_variance_[-1])

normals = np.array(normals)
curvature = np.array(curvature)

# --------------------------------------------------
# 3. PLOT
# --------------------------------------------------

fig = plt.figure(figsize=(14,10))

# --- Q1: point cloud
ax1 = fig.add_subplot(221, projection='3d')
ax1.scatter(points[:,0], points[:,1], points[:,2],
            c=curvature, cmap='viridis', s=10)
ax1.set_title("Point Cloud + Curvature")

# --- Q2: normals (sheet orientation)
ax2 = fig.add_subplot(222, projection='3d')
ax2.quiver(points[:,0], points[:,1], points[:,2],
           normals[:,0], normals[:,1], normals[:,2],
           length=0.2, normalize=True)
ax2.set_title("Local Surface Normals")

# --- Q3: sheet detection (low curvature)
ax3 = fig.add_subplot(223, projection='3d')
mask = curvature < np.percentile(curvature, 40)

ax3.scatter(points[mask][:,0],
            points[mask][:,1],
            points[mask][:,2],
            c='cyan', s=10, label='sheet')

ax3.scatter(points[~mask][:,0],
            points[~mask][:,1],
            points[~mask][:,2],
            c='purple', s=5, alpha=0.3, label='non-sheet')

ax3.legend()
ax3.set_title("Sheet Extraction")

# --- Q4: projection (α-β view)
ax4 = fig.add_subplot(224)
ax4.scatter(points[:,0], points[:,1],
            c=curvature, cmap='viridis', s=10)
ax4.set_title("α-β Projection (Sheet footprint)")

plt.tight_layout()
plt.savefig("outputs/demo/nexah_surface_sheet.png", dpi=200)

print("✔ Saved → outputs/demo/nexah_surface_sheet.png")

print("""
🧠 Interpretation:
Low curvature → sheet structure
High curvature → folds / transitions
→ reveals manifold geometry
""")
