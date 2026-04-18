import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# Lorenz System
# =========================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])


def simulate(n_steps=5000, dt=0.01):
    traj = np.zeros((n_steps, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    for i in range(n_steps - 1):
        traj[i+1] = traj[i] + dt * lorenz(*traj[i])

    return traj


# =========================
# Metrics
# =========================

def compute_metrics(traj, dt):
    v = np.gradient(traj, axis=0) / dt
    a = np.gradient(v, axis=0) / dt

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)

    risk = flow * curvature

    return risk


# =========================
# Event Detection
# =========================

def detect_events(signal, threshold_factor=2.5, min_distance=50):
    threshold = np.mean(signal) * threshold_factor
    peaks = np.where(signal > threshold)[0]

    filtered = []
    last = -min_distance

    for p in peaks:
        if p - last > min_distance:
            filtered.append(p)
            last = p

    return np.array(filtered)


# =========================
# Directional Transitions
# =========================

def detect_transitions(traj):
    x = traj[:, 0]

    transitions = []

    for i in range(len(x) - 1):
        if (x[i] < 0 and x[i+1] > 0) or (x[i] > 0 and x[i+1] < 0):
            transitions.append(i)

    return np.array(transitions)


# =========================
# V7: Manifold Extraction
# =========================

def extract_manifold(traj, transition_indices):
    points = traj[transition_indices]

    pca = PCA(n_components=1)
    pca.fit(points)

    direction = pca.components_[0]
    center = np.mean(points, axis=0)

    # Linie erzeugen
    t = np.linspace(-20, 20, 100)
    line = center + np.outer(t, direction)

    return points, line, center, direction


# =========================
# MAIN
# =========================

def main():
    print("Running Discovery Core V7...")

    traj = simulate()
    risk = compute_metrics(traj, dt=0.01)

    events = detect_events(risk)
    transitions = detect_transitions(traj)

    print(f"Events: {len(events)}")
    print(f"Transitions: {len(transitions)}")

    # Manifold
    points, line, center, direction = extract_manifold(traj, transitions)

    # =========================
    # Plot
    # =========================

    fig = plt.figure(figsize=(14, 6))

    ax = fig.add_subplot(111, projection='3d')

    # Trajectory
    ax.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.3)

    # Events
    ax.scatter(traj[events,0], traj[events,1], traj[events,2],
               color='red', s=20, label="Events")

    # Transition points
    ax.scatter(points[:,0], points[:,1], points[:,2],
               color='green', s=40, label="Transitions")

    # Manifold line
    ax.plot(line[:,0], line[:,1], line[:,2],
            color='black', linewidth=3, label="Manifold")

    # Center point
    ax.scatter(center[0], center[1], center[2],
               color='yellow', s=80, label="Center")

    ax.set_title("V7: Transition Manifold Extraction")
    ax.legend()

    plt.tight_layout()

    # Save
    plt.savefig(f"{OUTPUT_DIR}/lorenz_v7_manifold.png", dpi=200)

    plt.show()


if __name__ == "__main__":
    main()
