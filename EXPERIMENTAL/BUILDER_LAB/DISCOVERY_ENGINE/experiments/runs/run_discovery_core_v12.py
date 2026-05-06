import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.decomposition import PCA

OUTPUT_DIR = "DISCOVERY_ENGINE/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DT = 0.01
N_STEPS = 5000


# =========================
# Lorenz
# =========================

def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])


def simulate():
    traj = np.zeros((N_STEPS, 3))
    traj[0] = np.array([1.0, 1.0, 1.0])

    for i in range(N_STEPS - 1):
        traj[i+1] = traj[i] + DT * lorenz(*traj[i])

    return traj


# =========================
# Metrics
# =========================

def compute_metrics(traj):
    v = np.gradient(traj, axis=0) / DT
    a = np.gradient(v, axis=0) / DT

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)

    risk = flow * curvature
    return risk


def detect_events(signal, factor=2.5):
    threshold = np.mean(signal) * factor
    peaks = np.where(signal > threshold)[0]

    if len(peaks) == 0:
        return np.array([])

    events = []
    cluster = [peaks[0]]

    for i in range(1, len(peaks)):
        if peaks[i] - peaks[i-1] < 10:
            cluster.append(peaks[i])
        else:
            events.append(int(np.mean(cluster)))
            cluster = [peaks[i]]

    events.append(int(np.mean(cluster)))
    return np.array(events)


def detect_transitions(traj):
    x = traj[:, 0]

    lr = []
    rl = []

    for i in range(len(x)-1):
        if x[i] < 0 and x[i+1] > 0:
            lr.append(i)
        elif x[i] > 0 and x[i+1] < 0:
            rl.append(i)

    return np.array(lr), np.array(rl)


# =========================
# Geometry
# =========================

def extract_axis(points):
    pca = PCA(n_components=1)
    pca.fit(points)

    axis = pca.components_[0]
    axis /= np.linalg.norm(axis)

    center = np.mean(points, axis=0)

    return axis, center


def distance_to_axis(points, axis, center):
    diffs = points - center
    proj = np.dot(diffs, axis)

    proj_points = np.outer(proj, axis) + center
    dist = np.linalg.norm(points - proj_points, axis=1)

    return dist


# =========================
# Main
# =========================

def main():
    print("Running Discovery Core V12 (Metrics)...")

    traj = simulate()
    risk = compute_metrics(traj)

    events = detect_events(risk)
    lr, rl = detect_transitions(traj)

    transitions = np.concatenate([lr, rl])
    transition_points = traj[transitions]

    axis, center = extract_axis(transition_points)

    # =========================
    # Measurements
    # =========================

    # distance of events to axis
    event_points = traj[events]
    event_dist = distance_to_axis(event_points, axis, center)

    # channel width
    channel_width = np.std(event_dist)

    # global deviation
    traj_dist = distance_to_axis(traj, axis, center)
    mean_deviation = np.mean(traj_dist)

    # event clustering
    event_density = len(events) / N_STEPS

    # =========================
    # Print Metrics
    # =========================

    print("\n--- METRICS ---")
    print(f"Events: {len(events)}")
    print(f"Transitions: {len(transitions)}")
    print(f"Channel width (std): {channel_width:.4f}")
    print(f"Mean trajectory deviation: {mean_deviation:.4f}")
    print(f"Event density: {event_density:.4f}")
    print(f"Mean risk: {np.mean(risk):.4f}")

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(14, 10))

    # 3D trajectory + axis
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.25)
    ax1.scatter(traj[events,0], traj[events,1], traj[events,2],
                color='red', s=20)

    t = np.linspace(-20, 20, 100)
    axis_line = center + np.outer(t, axis)

    ax1.plot(axis_line[:,0], axis_line[:,1], axis_line[:,2],
             color='black', linewidth=2)

    ax1.scatter(center[0], center[1], center[2],
                color='yellow', s=80)

    ax1.set_title("Trajectory + Channel Axis")

    # distance distribution
    ax2 = fig.add_subplot(222)
    ax2.hist(event_dist, bins=30)
    ax2.set_title("Event Distance to Axis")

    # risk signal
    ax3 = fig.add_subplot(223)
    ax3.plot(risk)
    ax3.scatter(events, risk[events], color='red')
    ax3.set_title("Risk Signal")

    # deviation over time
    ax4 = fig.add_subplot(224)
    ax4.plot(traj_dist)
    ax4.set_title("Distance to Axis over Time")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/v12_metrics.png", dpi=200)
    plt.show()

    print("\nSaved V12 output")


if __name__ == "__main__":
    main()
