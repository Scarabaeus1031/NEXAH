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
# 4. Transition Detection (Peak-based)
# =========================

def detect_peaks(signal, threshold_factor=2.0, min_distance=50):
    threshold = np.mean(signal) * threshold_factor

    candidates = np.where(signal > threshold)[0]

    # simple peak thinning (distance filter)
    peaks = []
    last = -min_distance

    for idx in candidates:
        if idx - last >= min_distance:
            peaks.append(idx)
            last = idx

    return np.array(peaks)


# =========================
# 5. Main Runner
# =========================

def main():
    print("Running Discovery Core V4...")

    output_dir = "DISCOVERY_ENGINE/outputs"
    os.makedirs(output_dir, exist_ok=True)

    traj = simulate()
    flow, curvature, risk = compute_metrics(traj, dt=0.01)
    peaks = detect_peaks(risk)

    print(f"Detected {len(peaks)} transition events")

    # =========================
    # Split EVEN / ODD
    # =========================

    even_idx = peaks[::2]
    odd_idx = peaks[1::2]

    # =========================
    # Normalize for size scaling
    # =========================

    norm_risk = (risk - np.min(risk)) / (np.max(risk) - np.min(risk) + 1e-9)

    sizes_even = 20 + 100 * norm_risk[even_idx]
    sizes_odd = 20 + 100 * norm_risk[odd_idx]

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(12, 6))

    # 3D Trajectory
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.5)

    # EVEN events
    ax1.scatter(
        traj[even_idx,0],
        traj[even_idx,1],
        traj[even_idx,2],
        s=sizes_even,
        label="Even Events"
    )

    # ODD events
    ax1.scatter(
        traj[odd_idx,0],
        traj[odd_idx,1],
        traj[odd_idx,2],
        s=sizes_odd,
        label="Odd Events"
    )

    ax1.set_title("Lorenz Trajectory + Structured Events")
    ax1.legend()

    # Risk signal
    ax2 = fig.add_subplot(122)
    ax2.plot(risk, label="Risk Signal")

    ax2.scatter(even_idx, risk[even_idx], s=sizes_even)
    ax2.scatter(odd_idx, risk[odd_idx], s=sizes_odd)

    ax2.set_title("Risk Signal (flow × curvature)")
    ax2.legend()

    plt.tight_layout()

    # SAVE FIRST (wichtig!)
    plt.savefig(f"{output_dir}/lorenz_core_v4.png", dpi=200)

    # THEN SHOW
    plt.show()

    np.save(f"{output_dir}/risk_signal_v4.npy", risk)

    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()

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
