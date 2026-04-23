# ⚡ NEXAH Boundary Detection (robust version)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import os

print("⚡ NEXAH Boundary Detection")

# =========================
# 1. DATA (synthetic field)
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
# 5. OUTPUT PATH (FIXED)
# =========================
base_dir = os.path.dirname(__file__)

out_dir = os.path.join(base_dir, "..", "outputs", "demo")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_boundary_map.png")

# =========================
# 6. PLOT (3D)
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
# 7. PROJECTION (α-β)
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
# 8. SAVE
# =========================
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

# =========================
# 9. INTERPRETATION
# =========================
print("""
🧠 Interpretation:

Red = boundary / transition regions
Blue = stable core structure

→ identifies limits of reliable reconstruction
→ highlights potential regime boundaries
""")

plt.show()
