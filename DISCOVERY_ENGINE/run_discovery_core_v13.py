import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DT = 0.01
N_STEPS = 5000


# =========================
# Lorenz System
# =========================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])


def simulate():
    traj = np.zeros((N_STEPS, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    for i in range(N_STEPS - 1):
        traj[i+1] = traj[i] + DT * lorenz(*traj[i])

    return traj


# =========================
# Metrics
# =========================

def compute_metrics(traj):
    v = np.gradient(traj, axis=0) / DT
    a = np.gradient(v, axis=0) / DT

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)

    risk = flow * curvature
    return risk


def detect_events(signal, factor=2.5):
    threshold = np.mean(signal) * factor
    peaks = np.where(signal > threshold)[0]

    if len(peaks) == 0:
        return np.array([])

    events = []
    cluster = [peaks[0]]

    for i in range(1, len(peaks)):
        if peaks[i] - peaks[i-1] < 10:
            cluster.append(peaks[i])
        else:
            events.append(int(np.mean(cluster)))
            cluster = [peaks[i]]

    events.append(int(np.mean(cluster)))
    return np.array(events)


# =========================
# 🔥 LOBE ALIGNMENT (V13)
# =========================

def align_lobes(points):
    aligned = points.copy()

    # einfache Spiegelung der rechten Lobe
    mask = aligned[:, 0] > 0

    aligned[mask, 0] *= -1  # Spiegelung an YZ-Ebene

    return aligned


# =========================
# Geometry
# =========================

def extract_axis(points):
    pca = PCA(n_components=1)
    pca.fit(points)

    axis = pca.components_[0]
    axis /= np.linalg.norm(axis)

    center = np.mean(points, axis=0)

    return axis, center


def distance_to_axis(points, axis, center):
    diffs = points - center
    proj = np.dot(diffs, axis)

    proj_points = np.outer(proj, axis) + center
    dist = np.linalg.norm(points - proj_points, axis=1)

    return dist


# =========================
# Main
# =========================

def main():
    print("Running Discovery Core V13 (Lobe Alignment)...")

    traj = simulate()
    risk = compute_metrics(traj)

    events = detect_events(risk)

    event_points = traj[events]

    # 🔥 Alignment Schritt
    aligned_events = align_lobes(event_points)

    # PCA auf aligned space
    axis, center = extract_axis(aligned_events)

    # Distances
    event_dist = distance_to_axis(aligned_events, axis, center)

    # Metrics
    channel_width = np.std(event_dist)
    mean_dist = np.mean(event_dist)

    print("\n--- METRICS ---")
    print(f"Events: {len(events)}")
    print(f"Aligned channel width: {channel_width:.4f}")
    print(f"Mean distance to axis: {mean_dist:.4f}")

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(14, 6))

    # Original space
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.2)

    ax1.scatter(event_points[:,0], event_points[:,1], event_points[:,2],
                color='red', s=30, label="Original Events")

    ax1.set_title("Original Space")

    # Aligned space
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(aligned_events[:,0], aligned_events[:,1], aligned_events[:,2],
                color='green', s=30, label="Aligned Events")

    # PCA axis
    t = np.linspace(-20, 20, 100)
    axis_line = center + np.outer(t, axis)

    ax2.plot(axis_line[:,0], axis_line[:,1], axis_line[:,2],
             color='black', linewidth=2)

    ax2.scatter(center[0], center[1], center[2],
                color='yellow', s=80, label="Center")

    ax2.set_title("Aligned Space + Unified Axis")

    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/v13_aligned.png", dpi=200)
    plt.show()

    print("\nSaved V13 output")


if __name__ == "__main__":
    main()
