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
# 3. Metrics
# =========================

def compute_metrics(traj, dt):
    v = np.gradient(traj, axis=0) / dt
    a = np.gradient(v, axis=0) / dt

    flow = np.linalg.norm(v, axis=1)
    curvature = np.linalg.norm(a, axis=1)

    risk = flow * curvature
    return v, flow, curvature, risk

# =========================
# 4. Event Detection
# =========================

def detect_events(signal, factor=2.5):
    threshold = np.mean(signal) * factor
    peaks = np.where(signal > threshold)[0]

    # Cluster peaks → einzelne Events
    events = []
    current = [peaks[0]]

    for i in range(1, len(peaks)):
        if peaks[i] - peaks[i-1] < 10:
            current.append(peaks[i])
        else:
            events.append(int(np.mean(current)))
            current = [peaks[i]]

    events.append(int(np.mean(current)))
    return np.array(events)

# =========================
# 5. Lobe classification
# =========================

def classify_lobes(traj, events):
    x = traj[events, 0]
    labels = np.where(x > 0, 1, 0)  # 1=Right, 0=Left
    return labels

# =========================
# 6. Build features
# =========================

def build_features(traj, velocity, events):
    pos = traj[events]
    vel = velocity[events]

    features = np.hstack([pos, vel])  # [x,y,z, vx,vy,vz]
    return features

# =========================
# 7. Predict next lobe
# =========================

def build_predictor(features, labels):
    # Simple prototype (mean of each class)
    left_proto = features[labels == 0].mean(axis=0)
    right_proto = features[labels == 1].mean(axis=0)

    return left_proto, right_proto

def predict(features, left_proto, right_proto):
    preds = []
    for f in features:
        dL = np.linalg.norm(f - left_proto)
        dR = np.linalg.norm(f - right_proto)
        preds.append(1 if dR < dL else 0)
    return np.array(preds)

# =========================
# 8. Evaluate transitions
# =========================

def compute_next_labels(labels):
    # next lobe after event
    next_labels = np.roll(labels, -1)
    return next_labels[:-1], labels[:-1]

# =========================
# 9. Main
# =========================

def main():
    print("Running Discovery Core V9...")

    os.makedirs("DISCOVERY_ENGINE/outputs", exist_ok=True)

    traj = simulate()
    v, flow, curvature, risk = compute_metrics(traj, dt=0.01)

    events = detect_events(risk)
    labels = classify_lobes(traj, events)

    features = build_features(traj, v, events)

    # next step prediction problem
    next_labels, current_labels = compute_next_labels(labels)
    features = features[:-1]

    left_proto, right_proto = build_predictor(features, next_labels)
    preds = predict(features, left_proto, right_proto)

    accuracy = np.mean(preds == next_labels)

    print(f"Events: {len(events)}")
    print(f"Prediction Accuracy: {accuracy:.3f}")

    # =========================
    # Visualization
    # =========================

    fig = plt.figure(figsize=(12, 6))

    ax = fig.add_subplot(121, projection='3d')
    ax.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.3)

    correct = preds == next_labels

    ax.scatter(
        traj[events[:-1],0],
        traj[events[:-1],1],
        traj[events[:-1],2],
        c=correct,
        cmap='coolwarm',
        s=40
    )

    ax.set_title("Prediction (blue=correct, red=wrong)")

    ax2 = fig.add_subplot(122)
    ax2.plot(risk, label="Risk")

    ax2.scatter(events[:-1], risk[events[:-1]], c=correct, cmap='coolwarm')

    ax2.set_title("Risk + Prediction Quality")
    ax2.legend()

    plt.tight_layout()
    plt.savefig("DISCOVERY_ENGINE/outputs/v9_prediction.png", dpi=200)
    plt.show()

    print("Saved V9 output")

# =========================

if __name__ == "__main__":
    main()
