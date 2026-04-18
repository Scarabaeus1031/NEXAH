import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA
from scipy.interpolate import splprep, splev

# =========================
# Setup
# =========================

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
# 4. Event Detection
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
# 5. Directional Transitions
# =========================

def detect_directional_transitions(traj):
    x = traj[:, 0]

    LR = []
    RL = []

    for i in range(len(x) - 1):
        if x[i] < 0 and x[i+1] > 0:
            LR.append(i)
        elif x[i] > 0 and x[i+1] < 0:
            RL.append(i)

    return np.array(LR), np.array(RL)


# =========================
# 6. PCA Manifold (linear)
# =========================

def extract_pca_manifold(traj, transition_indices):
    points = traj[transition_indices]

    pca = PCA(n_components=1)
    pca.fit(points)

    direction = pca.components_[0]
    center = np.mean(points, axis=0)

    t = np.linspace(-20, 20, 100)
    line = center + np.outer(t, direction)

    return points, line, center


# =========================
# 7. Nonlinear Manifold (V8)
# =========================

def extract_nonlinear_manifold(traj, transition_indices):
    points = traj[transition_indices]

    # sortiert entlang Zeit
    order = np.argsort(transition_indices)
    points = points[order]

    x, y, z = points[:,0], points[:,1], points[:,2]

    # Spline Fit
    tck, u = splprep([x, y, z], s=5)

    u_fine = np.linspace(0, 1, 200)
    x_f, y_f, z_f = splev(u_fine, tck)

    curve = np.vstack([x_f, y_f, z_f]).T

    return points, curve


# =========================
# MAIN
# =========================

def main():
    print("Running Discovery Core V8...")

    traj = simulate()
    risk = compute_metrics(traj, dt=0.01)

    events = detect_events(risk)
    LR, RL = detect_directional_transitions(traj)

    transitions = np.concatenate([LR, RL])

    print(f"Events: {len(events)}")
    print(f"L→R: {len(LR)} | R→L: {len(RL)}")

    # PCA
    points, line, center = extract_pca_manifold(traj, transitions)

    # Nonlinear
    points_nl, curve = extract_nonlinear_manifold(traj, transitions)

    # =========================
    # Plot
    # =========================

    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Trajectory
    ax.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.3)

    # Events
    ax.scatter(traj[events,0], traj[events,1], traj[events,2],
               color='red', s=20, label="Events")

    # Transitions
    ax.scatter(traj[LR,0], traj[LR,1], traj[LR,2],
               color='green', s=40, label="L→R")

    ax.scatter(traj[RL,0], traj[RL,1], traj[RL,2],
               color='purple', s=40, label="R→L")

    # PCA Line
    ax.plot(line[:,0], line[:,1], line[:,2],
            color='black', linewidth=2, label="PCA Axis")

    # Nonlinear Curve
    ax.plot(curve[:,0], curve[:,1], curve[:,2],
            color='orange', linewidth=3, label="Nonlinear Manifold")

    # Center
    ax.scatter(center[0], center[1], center[2],
               color='yellow', s=80, label="Center")

    ax.set_title("V8: Linear + Nonlinear Transition Manifold")
    ax.legend()

    plt.tight_layout()

    # Save
    plt.savefig(f"{OUTPUT_DIR}/lorenz_v8_manifold.png", dpi=200)

    np.save(f"{OUTPUT_DIR}/transitions_v8.npy", transitions)
    np.save(f"{OUTPUT_DIR}/risk_v8.npy", risk)

    plt.show()


if __name__ == "__main__":
    main()
