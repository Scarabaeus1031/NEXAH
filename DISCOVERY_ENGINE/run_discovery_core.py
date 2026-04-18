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

    return flow, curvature, risk


# =========================
# 4. Event Detection
# =========================

def detect_peaks(signal, threshold_factor=2.0, min_distance=50):
    threshold = np.mean(signal) * threshold_factor

    candidates = np.where(signal > threshold)[0]

    peaks = []
    last = -min_distance

    for idx in candidates:
        if idx - last >= min_distance:
            peaks.append(idx)
            last = idx

    return np.array(peaks)


# =========================
# 5. PCA Axis (Key Step)
# =========================

def compute_axis(traj):
    mean = np.mean(traj, axis=0)
    centered = traj - mean

    cov = np.cov(centered.T)
    eigvals, eigvecs = np.linalg.eig(cov)

    axis = eigvecs[:, np.argmax(eigvals)]
    return axis, mean


# =========================
# 6. Main
# =========================

def main():
    print("Running Discovery Core V5...")

    output_dir = "DISCOVERY_ENGINE/outputs"
    os.makedirs(output_dir, exist_ok=True)

    traj = simulate()
    flow, curvature, risk = compute_metrics(traj, dt=0.01)
    peaks = detect_peaks(risk)

    print(f"Detected {len(peaks)} transition events")

    # =========================
    # Axis Projection
    # =========================

    axis, mean = compute_axis(traj)

    centered = traj - mean
    projection = centered @ axis

    # Lobe classification
    left = projection < 0
    right = projection >= 0

    # Event classification
    left_events = peaks[projection[peaks] < 0]
    right_events = peaks[projection[peaks] >= 0]

    # Normalize size
    norm_risk = (risk - np.min(risk)) / (np.max(risk) - np.min(risk) + 1e-9)
    sizes = 20 + 100 * norm_risk[peaks]

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(14, 6))

    # --- 3D Plot ---
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.4)

    ax1.scatter(
        traj[left_events,0],
        traj[left_events,1],
        traj[left_events,2],
        s=sizes[:len(left_events)],
        label="Left Lobe"
    )

    ax1.scatter(
        traj[right_events,0],
        traj[right_events,1],
        traj[right_events,2],
        s=sizes[len(left_events):],
        label="Right Lobe"
    )

    ax1.set_title("Lobe-based Event Classification")
    ax1.legend()

    # --- Projection Plot ---
    ax2 = fig.add_subplot(122)
    ax2.plot(projection, alpha=0.6, label="Projection")

    ax2.scatter(left_events, projection[left_events], label="Left Events")
    ax2.scatter(right_events, projection[right_events], label="Right Events")

    ax2.set_title("Axis Projection (Structure View)")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f"{output_dir}/lorenz_core_v5.png", dpi=200)
    plt.show()

    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
