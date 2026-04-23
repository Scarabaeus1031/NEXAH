import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

print("⚡ NEXAH Boundary Detection")

# =========================
# 1. DATA (same as before)
# =========================
t = np.linspace(0, 20, 600)
x = np.sin(t) + 0.2*np.sin(5*t)
y = np.cos(t) + 0.2*np.cos(3*t)
z = np.sin(2*t)

points = np.vstack([x, y, z]).T

# =========================
# 2. LOCAL DENSITY ESTIMATE
# =========================
k = 15
nbrs = NearestNeighbors(n_neighbors=k).fit(points)
distances, _ = nbrs.kneighbors(points)

# mean distance to neighbors
density = distances.mean(axis=1)

# =========================
# 3. NORMALIZE
# =========================
density_norm = (density - density.min()) / (density.max() - density.min())

# =========================
# 4. BOUNDARY CLASSIFICATION
# =========================
threshold = 0.6

boundary_mask = density_norm > threshold
core_mask = density_norm <= threshold

# =========================
# 5. PLOT (3D)
# =========================
fig = plt.figure(figsize=(12,5))

ax = fig.add_subplot(121, projection='3d')
ax.scatter(points[core_mask,0], points[core_mask,1], points[core_mask,2],
           c='blue', s=10, label='core')

ax.scatter(points[boundary_mask,0], points[boundary_mask,1], points[boundary_mask,2],
           c='red', s=20, label='boundary')

ax.set_title("3D Boundary Detection")
ax.legend()

# =========================
# 6. PROJECTION (α-β view)
# =========================
ax2 = fig.add_subplot(122)

ax2.scatter(points[core_mask,0], points[core_mask,1],
            c='blue', s=10)

ax2.scatter(points[boundary_mask,0], points[boundary_mask,1],
            c='red', s=20)

ax2.set_title("α-β Projection (Boundary Map)")
ax2.set_xlabel("α")
ax2.set_ylabel("β")

plt.tight_layout()

# =========================
# 7. SAVE
# =========================
out_path = "../outputs/demo/nexah_boundary_map.png"
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

# =========================
# 8. INSIGHT
# =========================
print("""
🧠 Interpretation:

Red = boundary / transition regions
Blue = stable core structure

→ identifies limits of reliable reconstruction
→ highlights potential regime boundaries
""")

plt.show()
