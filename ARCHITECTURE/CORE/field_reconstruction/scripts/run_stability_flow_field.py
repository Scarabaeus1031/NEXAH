# ⚡ NEXAH Stability Flow Field (Vector Field)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import os

print("⚡ NEXAH Stability Flow Field")

# =========================
# 1. DATA
# =========================
t = np.linspace(0, 20, 600)

x = np.sin(t) + 0.2*np.sin(5*t)
y = np.cos(t) + 0.2*np.cos(3*t)
z = np.sin(2*t)

points = np.vstack([x, y, z]).T

# =========================
# 2. DENSITY (Boundary Strength)
# =========================
k = 15
nbrs = NearestNeighbors(n_neighbors=k).fit(points)
distances, indices = nbrs.kneighbors(points)

density = distances.mean(axis=1)
density_norm = (density - density.min()) / (density.max() - density.min())

# =========================
# 3. GRADIENT ESTIMATION
# =========================
gradients = np.zeros_like(points)

for i in range(len(points)):
    neighbors = points[indices[i]]
    diff = neighbors - points[i]
    
    # weight by density difference
    weights = (density_norm[indices[i]] - density_norm[i]).reshape(-1,1)
    
    grad = np.sum(weights * diff, axis=0)
    gradients[i] = grad

# normalize vectors
norm = np.linalg.norm(gradients, axis=1, keepdims=True)
norm[norm == 0] = 1
gradients /= norm

# =========================
# 4. STABILITY FLOW
# =========================
flow = -gradients  # invert → towards stability

# =========================
# 5. OUTPUT PATH
# =========================
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "..", "outputs", "demo")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_stability_flow.png")

# =========================
# 6. PLOT
# =========================
fig = plt.figure(figsize=(12,5))

# 3D Flow
ax = fig.add_subplot(121, projection='3d')

ax.scatter(points[:,0], points[:,1], points[:,2],
           c=density_norm, s=10)

ax.quiver(points[:,0], points[:,1], points[:,2],
          flow[:,0], flow[:,1], flow[:,2],
          length=0.2, normalize=True)

ax.set_title("3D Stability Flow Field")

# 2D Projection
ax2 = fig.add_subplot(122)

ax2.scatter(points[:,0], points[:,1],
            c=density_norm, s=10)

ax2.quiver(points[:,0], points[:,1],
           flow[:,0], flow[:,1],
           angles='xy', scale_units='xy', scale=10)

ax2.set_title("α-β Stability Flow")
ax2.set_xlabel("α")
ax2.set_ylabel("β")

plt.tight_layout()
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

# =========================
# 7. INTERPRETATION
# =========================
print("""
🧠 Interpretation:

Arrows = direction toward stability

→ system can be guided
→ reveals safe motion directions
→ defines natural flow in field

This is the bridge to CONTROL.
""")

plt.show()
