# rift_predictor_v2.py (FIXED)

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


def load_data():
    trajectory = None

    for name in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory: {name}")
            break

    if trajectory is None:
        raise FileNotFoundError("❌ No trajectory file found")

    rift_path = os.path.join(RIFT_DIR, "rift_curve.npy")
    if not os.path.exists(rift_path):
        raise FileNotFoundError("❌ No rift_curve.npy found")

    rift = np.load(rift_path)
    print("✅ Loaded rift")

    return trajectory, rift


def compute_instability(signal):
    return np.abs(np.diff(signal))


def detect_events(instability, factor=2.0):
    mean = np.mean(instability)
    std = np.std(instability)
    threshold = mean + factor * std
    events = np.where(instability > threshold)[0]
    return events


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def predictive_control(trajectory, rift, lookahead=2, gain=0.2):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    inst1 = compute_instability(pc1)
    inst2 = compute_instability(pc2)

    events = sorted(set(
        list(detect_events(inst1)) +
        list(detect_events(inst2))
    ))

    print(f"🔮 Events: {events}")

    for t in events:
        for k in range(1, lookahead + 1):
            idx = t + k
            if idx >= len(controlled):
                continue

            current = controlled[idx]
            target = nearest_rift_point(current, rift)

            correction = gain * (target - current)

            # clamp (wichtig!)
            correction = np.clip(correction, -0.05, 0.05)

            controlled[idx] += correction

    return controlled


def plot_result(original, controlled, rift):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="predictive v2", color="gold")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "predictive_v2.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()   # 🔥 wichtig → kein freeze


def main():
    trajectory, rift = load_data()

    # 🔥 kleiner machen → stabil
    trajectory = trajectory[::2]

    controlled = predictive_control(
        trajectory,
        rift,
        lookahead=2,   # ↓ reduziert
        gain=0.2       # ↓ stabiler
    )

    plot_result(trajectory, controlled, rift)

    print("🚀 Predictive V2 stable")


if __name__ == "__main__":
    main()
