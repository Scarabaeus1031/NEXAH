# ============================================================
# NEXAH — Generate Clusters (Simple Binning)
# ============================================================

import numpy as np
import os

# ------------------------------------------------------------
# Load trajectory
# ------------------------------------------------------------
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "..", "data")

traj_path = os.path.join(data_path, "trajectory.npy")

if not os.path.exists(traj_path):
    raise RuntimeError("❌ trajectory.npy not found. Run trajectory script first.")

traj = np.load(traj_path)

# ------------------------------------------------------------
# Simple coarse clustering (grid-based)
# ------------------------------------------------------------
# discretize space into bins
bins = 10

mins = traj.min(axis=0)
maxs = traj.max(axis=0)

norm = (traj - mins) / (maxs - mins + 1e-9)
clusters = (norm * bins).astype(int)

# flatten cluster id
cluster_ids = clusters[:,0]*100 + clusters[:,1]*10 + clusters[:,2]

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
clusters_path = os.path.join(data_path, "clusters.npy")
np.save(clusters_path, cluster_ids)

print(f"[✓] clusters saved: {clusters_path}")
