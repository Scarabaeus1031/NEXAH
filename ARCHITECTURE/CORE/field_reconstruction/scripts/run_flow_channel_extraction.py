# ⚡ NEXAH Flow Channel Extraction

# Extract stable navigation channels from reconstructed stability flow

import os

import numpy as np

import matplotlib.pyplot as plt

from sklearn.neighbors import NearestNeighbors

print("⚡ NEXAH Flow Channel Extraction")

# =========================

# 1. DATA

# =========================

t = np.linspace(0, 20, 600)

x = np.sin(t) + 0.2 * np.sin(5 * t)

y = np.cos(t) + 0.2 * np.cos(3 * t)

z = np.sin(2 * t)

points = np.vstack([x, y, z]).T

# =========================

# 2. LOCAL DENSITY / BOUNDARY STRENGTH

# =========================

k = 20

nbrs = NearestNeighbors(n_neighbors=k).fit(points)

distances, indices = nbrs.kneighbors(points)

density = distances.mean(axis=1)

density_norm = (density - density.min()) / (density.max() - density.min())

# =========================

# 3. STABILITY FLOW (same logic as previous script)

# =========================

gradients = np.zeros_like(points)

for i in range(len(points)):

    neighbors = points[indices[i]]

    diff = neighbors - points[i]

    weights = (density_norm[indices[i]] - density_norm[i]).reshape(-1, 1)

    gradients[i] = np.sum(weights * diff, axis=0)

# normalize gradients

norm = np.linalg.norm(gradients, axis=1, keepdims=True)

norm[norm == 0] = 1.0

gradients /= norm

# negative gradient = direction toward stability

flow = -gradients

# smooth flow by neighborhood averaging

flow_smooth = np.zeros_like(flow)

for i in range(len(points)):

    flow_smooth[i] = np.mean(flow[indices[i]], axis=0)

norm = np.linalg.norm(flow_smooth, axis=1, keepdims=True)

norm[norm == 0] = 1.0

flow_smooth /= norm

# =========================

# 4. FLOW COHERENCE

# =========================

# Idea:

# stable channels = places where neighboring arrows point in similar direction

coherence = np.zeros(len(points))

for i in range(len(points)):

    local_flow = flow_smooth[indices[i]]

    mean_vec = np.mean(local_flow, axis=0)

    coherence[i] = np.linalg.norm(mean_vec)

coherence_norm = (coherence - coherence.min()) / (coherence.max() - coherence.min() + 1e-12)

# =========================

# 5. CHANNEL MASK

# =========================

# stable channel = low boundary strength + high directional coherence

channel_score = (1.0 - density_norm) * coherence_norm

threshold = np.percentile(channel_score, 70)

channel_mask = channel_score >= threshold

non_channel_mask = ~channel_mask

# =========================

# 6. OUTPUT

# =========================

base_dir = os.path.dirname(__file__)

out_dir = os.path.join(base_dir, "..", "outputs", "demo")

os.makedirs(out_dir, exist_ok=True)

out_path = os.path.join(out_dir, "nexah_flow_channels.png")

# =========================

# 7. PLOT

# =========================

fig = plt.figure(figsize=(13, 5))

# --- 3D

ax = fig.add_subplot(121, projection="3d")

ax.scatter(

    points[non_channel_mask, 0],

    points[non_channel_mask, 1],

    points[non_channel_mask, 2],

    c="lightgray",

    s=8,

    alpha=0.35,

    label="background"

)

ax.scatter(

    points[channel_mask, 0],

    points[channel_mask, 1],

    points[channel_mask, 2],

    c=channel_score[channel_mask],

    cmap="viridis",

    s=20,

    label="flow channel"

)

# show arrows only on channels

step_idx = np.where(channel_mask)[0][::3]

ax.quiver(

    points[step_idx, 0],

    points[step_idx, 1],

    points[step_idx, 2],

    flow_smooth[step_idx, 0],

    flow_smooth[step_idx, 1],

    flow_smooth[step_idx, 2],

    length=0.12,

    normalize=True,

    color="black"

)

ax.set_title("3D Flow Channel Extraction")

ax.set_xlabel("α")

ax.set_ylabel("β")

ax.set_zlabel("γ")

ax.legend()

# --- 2D projection

ax2 = fig.add_subplot(122)

ax2.scatter(

    points[non_channel_mask, 0],

    points[non_channel_mask, 1],

    c="lightgray",

    s=8,

    alpha=0.35

)

sc = ax2.scatter(

    points[channel_mask, 0],

    points[channel_mask, 1],

    c=channel_score[channel_mask],

    cmap="viridis",

    s=22

)

step_idx_2d = np.where(channel_mask)[0][::3]

ax2.quiver(

    points[step_idx_2d, 0],

    points[step_idx_2d, 1],

    flow_smooth[step_idx_2d, 0],

    flow_smooth[step_idx_2d, 1],

    angles="xy",

    scale_units="xy",

    scale=18,

    color="black"

)

ax2.set_title("α-β Flow Channels")

ax2.set_xlabel("α")

ax2.set_ylabel("β")

fig.colorbar(sc, ax=ax2, label="channel strength")

plt.tight_layout()

plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

print("""

🧠 Interpretation:

Bright regions = stable flow channels

Gray regions   = weak / noisy / boundary-dominated structure

→ extracts usable navigation paths

→ highlights coherent motion corridors

→ reduces visual noise and local flow artifacts

""")

plt.show()
