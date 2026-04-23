import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# =========================
# SETUP
# =========================

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

dt = 0.01
steps = 5000

K_NEIGHBORS = 20

# =========================
# LORENZ SYSTEM
# =========================

def lorenz(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

def simulate():
    xs, ys, zs = [], [], []
    x, y, z = 1.0, 1.0, 1.0

    for _ in range(steps):
        dx, dy, dz = lorenz(x, y, z)
        x += dx * dt
        y += dy * dt
        z += dz * dt

        xs.append(x)
        ys.append(y)
        zs.append(z)

    return np.array(xs), np.array(ys), np.array(zs)

# =========================
# FIELD CONSTRUCTION
# =========================

def compute_field(xs, ys, zs):
    vx, vy, vz = [], [], []
    for x, y, z in zip(xs, ys, zs):
        dx, dy, dz = lorenz(x, y, z)
        vx.append(dx)
        vy.append(dy)
        vz.append(dz)
    return np.array(vx), np.array(vy), np.array(vz)

# =========================
# LOCAL OPERATORS
# =========================

def compute_divergence(points, vectors):
    nbrs = NearestNeighbors(n_neighbors=K_NEIGHBORS).fit(points)
    _, indices = nbrs.kneighbors(points)

    divergence = []

    for i, neighbors in enumerate(indices):
        p0 = points[i]
        v0 = vectors[i]

        div = 0.0

        for j in neighbors[1:]:
            dp = points[j] - p0
            dv = vectors[j] - v0

            if np.linalg.norm(dp) > 0:
                div += np.dot(dv, dp) / (np.linalg.norm(dp)**2)

        divergence.append(div / (K_NEIGHBORS - 1))

    return np.array(divergence)

def compute_curl(points, vectors):
    nbrs = NearestNeighbors(n_neighbors=K_NEIGHBORS).fit(points)
    _, indices = nbrs.kneighbors(points)

    curl_mag = []

    for i, neighbors in enumerate(indices):
        p0 = points[i]
        v0 = vectors[i]

        curl = np.zeros(3)

        for j in neighbors[1:]:
            dp = points[j] - p0
            dv = vectors[j] - v0

            if np.linalg.norm(dp) > 0:
                curl += np.cross(dp, dv) / (np.linalg.norm(dp)**2)

        curl_mag.append(np.linalg.norm(curl))

    return np.array(curl_mag)

# =========================
# RUN
# =========================

print("Running Discovery Core V20 (Maxwell Field)...")

xs, ys, zs = simulate()
vx, vy, vz = compute_field(xs, ys, zs)

points = np.vstack([xs, ys, zs]).T
vectors = np.vstack([vx, vy, vz]).T

divergence = compute_divergence(points, vectors)
curl = compute_curl(points, vectors)

# =========================
# VISUALIZATION
# =========================

fig = plt.figure(figsize=(14, 10))

# --- 3D Divergence Field
ax1 = fig.add_subplot(221, projection='3d')
p = ax1.scatter(xs, ys, zs, c=divergence, s=2)
ax1.set_title("Divergence Field (Sources/Sinks)")
fig.colorbar(p, ax=ax1)

# --- 3D Curl Field
ax2 = fig.add_subplot(222, projection='3d')
p2 = ax2.scatter(xs, ys, zs, c=curl, s=2)
ax2.set_title("Curl Field (Rotation)")
fig.colorbar(p2, ax=ax2)

# --- Time Series
ax3 = fig.add_subplot(223)
ax3.plot(divergence, label="divergence")
ax3.plot(curl, label="curl")
ax3.set_title("Field Operators over Time")
ax3.legend()

# --- Relation
ax4 = fig.add_subplot(224)
ax4.scatter(divergence, curl, s=2)
ax4.set_title("Divergence vs Curl")

plt.tight_layout()

output_path = os.path.join(OUTPUT_DIR, "v20_maxwell_field.png")
plt.savefig(output_path, dpi=150)

print(f"Saved: {output_path}")
