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
# 3. Field + Signal
# =========================

def compute_metrics(traj, dt):
    # velocity (dx/dt)
    v = np.gradient(traj, axis=0) / dt

    # acceleration (d2x/dt2)
    a = np.gradient(v, axis=0) / dt

    # flow strength
    flow = np.linalg.norm(v, axis=1)

    # curvature (proxy)
    curvature = np.linalg.norm(a, axis=1)

    # risk signal
    risk = flow * curvature

    return flow, curvature, risk


# =========================
# 4. Transition Detection
# =========================

def detect_peaks(signal, threshold_factor=2.0):
    threshold = np.mean(signal) * threshold_factor
    peaks = np.where(signal > threshold)[0]
    return peaks


# =========================
# 5. Main Runner
# =========================

def main():
    print("Running Discovery Core V2...")

    traj = simulate()
    flow, curvature, risk = compute_metrics(traj, dt=0.01)
    peaks = detect_peaks(risk)

    print(f"Detected {len(peaks)} high-risk transition points")

    # =========================
    # 6. Visualization
    # =========================

    fig = plt.figure(figsize=(12, 6))

    # Trajectory
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.6)

    # mark transitions
    ax1.scatter(traj[peaks,0], traj[peaks,1], traj[peaks,2],
                color='red', s=5, label="Transitions")

    ax1.set_title("Lorenz Trajectory + Transitions")
    ax1.legend()

    # Risk signal
    ax2 = fig.add_subplot(122)
    ax2.plot(risk, label="Risk Signal")

    ax2.scatter(peaks, risk[peaks], color='red', s=10)

    ax2.set_title("Risk Signal (flow × curvature)")
    ax2.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
