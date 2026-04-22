import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

dt = 0.01
steps = 5000
K = 20

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
        xs.append(x); ys.append(y); zs.append(z)

    return np.array(xs), np.array(ys), np.array(zs)

# =========================
# FIELD
# =========================

def compute_field(xs, ys, zs):
    vx, vy, vz = [], [], []
    for x, y, z in zip(xs, ys, zs):
        dx, dy, dz = lorenz(x, y, z)
        vx.append(dx); vy.append(dy); vz.append(dz)
    return np.array(vx), np.array(vy), np.array(vz)

# =========================
# OPERATORS
# =========================

def compute_div(points, vecs):
    nbrs = NearestNeighbors(n_neighbors=K).fit(points)
    _, idx = nbrs.kneighbors(points)

    div = []
    for i, neigh in enumerate(idx):
        p0 = points[i]
        v0 = vecs[i]
        val = 0
        for j in neigh[1:]:
            dp = points[j] - p0
            dv = vecs[j] - v0
            if np.linalg.norm(dp) > 0:
                val += np.dot(dv, dp)/(np.linalg.norm(dp)**2)
        div.append(val/(K-1))
    return np.array(div)

def compute_curl(points, vecs):
    nbrs = NearestNeighbors(n_neighbors=K).fit(points)
    _, idx = nbrs.kneighbors(points)

    curl = []
    for i, neigh in enumerate(idx):
        p0 = points[i]
        v0 = vecs[i]
        c = np.zeros(3)
        for j in neigh[1:]:
            dp = points[j] - p0
            dv = vecs[j] - v0
            if np.linalg.norm(dp) > 0:
                c += np.cross(dp, dv)/(np.linalg.norm(dp)**2)
        curl.append(np.linalg.norm(c))
    return np.array(curl)

# =========================
# CROSS CORRELATION
# =========================

def cross_corr(a, b, max_lag=200):
    lags = np.arange(-max_lag, max_lag)
    corr = []

    a = (a - np.mean(a)) / (np.std(a)+1e-8)
    b = (b - np.mean(b)) / (np.std(b)+1e-8)

    for lag in lags:
        if lag < 0:
            c = np.corrcoef(a[:lag], b[-lag:])[0,1]
        elif lag > 0:
            c = np.corrcoef(a[lag:], b[:-lag])[0,1]
        else:
            c = np.corrcoef(a, b)[0,1]
        corr.append(c)

    return lags, np.array(corr)

# =========================
# RUN
# =========================

print("Running V22...")

xs, ys, zs = simulate()
vx, vy, vz = compute_field(xs, ys, zs)

pts = np.vstack([xs, ys, zs]).T
vecs = np.vstack([vx, vy, vz]).T

div = compute_div(pts, vecs)
curl = compute_curl(pts, vecs)

lags1, c1 = cross_corr(curl, div)
lags2, c2 = cross_corr(div, curl)

# =========================
# VISUAL
# =========================

plt.figure(figsize=(10,6))
plt.plot(lags1, c1, label="curl → div")
plt.plot(lags2, c2, label="div → curl")
plt.axvline(0, linestyle="--", color="black")

plt.legend()
plt.title("V22 Time Lag Coupling")

out = os.path.join(OUTPUT_DIR, "v22_time_lag.png")
plt.savefig(out, dpi=150)

print("Saved:", out)

print("\n--- RESULTS ---")
print("curl → div lag:", lags1[np.argmax(c1)])
print("div → curl lag:", lags2[np.argmax(c2)])
