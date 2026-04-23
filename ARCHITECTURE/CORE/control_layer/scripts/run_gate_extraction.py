# ARCHITECTURE/CORE/control_layer/scripts/run_gate_extraction.py

import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import cKDTree

# --------------------------------
# Vector field (same as before)
# --------------------------------
def field(x, y):
    dx = y - 0.3 * x - x * (x**2 + y**2)
    dy = -x - 0.3 * y - y * (x**2 + y**2)
    return np.array([dx, dy])


# --------------------------------
# Load separatrix points
# --------------------------------
# (reuse from your pipeline)
data = np.load("ARCHITECTURE/CORE/control_layer/outputs/demo/separatrix_points.npy")

points = data[:, :2]


# --------------------------------
# Local metrics
# --------------------------------
tree = cKDTree(points)

def local_density(p, k=10):
    d, _ = tree.query(p, k=k)
    return np.mean(d)

def flow_alignment(p, target=np.array([0.0, 0.0])):
    f = field(p[0], p[1])
    direction = target - p
    return np.dot(f, direction) / (np.linalg.norm(f) * np.linalg.norm(direction) + 1e-6)


def curvature_estimate(p, k=6):
    d, idx = tree.query(p, k=k)
    neighbors = points[idx]
    cov = np.cov(neighbors.T)
    eigvals = np.linalg.eigvals(cov)
    return np.min(eigvals) / (np.max(eigvals) + 1e-6)


# --------------------------------
# Gate scoring
# --------------------------------
scores = []

for p in points:
    density = local_density(p)
    align = flow_alignment(p)
    curv = curvature_estimate(p)

    score = (
        1.0 / (density + 1e-3)   # sparse → sharper boundary
        + 2.0 * align            # flow toward center
        - 1.5 * curv             # avoid chaotic curvature
    )

    scores.append(score)

scores = np.array(scores)


# --------------------------------
# Select best gates
# --------------------------------
N_GATES = 6
idx = np.argsort(scores)[-N_GATES:]
gates = points[idx]


# --------------------------------
# Save
# --------------------------------
np.save(
    "ARCHITECTURE/CORE/control_layer/outputs/demo/gate_points.npy",
    gates
)


# --------------------------------
# Plot
# --------------------------------
plt.figure(figsize=(8, 8))

# background field
xx, yy = np.meshgrid(np.linspace(-2, 2, 50), np.linspace(-2, 2, 50))
u, v = field(xx, yy)
plt.streamplot(xx, yy, u, v, color="black", density=1.2)

# separatrix
plt.scatter(points[:, 0], points[:, 1], s=20, color="black", alpha=0.6, label="separatrix")

# gates
plt.scatter(gates[:, 0], gates[:, 1], s=120, color="magenta", edgecolor="white", label="gates")

# center
plt.scatter(0, 0, s=150, color="yellow", edgecolor="black", label="core")

plt.title("NEXAH Gate Extraction")
plt.legend()
plt.grid(True)

plt.savefig(
    "ARCHITECTURE/CORE/control_layer/outputs/demo/nexah_gate_extraction.png",
    dpi=150
)

print("✔ Saved → nexah_gate_extraction.png")
print("✔ Gates:", gates)

# --------------------------------
# SAVE separatrix points
# --------------------------------
np.save(
    "ARCHITECTURE/CORE/control_layer/outputs/demo/separatrix_points.npy",
    np.array(separatrix_points)
)

print("✔ Saved → separatrix_points.npy")
