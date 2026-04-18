import numpy as np
import matplotlib.pyplot as plt
import os

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

    return flow, curvature, risk


# =========================
# 4. Event Detection (clean peaks)
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

    transitions_LR = []
    transitions_RL = []

    for i in range(len(x) - 1):
        if x[i] < 0 and x[i+1] > 0:
            transitions_LR.append(i)

        if x[i] > 0 and x[i+1] < 0:
            transitions_RL.append(i)

    return np.array(transitions_LR), np.array(transitions_RL)


# =========================
# 6. Main
# =========================

def main():
    print("Running Discovery Core V6...")

    traj = simulate()
    flow, curvature, risk = compute_metrics(traj, dt=0.01)

    events = detect_events(risk)
    trans_LR, trans_RL = detect_directional_transitions(traj)

    print(f"Detected {len(events)} high-risk events")
    print(f"L → R transitions: {len(trans_LR)}")
    print(f"R → L transitions: {len(trans_RL)}")

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(14, 6))

    # --- 3D Trajectory ---
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.5)

    # Events
    ax1.scatter(traj[events,0], traj[events,1], traj[events,2],
                color='red', s=20, label="Events")

    # Transitions L → R
    ax1.scatter(traj[trans_LR,0], traj[trans_LR,1], traj[trans_LR,2],
                color='green', s=40, label="L → R")

    # Transitions R → L
    ax1.scatter(traj[trans_RL,0], traj[trans_RL,1], traj[trans_RL,2],
                color='purple', s=40, label="R → L")

    ax1.set_title("Lorenz Trajectory + Directional Transitions")
    ax1.legend()

    # --- Risk Signal ---
    ax2 = fig.add_subplot(122)
    ax2.plot(risk, label="Risk")

    ax2.scatter(events, risk[events], color='red', s=20)

    ax2.scatter(trans_LR, risk[trans_LR], color='green', label="L→R")
    ax2.scatter(trans_RL, risk[trans_RL], color='purple', label="R→L")

    ax2.set_title("Risk + Transition Directions")
    ax2.legend()

    plt.tight_layout()

    # Save
    plt.savefig(f"{OUTPUT_DIR}/lorenz_v6_transitions.png", dpi=200)
    np.save(f"{OUTPUT_DIR}/risk_v6.npy", risk)

    plt.show()


if __name__ == "__main__":
    main()
