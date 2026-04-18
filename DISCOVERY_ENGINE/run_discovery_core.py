import numpy as np
import matplotlib.pyplot as plt
import os

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
    v = np.gradient(traj, axis=0) / dt
    a = np.gradient(v, axis=0) / dt

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)

    risk = flow * curvature

    return flow, curvature, risk


# =========================
# 4. EVENT DETECTION (NEW)
# =========================

def detect_events(signal, threshold_factor=2.0):
    threshold = np.mean(signal) * threshold_factor

    above = signal > threshold

    events = []
    current = []

    for i, val in enumerate(above):
        if val:
            current.append(i)
        else:
            if current:
                events.append(current)
                current = []

    if current:
        events.append(current)

    return events


# =========================
# 5. Main Runner
# =========================

def main():
    print("Running Discovery Core V3...")

    # ensure output folder exists
    output_dir = "DISCOVERY_ENGINE/outputs"
    os.makedirs(output_dir, exist_ok=True)

    run_id = "run_001"

    traj = simulate()
    flow, curvature, risk = compute_metrics(traj, dt=0.01)

    events = detect_events(risk)

    # event centers (for plotting)
    centers = [int(np.mean(e)) for e in events]

    print(f"Detected {len(events)} transition events")

    # =========================
    # 6. Visualization
    # =========================

    fig = plt.figure(figsize=(12, 6))

    # Trajectory
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.6)

    ax1.scatter(
        traj[centers,0],
        traj[centers,1],
        traj[centers,2],
        color='red',
        s=20,
        label="Events"
    )

    ax1.set_title("Lorenz Trajectory + Events")
    ax1.legend()

    # Risk signal
    ax2 = fig.add_subplot(122)
    ax2.plot(risk, label="Risk Signal")

    ax2.scatter(centers, risk[centers], color='red', s=20)

    ax2.set_title("Risk Signal (flow × curvature)")
    ax2.legend()

    plt.tight_layout()

    # =========================
    # 7. Save outputs
    # =========================

    plt.savefig(f"{output_dir}/lorenz_{run_id}.png", dpi=200)
    np.save(f"{output_dir}/risk_{run_id}.npy", risk)
    np.save(f"{output_dir}/events_{run_id}.npy", centers)

    print(f"Saved outputs to {output_dir}")

    plt.show()


if __name__ == "__main__":
    main()
