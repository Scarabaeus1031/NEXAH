import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# CONFIG
# =========================

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_LOBE = 1   # 1 = right, 0 = left
CONTROL_STRENGTH = 2.0


# =========================
# 1. Lorenz System
# =========================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])


# =========================
# 2. Simulation with control
# =========================

def simulate_controlled(n_steps=5000, dt=0.01):
    traj = np.zeros((n_steps, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    control_flags = []

    for i in range(n_steps - 1):
        x, y, z = traj[i]

        dx, dy, dz = lorenz(x, y, z)

        # ===== CONTROL LOGIC =====
        current_lobe = 1 if x > 0 else 0

        control = 0.0

        if current_lobe != TARGET_LOBE:
            # push towards target side
            direction = 1 if TARGET_LOBE == 1 else -1
            control = CONTROL_STRENGTH * direction
            dx += control

        control_flags.append(control)

        traj[i+1] = traj[i] + dt * np.array([dx, dy, dz])

    return traj, np.array(control_flags)


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
# 4. Event detection
# =========================

def detect_events(signal, factor=2.5):
    threshold = np.mean(signal) * factor
    peaks = np.where(signal > threshold)[0]

    events = []
    if len(peaks) == 0:
        return np.array(events)

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
# 5. Main
# =========================

def main():
    print("Running Discovery Core V10 (Control)...")

    traj, control = simulate_controlled()
    risk = compute_metrics(traj, dt=0.01)

    events = detect_events(risk)

    # success measure
    final_lobe = np.sign(traj[-1, 0])
    success = (final_lobe > 0 and TARGET_LOBE == 1) or (final_lobe < 0 and TARGET_LOBE == 0)

    print(f"Events: {len(events)}")
    print(f"Control success: {success}")

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(12,6))

    # trajectory
    ax = fig.add_subplot(121, projection='3d')
    ax.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.3)

    ax.scatter(traj[events,0], traj[events,1], traj[events,2],
               color='red', s=40, label="Events")

    ax.set_title("Controlled Lorenz Trajectory")
    ax.legend()

    # control signal
    ax2 = fig.add_subplot(122)
    ax2.plot(control, label="Control Signal")
    ax2.set_title("Control Injection")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/v10_control.png", dpi=200)
    plt.show()

    print("Saved V10 output")


# =========================

if __name__ == "__main__":
    main()
