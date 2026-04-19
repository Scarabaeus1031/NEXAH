import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

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
DENSITY_RADIUS = 2.5

# =========================
# LORENZ
# =========================

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

# =========================
# RISK
# =========================

def compute_risk(xs, ys, zs):
    dx = np.gradient(xs)
    dy = np.gradient(ys)
    dz = np.gradient(zs)

    velocity = np.sqrt(dx**2 + dy**2 + dz**2)

    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    ddz = np.gradient(dz)

    curvature = np.sqrt(ddx**2 + ddy**2 + ddz**2)

    return velocity * curvature

# =========================
# EVENTS
# =========================

def detect_events(risk):
    threshold = np.mean(risk) * RISK_FACTOR
    raw = np.where(risk > threshold)[0]

    events = []
    last = -50

    for i in raw:
        if i - last > 20:
            events.append(i)
            last = i

    return np.array(events)

# =========================
# PCA AXIS
# =========================

def compute_pca_axis(points):
    center = np.mean(points, axis=0)
    centered = points - center
    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eig(cov)
    axis = eigvecs[:, np.argmax(eigvals)]
    axis = axis / np.linalg.norm(axis)
    return center, axis

def point_line_distance(points, center, axis):
    diff = points - center
    proj = np.dot(diff, axis)[:, None] * axis
    perp = diff - proj
    return np.linalg.norm(perp, axis=1)

# =========================
# PROBABILITY FIELD
# =========================

def compute_density(points):
    D = cdist(points, points)
    return (D < DENSITY_RADIUS).sum(axis=1)

def map_probability(traj_points, event_points, event_prob):
    D = cdist(traj_points, event_points)
    nearest = np.argmin(D, axis=1)
    return event_prob[nearest]

# =========================
# PRE-TRANSITION LABELS
# =========================

def build_labels(events, n):
    labels = np.zeros(n)
    for e in events:
        start = max(0, e - PRE_WINDOW)
        labels[start:e] = 1
    return labels

# =========================
# NORMALIZE
# =========================

def norm(x):
    mn, mx = np.min(x), np.max(x)
    return (x - mn) / (mx - mn + 1e-12)

# =========================
# MAIN
# =========================

def main():
    print("Running V17...")

    xs, ys, zs = simulate()
    traj = np.stack([xs, ys, zs], axis=1)

    risk = compute_risk(xs, ys, zs)
    events = detect_events(risk)

    print("Events:", len(events))

    event_points = traj[events]

    center, axis = compute_pca_axis(event_points)
    dist = point_line_distance(traj, center, axis)

    density = compute_density(event_points)
    prob_events = density / np.max(density)

    prob_field = map_probability(traj, event_points, prob_events)

    labels = build_labels(events, len(xs))

    # WARNING SCORE
    score = (
        0.45 * norm(risk) +
        0.30 * (1 - norm(dist)) +
        0.25 * norm(prob_field)
    )

    prediction = (score > 0.65).astype(int)

    # =========================
    # PLOTS
    # =========================

    fig = plt.figure(figsize=(14,10))

    # 3D
    ax = fig.add_subplot(221, projection='3d')
    ax.plot(xs, ys, zs, alpha=0.2)

    sc = ax.scatter(
        event_points[:,0],
        event_points[:,1],
        event_points[:,2],
        c=prob_events,
        cmap='hot',
        s=60
    )

    t = np.linspace(-20,20,100)
    ax.plot(
        center[0] + axis[0]*t,
        center[1] + axis[1]*t,
        center[2] + axis[2]*t,
        color='black'
    )

    ax.scatter(*center, color='yellow', s=120)
    ax.set_title("3D Probability + Channel")

    # Warning signal
    ax2 = fig.add_subplot(222)
    ax2.plot(score, label='score')
    ax2.plot(labels, label='true')
    ax2.plot(prediction, label='pred')
    ax2.legend()
    ax2.set_title("Early Warning")

    # components
    ax3 = fig.add_subplot(223)
    ax3.plot(norm(risk), label='risk')
    ax3.plot(1-norm(dist), label='axis')
    ax3.plot(norm(prob_field), label='prob')
    ax3.legend()
    ax3.set_title("Components")

    # scatter
    ax4 = fig.add_subplot(224)
    ax4.scatter(dist, score, c=labels, s=8)
    ax4.set_title("Distance vs Score")

    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "v17_pretransition.png")
    plt.savefig(path, dpi=150)
    plt.close()

    print("Saved:", path)

if __name__ == "__main__":
    main()
