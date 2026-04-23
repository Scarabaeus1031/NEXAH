# ⚡ NEXAH Target-Guided Navigation
# Navigate through field toward a target using flow + attraction

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

print("⚡ NEXAH Target-Guided Navigation")

# =========================
# 1. DATA
# =========================
t = np.linspace(0, 20, 600)

x = np.sin(t) + 0.2 * np.sin(5 * t)
y = np.cos(t) + 0.2 * np.cos(3 * t)
z = np.sin(2 * t)

points = np.vstack([x, y, z]).T

# =========================
# 2. NEIGHBORS
# =========================
k = 20
nbrs = NearestNeighbors(n_neighbors=k).fit(points)
distances, indices = nbrs.kneighbors(points)

density = distances.mean(axis=1)
density_norm = (density - density.min()) / (density.max() - density.min() + 1e-12)

# =========================
# 3. FLOW FIELD
# =========================
gradients = np.zeros_like(points)

for i in range(len(points)):
    neighbors = points[indices[i]]
    diff = neighbors - points[i]
    weights = (density_norm[indices[i]] - density_norm[i]).reshape(-1, 1)
    gradients[i] = np.sum(weights * diff, axis=0)

# normalize
norm = np.linalg.norm(gradients, axis=1, keepdims=True)
norm[norm == 0] = 1.0
gradients /= norm

flow = -gradients

# smooth
flow_smooth = np.zeros_like(flow)
for i in range(len(points)):
    flow_smooth[i] = np.mean(flow[indices[i]], axis=0)

norm = np.linalg.norm(flow_smooth, axis=1, keepdims=True)
norm[norm == 0] = 1.0
flow_smooth /= norm

# =========================
# 4. TARGET NAVIGATION
# =========================

start = points[100]
target = points[450]

trajectory = [start]
pos = start.copy()

for _ in range(150):
    # nearest field direction
    d = np.linalg.norm(points - pos, axis=1)
    idx = np.argmin(d)

    flow_dir = flow_smooth[idx]

    # attraction toward target
    target_dir = target - pos
    target_dir /= (np.linalg.norm(target_dir) + 1e-12)

    # combine
    direction = 0.7 * flow_dir + 0.3 * target_dir
    direction /= np.linalg.norm(direction)

    pos = pos + 0.05 * direction
    trajectory.append(pos.copy())

trajectory = np.array(trajectory)

# =========================
# 5. OUTPUT
# =========================
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "..", "outputs", "demo")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_target_navigation.png")

# =========================
# 6. PLOT
# =========================
fig = plt.figure(figsize=(13, 5))

# 3D
ax = fig.add_subplot(121, projection="3d")

ax.scatter(points[:,0], points[:,1], points[:,2],
           c="lightgray", s=5, alpha=0.3)

ax.plot(trajectory[:,0], trajectory[:,1], trajectory[:,2],
        color="red", linewidth=2)

ax.scatter(*start, c="green", s=60, label="start")
ax.scatter(*target, c="blue", s=60, label="target")

ax.set_title("Target Guided Navigation")
ax.legend()

# 2D
ax2 = fig.add_subplot(122)

ax2.scatter(points[:,0], points[:,1],
            c="lightgray", s=5, alpha=0.3)

ax2.plot(trajectory[:,0], trajectory[:,1],
         color="red", linewidth=2)

ax2.scatter(start[0], start[1], c="green", s=60)
ax2.scatter(target[0], target[1], c="blue", s=60)

ax2.set_title("α-β Target Navigation")

plt.tight_layout()
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

print("""
🧠 Interpretation:

Trajectory balances:
- field stability (flow)
- goal direction (target)

→ navigates THROUGH structure
→ avoids unstable regions
→ demonstrates controllable dynamics

This is the first true CONTROL layer.
""")

plt.show()
