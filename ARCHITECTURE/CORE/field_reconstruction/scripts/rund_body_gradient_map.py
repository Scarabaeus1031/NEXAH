# ⚡ NEXAH Boundary Gradient Map

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import os

print("⚡ NEXAH Boundary Gradient Map")

# =========================
# DATA
# =========================
t = np.linspace(0, 20, 600)

x = np.sin(t) + 0.2*np.sin(5*t)
y = np.cos(t) + 0.2*np.cos(3*t)
z = np.sin(2*t)

points = np.vstack([x, y, z]).T

# =========================
# NEIGHBOR DISTANCE
# =========================
k = 15
nbrs = NearestNeighbors(n_neighbors=k).fit(points)
distances, _ = nbrs.kneighbors(points)

density = distances.mean(axis=1)

# normalize
density_norm = (density - density.min()) / (density.max() - density.min())

# =========================
# OUTPUT PATH
# =========================
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "..", "outputs", "demo")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_boundary_gradient.png")

# =========================
# PLOT
# =========================
fig = plt.figure(figsize=(12,5))

# 3D
ax = fig.add_subplot(121, projection='3d')
sc = ax.scatter(points[:,0], points[:,1], points[:,2],
                c=density_norm, s=15)

ax.set_title("3D Boundary Strength")
fig.colorbar(sc, ax=ax, label="boundary strength")

# 2D projection
ax2 = fig.add_subplot(122)
sc2 = ax2.scatter(points[:,0], points[:,1],
                  c=density_norm, s=15)

ax2.set_title("α-β Projection (Gradient)")
ax2.set_xlabel("α")
ax2.set_ylabel("β")

fig.colorbar(sc2, ax=ax2)

plt.tight_layout()
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

print("""
🧠 Interpretation:

Dark → stable regions
Bright → transition / boundary regions

→ continuous boundary field
→ reveals strength of transitions
""")

plt.show()
