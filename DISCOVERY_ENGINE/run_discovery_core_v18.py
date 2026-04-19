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
PRE_WINDOW = 40

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
# FEATURE EXTRACTION
# =========================

def compute_risk(xs, ys, zs):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    dz = np.gradient(zs)

    curvature = np.sqrt(np.gradient(dx)**2 + np.gradient(dy)**2 + np.gradient(dz)**2)
    flow = np.sqrt(dx**2 + dy**2 + dz**2)

    return flow * curvature * RISK_FACTOR

def detect_events(risk):
    threshold = np.mean(risk) + 2 * np.std(risk)
    return np.where(risk > threshold)[0]

# =========================
# PCA CHANNEL AXIS
# =========================

def compute_channel_axis(xs, ys, zs):
    data = np.stack([xs, ys, zs], axis=1)
    pca = PCA(n_components=1)
    pca.fit(data)

    center = np.mean(data, axis=0)
    axis = pca.components_[0]

    return center, axis

def project_to_axis(points, center, axis):
    return np.dot(points - center, axis)

def distance_to_axis(points, center, axis):
    proj = project_to_axis(points, center, axis)
    proj_points = np.outer(proj, axis) + center
    return np.linalg.norm(points - proj_points, axis=1)

# =========================
# V18 CORE: ECHO + PROB FIELD
# =========================

def compute_echo_field(events, total_steps):
    echo = np.zeros(total_steps)

    for e in events:
        start = max(0, e - PRE_WINDOW)
        echo[start:e] += np.linspace(0, 1, e - start)

    return echo

def compute_probability_field(distance, risk):
    # normalize
    d_norm = (distance - np.min(distance)) / (np.max(distance) - np.min(distance) + 1e-8)
    r_norm = (risk - np.min(risk)) / (np.max(risk) - np.min(risk) + 1e-8)

    # probability model
    prob = np.exp(-2 * d_norm) * r_norm

    return prob

def compute_gradient(signal):
    return np.gradient(signal)

# =========================
# MAIN
# =========================

def main():
    print("Running Discovery Core V18...")

    xs, ys, zs = simulate()
    risk = compute_risk(xs, ys, zs)
    events = detect_events(risk)

    points = np.stack([xs, ys, zs], axis=1)

    center, axis = compute_channel_axis(xs, ys, zs)
    dist = distance_to_axis(points, center, axis)

    # NEW V18
    echo = compute_echo_field(events, steps)
    prob = compute_probability_field(dist, risk)
    grad = compute_gradient(prob)

    # =========================
    # VISUALIZATION
    # =========================

    fig = plt.figure(figsize=(16, 10))

    # 3D FIELD
    ax1 = fig.add_subplot(221, projection='3d')
    sc = ax1.scatter(xs, ys, zs, c=prob, cmap='inferno', s=5)

    ax1.scatter(xs[events], ys[events], zs[events], color='black', s=40)

    # axis line
    t = np.linspace(-30, 30, 100)
    line = center + np.outer(t, axis)
    ax1.plot(line[:,0], line[:,1], line[:,2], color='white', linewidth=2)

    ax1.scatter(*center, color='yellow', s=100)

    ax1.set_title("V18: 3D Probability + Channel")

    # ECHO + PROB
    ax2 = fig.add_subplot(222)
    ax2.plot(prob, label='probability')
    ax2.plot(echo, label='echo (pre-transition)', alpha=0.7)
    ax2.set_title("Probability + Echo Memory")
    ax2.legend()

    # GRADIENT
    ax3 = fig.add_subplot(223)
    ax3.plot(grad)
    ax3.set_title("Probability Gradient (Flow Direction)")

    # DISTANCE vs PROB
    ax4 = fig.add_subplot(224)
    ax4.scatter(dist, prob, s=5, alpha=0.5)
    ax4.set_xlabel("Distance to Axis")
    ax4.set_ylabel("Probability")
    ax4.set_title("Distance vs Probability Field")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "v18_probability_field.png"), dpi=300)
    plt.close()

    print(f"Events: {len(events)}")
    print("Saved: v18_probability_field.png")

if __name__ == "__main__":
    main()
