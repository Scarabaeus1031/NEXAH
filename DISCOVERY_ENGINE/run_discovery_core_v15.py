import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DT = 0.01
N_STEPS = 5000
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
# 2. Simulation
# =========================

def simulate(n_steps=N_STEPS, dt=DT):
    traj = np.zeros((n_steps, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    for i in range(n_steps - 1):
        traj[i+1] = traj[i] + dt * lorenz(*traj[i])

    return traj


# =========================
# 3. Metrics
# =========================

def compute_risk(traj, dt):
    v = np.gradient(traj, axis=0) / dt
    a = np.gradient(v, axis=0) / dt
    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)
    return flow * curvature


# =========================
# 4. Event Detection
# =========================

def detect_events(signal, factor=RISK_FACTOR):
    threshold = np.mean(signal) * factor
    peaks = np.where(signal > threshold)[0]

    events = []
    last = -20

    for i in peaks:
        if i - last > 20:
            events.append(i)
            last = i

    return np.array(events)


# =========================
# 5. PCA Channel
# =========================

def compute_pca_axis(points):
    center = np.mean(points, axis=0)
    centered = points - center
    U, S, Vt = np.linalg.svd(centered)
    axis = Vt[0]
    return center, axis


def project(traj, center, axis):
    return np.dot(traj - center, axis)


# =========================
# 6. State Machine
# =========================

def classify_states(proj, low=-10, high=10):
    states = np.zeros(len(proj))

    for i, p in enumerate(proj):
        if p < low:
            states[i] = -1   # LEFT
        elif p > high:
            states[i] = 1    # RIGHT
        else:
            states[i] = 0    # TRANSITION

    return states


# =========================
# 7. Early Warning
# =========================

def compute_early_warning(proj, threshold=8):
    """
    Warning if we approach transition zone boundary
    """
    warning = np.zeros(len(proj))

    for i, p in enumerate(proj):
        if abs(p) < threshold:
            warning[i] = 1

    return warning


# =========================
# 8. Main
# =========================

def main():
    print("Running Discovery Core V15 (State Machine + Early Warning)...")

    traj = simulate()
    risk = compute_risk(traj, DT)

    events = detect_events(risk)
    event_points = traj[events]

    # Channel
    center, axis = compute_pca_axis(event_points)

    # Full trajectory projection
    proj = project(traj, center, axis)

    # States
    states = classify_states(proj)

    # Early warning
    warning = compute_early_warning(proj)

    print(f"Events: {len(events)}")

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(14, 8))

    # 3D plot
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.2)

    # color by state
    colors = ['blue' if s==-1 else 'red' if s==1 else 'orange' for s in states]

    ax1.scatter(traj[:,0], traj[:,1], traj[:,2],
                c=colors, s=1)

    ax1.scatter(event_points[:,0], event_points[:,1], event_points[:,2],
                color='black', s=40, label='Events')

    ax1.set_title("State Classification in 3D")
    ax1.legend()

    # Projection
    ax2 = fig.add_subplot(222)
    ax2.plot(proj, label='Projection')
    ax2.set_title("Channel Projection")

    # States timeline
    ax3 = fig.add_subplot(223)
    ax3.plot(states)
    ax3.set_title("State Timeline (-1 left, 0 transition, +1 right)")

    # Early warning
    ax4 = fig.add_subplot(224)
    ax4.plot(warning)
    ax4.set_title("Early Warning Signal")

    plt.tight_layout()

    out_path = f"{OUTPUT_DIR}/v15_state_machine.png"
    plt.savefig(out_path, dpi=200)
    plt.close()

    print("Saved:", out_path)


if __name__ == "__main__":
    main()
