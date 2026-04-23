# ⚡ NEXAH Smoothed Stability Flow

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import os

print("⚡ NEXAH Smoothed Stability Flow")

# =========================
# DATA
# =========================
t = np.linspace(0, 20, 600)

x = np.sin(t) + 0.2*np.sin(5*t)
y = np.cos(t) + 0.2*np.cos(3*t)
z = np.sin(2*t)

points = np.vstack([x, y, z]).T

# =========================
# NEIGHBORS
# =========================
k = 20
nbrs = NearestNeighbors(n_neighbors=k).fit(points)
distances, indices = nbrs.kneighbors(points)

density = distances.mean(axis=1)
density_norm = (density - density.min()) / (density.max() - density.min())

# =========================
# GRADIENT
# =========================
gradients = np.zeros_like(points)

for i in range(len(points)):
    neighbors = points[indices[i]]
    diff = neighbors - points[i]
    
    weights = (density_norm[indices[i]] - density_norm[i]).reshape(-1,1)
    gradients[i] = np.sum(weights * diff, axis=0)

# normalize
norm = np.linalg.norm(gradients, axis=1, keepdims=True)
norm[norm == 0] = 1
gradients /= norm

flow = -gradients

# =========================
# SMOOTH FLOW
# =========================
flow_smooth = np.zeros_like(flow)

for i in range(len(points)):
    flow_smooth[i] = np.mean(flow[indices[i]], axis=0)

# normalize again
norm = np.linalg.norm(flow_smooth, axis=1, keepdims=True)
norm[norm == 0] = 1
flow_smooth /= norm

# =========================
# OUTPUT
# =========================
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "..", "outputs", "demo")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_stability_flow_smooth.png")

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(6,6))

ax.scatter(points[:,0], points[:,1],
           c=density_norm, s=10)

ax.quiver(points[:,0], points[:,1],
          flow_smooth[:,0], flow_smooth[:,1],
          scale=20)

ax.set_title("Smoothed Stability Flow (α-β)")
ax.set_xlabel("α")
ax.set_ylabel("β")

plt.tight_layout()
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

plt.show()
