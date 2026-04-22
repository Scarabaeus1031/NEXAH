import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

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

RISK_FACTOR = 2.0
DENSITY_RADIUS = 2.5
EPS = 1e-8

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
# FEATURES
# =========================

def compute_risk(xs, ys, zs):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    dz = np.gradient(zs)

    flow = np.sqrt(dx**2 + dy**2 + dz**2)
    curvature = np.sqrt(np.gradient(dx)**2 + np.gradient(dy)**2 + np.gradient(dz)**2)

    return flow * curvature * RISK_FACTOR

def detect_events(risk):
    threshold = np.mean(risk) + 2 * np.std(risk)
    return np.where(risk > threshold)[0]

# =========================
# PCA CHANNEL
# =========================

def compute_channel_axis(points):
    pca = PCA(n_components=1)
    pca.fit(points)
    center = np.mean(points, axis=0)
    axis = pca.components_[0]
    return center, axis

def distance_to_axis(points, center, axis):
    proj = np.dot(points - center, axis)
    proj_points = np.outer(proj, axis) + center
    return np.linalg.norm(points - proj_points, axis=1)

# =========================
# DENSITY FIELD
# =========================

def compute_density(points):
    D = cdist(points, points)
    return (D < DENSITY_RADIUS).sum(axis=1)

# =========================
# NORMALIZATION
# =========================

def norm(x):
    x = np.asarray(x)
    return (x - x.min()) / (x.max() - x.min() + EPS)

# =========================
# V19 CORE: ENERGY FIELD
# =========================

def compute_probability(risk, dist, density):
    r = norm(risk)
    d = 1.0 - norm(dist)      # closer to axis = higher
    dens = norm(density)

    # weighted mixture
    return 0.4*r + 0.3*d + 0.3*dens

def compute_energy(prob):
    # Boltzmann-style: E = -log(P)
    return -np.log(prob + EPS)

def compute_gradient(signal):
    return np.gradient(signal)

# =========================
# MAIN
# =========================

def main():
    print("Running Discovery Core V19 (Energy Field)...")

    xs, ys, zs = simulate()
    points = np.stack([xs, ys, zs], axis=1)

    risk = compute_risk(xs, ys, zs)
    events = detect_events(risk)

    center, axis = compute_channel_axis(points)
    dist = distance_to_axis(points, center, axis)

    density = compute_density(points)

    prob = compute_probability(risk, dist, density)
    energy = compute_energy(prob)

    grad = compute_gradient(energy)

    # =========================
    # VISUALS
    # =========================

    fig = plt.figure(figsize=(16, 10))

    # 3D ENERGY FIELD
    ax1 = fig.add_subplot(221, projection='3d')
    sc = ax1.scatter(xs, ys, zs, c=energy, cmap='plasma', s=5)

    ax1.scatter(xs[events], ys[events], zs[events], color='black', s=40)

    t = np.linspace(-30, 30, 100)
    line = center + np.outer(t, axis)
    ax1.plot(line[:,0], line[:,1], line[:,2], color='white')

    ax1.scatter(*center, color='yellow', s=100)
    ax1.set_title("V19: Energy Landscape (Boltzmann)")

    # ENERGY SIGNAL
    ax2 = fig.add_subplot(222)
    ax2.plot(energy)
    ax2.set_title("Energy over Time")

    # GRADIENT
    ax3 = fig.add_subplot(223)
    ax3.plot(grad)
    ax3.set_title("Energy Gradient (Transition Pressure)")

    # DISTANCE vs ENERGY
    ax4 = fig.add_subplot(224)
    ax4.scatter(dist, energy, s=5, alpha=0.5)
    ax4.set_xlabel("Distance to Axis")
    ax4.set_ylabel("Energy")
    ax4.set_title("Distance vs Energy")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "v19_energy_field.png"), dpi=300)
    plt.close()

    print(f"Events: {len(events)}")
    print("Saved: v19_energy_field.png")

if __name__ == "__main__":
    main()
