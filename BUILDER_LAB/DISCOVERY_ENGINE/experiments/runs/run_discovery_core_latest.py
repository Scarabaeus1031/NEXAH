import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA

# =========================
# CONFIG
# =========================

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_LOBE = 1          # 1 = right, 0 = left
DT = 0.01
N_STEPS = 5000

CONTROL_GAIN = 0.8
CHANNEL_WIDTH = 8.0
RISK_FACTOR = 2.5


# =========================
# 1. Lorenz System
# =========================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])


# =========================
# 2. Baseline Simulation
# =========================

def simulate_baseline():
    traj = np.zeros((N_STEPS, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    for i in range(N_STEPS - 1):
        traj[i + 1] = traj[i] + DT * lorenz(*traj[i])

    return traj


# =========================
# 3. Metrics
# =========================

def compute_metrics(traj):
    v = np.gradient(traj, axis=0) / DT
    a = np.gradient(v, axis=0) / DT

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)
    risk = flow * curvature

    return flow, curvature, risk


# =========================
# 4. Event Detection
# =========================

def detect_events(signal):
    threshold = np.mean(signal) * RISK_FACTOR
    peaks = np.where(signal > threshold)[0]

    if len(peaks) == 0:
        return np.array([], dtype=int)

    events = []
    cluster = [peaks[0]]

    for i in range(1, len(peaks)):
        if peaks[i] - peaks[i - 1] < 10:
            cluster.append(peaks[i])
        else:
            events.append(int(np.mean(cluster)))
            cluster = [peaks[i]]

    events.append(int(np.mean(cluster)))
    return np.array(events, dtype=int)


# =========================
# 5. Transitions
# =========================

def detect_transitions(traj):
    x = traj[:, 0]

    lr = []
    rl = []

    for i in range(len(x) - 1):
        if x[i] < 0 and x[i + 1] > 0:
            lr.append(i)
        elif x[i] > 0 and x[i + 1] < 0:
            rl.append(i)

    return np.array(lr), np.array(rl)


# =========================
# 6. PCA Axis
# =========================

def extract_pca_axis(points):
    pca = PCA(n_components=1)
    pca.fit(points)

    axis = pca.components_[0]
    axis = axis / (np.linalg.norm(axis) + 1e-12)

    center = np.mean(points, axis=0)

    return axis, center


def project(point, axis, center):
    return np.dot(point - center, axis)


# =========================
# 7. V11 Control
# =========================

def simulate_control(axis, center):
    traj = np.zeros((N_STEPS, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    control_mag = np.zeros(N_STEPS)
    control_active = np.zeros(N_STEPS, dtype=bool)

    target_sign = 1 if TARGET_LOBE == 1 else -1

    for i in range(N_STEPS - 1):
        x = traj[i].copy()
        dx_nat = lorenz(*x)

        proj = project(x, axis, center)
        sign = 1 if x[0] >= 0 else -1

        u = np.zeros(3)

        if abs(proj) < CHANNEL_WIDTH and sign != target_sign:
            u = CONTROL_GAIN * axis * target_sign
            control_active[i] = True

        traj[i + 1] = x + DT * (dx_nat + u)
        control_mag[i] = np.linalg.norm(u)

    return traj, control_mag, control_active


# =========================
# MAIN
# =========================

def main():
    print("Running Discovery Core V11...")

    base_traj = simulate_baseline()
    _, _, base_risk = compute_metrics(base_traj)
    base_events = detect_events(base_risk)

    lr, rl = detect_transitions(base_traj)
    transitions = np.concatenate([lr, rl])
    transition_points = base_traj[transitions]

    axis, center = extract_pca_axis(transition_points)

    ctrl_traj, control_mag, control_active = simulate_control(axis, center)
    _, _, ctrl_risk = compute_metrics(ctrl_traj)
    ctrl_events = detect_events(ctrl_risk)

    print(f"Baseline events: {len(base_events)}")
    print(f"Controlled events: {len(ctrl_events)}")
    print(f"Control active steps: {np.sum(control_active)}")

    # Plot
    fig = plt.figure(figsize=(14, 10))

    # Baseline
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot(base_traj[:,0], base_traj[:,1], base_traj[:,2], alpha=0.3)
    ax1.scatter(base_traj[base_events,0], base_traj[base_events,1], base_traj[base_events,2], color='red')
    ax1.set_title("Baseline")

    # Controlled
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.plot(ctrl_traj[:,0], ctrl_traj[:,1], ctrl_traj[:,2], alpha=0.3)
    ax2.scatter(ctrl_traj[ctrl_events,0], ctrl_traj[ctrl_events,1], ctrl_traj[ctrl_events,2], color='red')
    ax2.scatter(ctrl_traj[control_active,0], ctrl_traj[control_active,1], ctrl_traj[control_active,2],
                color='orange', s=5)
    ax2.set_title("Controlled (Field-based)")

    # Risk
    ax3 = fig.add_subplot(223)
    ax3.plot(base_risk, label="Base")
    ax3.plot(ctrl_risk, label="Controlled")
    ax3.legend()

    # Control signal
    ax4 = fig.add_subplot(224)
    ax4.plot(control_mag)
    ax4.fill_between(range(len(control_mag)), 0, control_mag,
                     where=control_active, alpha=0.3)
    ax4.set_title("Control magnitude")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/v11.png", dpi=200)
    plt.show()

    print("Saved V11 output")


if __name__ == "__main__":
    main()
