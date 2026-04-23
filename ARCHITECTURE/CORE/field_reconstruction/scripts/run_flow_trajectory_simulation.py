# ⚡ NEXAH Flow Trajectory Simulation
# Simulates motion along extracted flow field

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

print("⚡ NEXAH Flow Trajectory Simulation")

# =========================
# 1. DATA
# =========================
t = np.linspace(0, 20, 600)

x = np.sin(t) + 0.2 * np.sin(5 * t)
y = np.cos(t) + 0.2 * np.cos(3 * t)
z = np.sin(2 * t)

points = np.vstack([x, y, z]).T

# =========================
# 2. NEIGHBOR STRUCTURE
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

# smooth flow
flow_smooth = np.zeros_like(flow)
for i in range(len(points)):
    flow_smooth[i] = np.mean(flow[indices[i]], axis=0)

norm = np.linalg.norm(flow_smooth, axis=1, keepdims=True)
norm[norm == 0] = 1.0
flow_smooth /= norm

# =========================
# 4. TRAJECTORY SIMULATION
# =========================

def step(position):
    # find nearest point in cloud
    distances = np.linalg.norm(points - position, axis=1)
    idx = np.argmin(distances)

    direction = flow_smooth[idx]

    # small step
    return position + 0.05 * direction


# start point (choose something near a channel)
start_idx = 100
trajectory = [points[start_idx]]

pos = points[start_idx].copy()

for _ in range(120):
    pos = step(pos)
    trajectory.append(pos.copy())

trajectory = np.array(trajectory)

# =========================
# 5. OUTPUT
# =========================
base_dir = os.path.dirname(__file__)
out_dir = os.path.join(base_dir, "..", "outputs", "demo")
os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_flow_trajectory.png")

# =========================
# 6. PLOT
# =========================
fig = plt.figure(figsize=(13, 5))

# --- 3D
ax = fig.add_subplot(121, projection="3d")

ax.scatter(points[:, 0], points[:, 1], points[:, 2],
           c="lightgray", s=5, alpha=0.3)

ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],
        color="red", linewidth=2, label="trajectory")

ax.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2],
           c="green", s=60, label="start")

ax.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2],
           c="blue", s=60, label="end")

ax.set_title("3D Flow Trajectory")
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.set_zlabel("γ")
ax.legend()

# --- 2D projection
ax2 = fig.add_subplot(122)

ax2.scatter(points[:, 0], points[:, 1],
            c="lightgray", s=5, alpha=0.3)

ax2.plot(trajectory[:, 0], trajectory[:, 1],
         color="red", linewidth=2)

ax2.scatter(trajectory[0, 0], trajectory[0, 1],
            c="green", s=60)

ax2.scatter(trajectory[-1, 0], trajectory[-1, 1],
            c="blue", s=60)

ax2.set_title("α-β Trajectory")
ax2.set_xlabel("α")
ax2.set_ylabel("β")

plt.tight_layout()
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

print("""
🧠 Interpretation:

Red path = simulated motion through the field

→ follows stable flow directions
→ naturally bends along channels
→ reveals preferred system trajectories

This is true FIELD NAVIGATION.
""")

plt.show()
