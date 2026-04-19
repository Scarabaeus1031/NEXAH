import os
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. Lorenz System
# =========================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])


# =========================
# 2. Simulation
# =========================

def simulate(n_steps=5000, dt=0.01):
    traj = np.zeros((n_steps, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    for i in range(n_steps - 1):
        traj[i+1] = traj[i] + dt * lorenz(*traj[i])

    return traj


# =========================
# 3. Metrics
# =========================

def compute_metrics(traj, dt):
    v = np.gradient(traj, axis=0) / dt
    a = np.gradient(v, axis=0) / dt

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)

    risk = flow * curvature
    return risk


# =========================
# 4. Event Detection (clean)
# =========================

def detect_events(signal, factor=2.5):
    threshold = np.mean(signal) * factor
    candidates = np.where(signal > threshold)[0]

    events = []
    last = -10

    for i in candidates:
        if i - last > 20:   # cluster suppression
            events.append(i)
            last = i

    return np.array(events)


# =========================
# 5. PCA Axis (Channel)
# =========================

def compute_pca_axis(points):
    center = np.mean(points, axis=0)
    centered = points - center

    U, S, Vt = np.linalg.svd(centered)
    axis = Vt[0]  # first principal component

    return center, axis


# =========================
# 6. Projection onto Channel
# =========================

def project_to_axis(points, center, axis):
    projections = np.dot(points - center, axis)
    return projections


# =========================
# 7. Main
# =========================

def main():
    print("Running Discovery Core V14 (Channel Navigation)...")

    os.makedirs("DISCOVERY_ENGINE/outputs", exist_ok=True)

    # simulate
    traj = simulate()
    risk = compute_metrics(traj, dt=0.01)

    # detect events
    events = detect_events(risk)
    event_points = traj[events]

    print(f"Events: {len(events)}")

    # PCA channel
    center, axis = compute_pca_axis(event_points)

    # projection
    proj = project_to_axis(event_points, center, axis)

    # sort events along channel
    order = np.argsort(proj)
    proj_sorted = proj[order]
    events_sorted = events[order]
    points_sorted = event_points[order]

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(12, 6))

    # --- 3D plot ---
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.3)

    # events
    ax1.scatter(event_points[:,0], event_points[:,1], event_points[:,2],
                color='red', s=40, label='Events')

    # channel axis
    t = np.linspace(-20, 20, 100)
    line = center + np.outer(t, axis)
    ax1.plot(line[:,0], line[:,1], line[:,2],
             color='black', linewidth=2, label='Channel Axis')

    # center
    ax1.scatter(*center, color='yellow', s=120, label='Center')

    ax1.set_title("3D Channel Structure")
    ax1.legend()

    # --- 1D channel dynamics ---
    ax2 = fig.add_subplot(122)

    ax2.plot(proj_sorted, marker='o')
    ax2.set_title("Event Sequence along Channel")
    ax2.set_xlabel("Ordered Event Index")
    ax2.set_ylabel("Projection (Channel Coordinate)")

    plt.tight_layout()

    # save
    out_path = "DISCOVERY_ENGINE/outputs/v14_channel_navigation.png"
    plt.savefig(out_path, dpi=200)
    plt.close()

    print("Saved:", out_path)


# =========================
# Run
# =========================

if __name__ == "__main__":
    main()
