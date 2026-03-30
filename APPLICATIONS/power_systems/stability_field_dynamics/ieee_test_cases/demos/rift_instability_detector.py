# rift_instability_detector.py

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

    return trajectory


def compute_instability(signal):
    """
    Instability = local change (velocity magnitude)
    """
    velocity = np.diff(signal)
    instability = np.abs(velocity)

    return instability


def detect_events(instability, threshold_factor=2.0):
    """
    Detect spikes = instability events
    """
    mean = np.mean(instability)
    std = np.std(instability)

    threshold = mean + threshold_factor * std

    events = np.where(instability > threshold)[0]

    print(f"\n📊 Instability threshold: {threshold:.4f}")
    print(f"⚠️ Detected events: {len(events)}")

    return events, threshold


def plot_instability(instability, events, threshold):
    plt.figure(figsize=(10, 4))

    plt.plot(instability, label="instability")

    if len(events) > 0:
        plt.scatter(events, instability[events], color="red", label="events")

    plt.axhline(y=threshold, linestyle="--", label="threshold")

    plt.title("Instability Detector")
    plt.xlabel("time step")
    plt.ylabel("instability")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "instability_detection.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    # NON-BLOCKING
    plt.show(block=False)
    plt.pause(0.1)


def main():
    trajectory = load_data()

    # optional downsampling (important for stability!)
    trajectory = trajectory[::2]

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    inst1 = compute_instability(pc1)
    inst2 = compute_instability(pc2)

    print("\n--- PC1 ---")
    events1, th1 = detect_events(inst1)

    print("\n--- PC2 ---")
    events2, th2 = detect_events(inst2)

    plot_instability(inst1, events1, th1)

    print("\n🚀 Instability detection complete")


if __name__ == "__main__":
    main()
