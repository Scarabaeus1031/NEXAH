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
# LORENZ
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
# FIELD
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
# OPERATORS
# =========================

def compute_divergence(points, vectors):
    nbrs = NearestNeighbors(n_neighbors=K_NEIGHBORS).fit(points)
    _, indices = nbrs.kneighbors(points)

    div = []

    for i, neigh in enumerate(indices):
        p0 = points[i]
        v0 = vectors[i]
        d = 0.0

        for j in neigh[1:]:
            dp = points[j] - p0
            dv = vectors[j] - v0
            if np.linalg.norm(dp) > 0:
                d += np.dot(dv, dp) / (np.linalg.norm(dp)**2)

        div.append(d / (K_NEIGHBORS - 1))

    return np.array(div)

def compute_curl(points, vectors):
    nbrs = NearestNeighbors(n_neighbors=K_NEIGHBORS).fit(points)
    _, indices = nbrs.kneighbors(points)

    curl_mag = []

    for i, neigh in enumerate(indices):
        p0 = points[i]
        v0 = vectors[i]
        c = np.zeros(3)

        for j in neigh[1:]:
            dp = points[j] - p0
            dv = vectors[j] - v0
            if np.linalg.norm(dp) > 0:
                c += np.cross(dp, dv) / (np.linalg.norm(dp)**2)

        curl_mag.append(np.linalg.norm(c))

    return np.array(curl_mag)

# =========================
# RUN
# =========================

print("Running Discovery Core V21 (Field Coupling)...")

xs, ys, zs = simulate()
vx, vy, vz = compute_field(xs, ys, zs)

points = np.vstack([xs, ys, zs]).T
vectors = np.vstack([vx, vy, vz]).T

div = compute_divergence(points, vectors)
curl = compute_curl(points, vectors)

# =========================
# COUPLING
# =========================

# Zeitliche Ableitungen
d_div = np.gradient(div)
d_curl = np.gradient(curl)

# =========================
# VISUALS
# =========================

plt.figure(figsize=(14,10))

# --- time coupling
plt.subplot(221)
plt.plot(curl, label="curl")
plt.plot(d_div, label="d(div)/dt")
plt.title("Curl ↔ d(Divergence)/dt")
plt.legend()

plt.subplot(222)
plt.plot(div, label="div")
plt.plot(d_curl, label="d(curl)/dt")
plt.title("Div ↔ d(Curl)/dt")
plt.legend()

# --- phase coupling
plt.subplot(223)
plt.scatter(curl, d_div, s=2)
plt.title("Curl vs d(Div)/dt")

plt.subplot(224)
plt.scatter(div, d_curl, s=2)
plt.title("Div vs d(Curl)/dt")

plt.tight_layout()

out = os.path.join(OUTPUT_DIR, "v21_field_coupling.png")
plt.savefig(out, dpi=150)

print(f"Saved: {out}")
