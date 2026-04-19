import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# ========== CONFIG ==========
OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lorenz params
sigma = 10
rho = 28
beta = 8/3
dt = 0.01
steps = 5000

# ========== LORENZ ==========
def lorenz_step(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

def simulate():
    xs, ys, zs = [], [], []
    x, y, z = 1.0, 1.0, 1.0

    for _ in range(steps):
        dx, dy, dz = lorenz_step(x, y, z)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        xs.append(x)
        ys.append(y)
        zs.append(z)

    return np.array(xs), np.array(ys), np.array(zs)

# ========== RISK ==========
def compute_risk(xs, ys, zs):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    dz = np.gradient(zs)

    velocity = np.sqrt(dx**2 + dy**2 + dz**2)

    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    ddz = np.gradient(dz)

    curvature = np.sqrt(ddx**2 + ddy**2 + ddz**2)

    risk = velocity * curvature
    return risk

# ========== EVENT DETECTION ==========
def detect_events(risk, threshold_factor=2.0):
    threshold = np.mean(risk) * threshold_factor
    events = np.where(risk > threshold)[0]
    return events

# ========== PCA AXIS ==========
def compute_pca_axis(points):
    center = np.mean(points, axis=0)
    centered = points - center
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eig(cov)
    axis = eigvecs[:, np.argmax(eigvals)]
    return center, axis

# ========== DISTANCE TO AXIS ==========
def point_line_distance(points, center, axis):
    axis = axis / np.linalg.norm(axis)
    diff = points - center
    proj = np.dot(diff, axis)[:, None] * axis
    perp = diff - proj
    dist = np.linalg.norm(perp, axis=1)
    return dist

# ========== PROBABILITY FIELD ==========
def compute_density(points, radius=2.5):
    # distance matrix
    D = cdist(points, points)
    density = (D < radius).sum(axis=1)
    return density

# ========== MAIN ==========
def main():
    print("Running Discovery Core V16 (Probability Field)...")

    xs, ys, zs = simulate()
    risk = compute_risk(xs, ys, zs)
    events_idx = detect_events(risk)

    event_points = np.stack([
        xs[events_idx],
        ys[events_idx],
        zs[events_idx]
    ], axis=1)

    # PCA axis
    center, axis = compute_pca_axis(event_points)

    # distance to axis
    distances = point_line_distance(event_points, center, axis)

    # density (HOT ZONES)
    density = compute_density(event_points)

    # normalize to probability
    prob = density / np.max(density)

    # ========== PLOT ==========
    fig = plt.figure(figsize=(14, 10))

    # --- 3D PLOT ---
    ax = fig.add_subplot(221, projection='3d')
    ax.plot(xs, ys, zs, color='lightblue', alpha=0.3)

    sc = ax.scatter(
        event_points[:,0],
        event_points[:,1],
        event_points[:,2],
        c=prob,
        cmap='hot',
        s=60
    )

    # axis line
    line = np.linspace(-20, 20, 100)
    ax.plot(
        center[0] + axis[0]*line,
        center[1] + axis[1]*line,
        center[2] + axis[2]*line,
        color='black', linewidth=2
    )

    ax.scatter(*center, color='yellow', s=120)

    ax.set_title("3D Probability Field (Hot Zones)")

    # --- DENSITY HIST ---
    ax2 = fig.add_subplot(222)
    ax2.hist(density, bins=10)
    ax2.set_title("Event Density Distribution")

    # --- PROB OVER EVENTS ---
    ax3 = fig.add_subplot(223)
    ax3.plot(prob, marker='o')
    ax3.set_title("Transition Probability per Event")

    # --- DISTANCE VS PROB ---
    ax4 = fig.add_subplot(224)
    ax4.scatter(distances, prob)
    ax4.set_xlabel("Distance to Axis")
    ax4.set_ylabel("Probability")
    ax4.set_title("Distance vs Transition Probability")

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "v16_probability_field.png")
    plt.savefig(path, dpi=150)
    plt.close()

    print(f"Events: {len(events_idx)}")
    print("Saved:", path)


if __name__ == "__main__":
    main()
