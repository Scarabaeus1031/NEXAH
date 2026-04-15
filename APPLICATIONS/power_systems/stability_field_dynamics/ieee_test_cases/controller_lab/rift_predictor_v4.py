# rift_predictor_v4_hybrid.py

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
    threshold = np.mean(instability) + factor * np.std(instability)
    return np.where(instability > threshold)[0]


def compute_fft(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def hybrid_control(trajectory, rift, gain_event=0.35, gain_freq=0.15):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    # event detection
    events = sorted(set(
        list(detect_events(compute_instability(pc1))) +
        list(detect_events(compute_instability(pc2)))
    ))

    print(f"⚡ Events: {events}")

    # frequency
    f1 = compute_fft(pc1)
    f2 = compute_fft(pc2)

    for t in range(len(controlled)):

        current = controlled[t]
        target = nearest_rift_point(current, rift)

        # --- event boost ---
        event_gain = gain_event if t in events else 0.0

        # --- frequency modulation ---
        phase = 0.5 * (
            np.sin(2 * np.pi * f1 * t) +
            np.sin(2 * np.pi * f2 * t)
        )

        freq_gain = gain_freq * phase

        correction = (event_gain + freq_gain) * (target - current)

        correction = np.clip(correction, -0.05, 0.05)

        controlled[t] += correction

    return controlled


def plot_result(original, controlled, rift):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1], label="original", color="green")
    plt.plot(rift[:, 0], rift[:, 1], label="rift", color="cyan")
    plt.plot(controlled[:, 0], controlled[:, 1], label="hybrid v4", color="gold")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", label="orig end")
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "predictive_v4_hybrid.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()


def main():
    trajectory, rift = load_data()
    trajectory = trajectory[:, :2]

    controlled = hybrid_control(trajectory, rift)

    plot_result(trajectory, controlled, rift)

    print("🚀 Hybrid Predictor V4 complete")


if __name__ == "__main__":
    main()
