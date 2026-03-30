# rift_predictor_v3_frequency.py

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


def compute_fft(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))

    return freqs, power


def extract_dominant_frequency(signal):
    freqs, power = compute_fft(signal)

    # skip DC (index 0)
    idx = np.argmax(power[1:]) + 1
    dominant_freq = freqs[idx]

    print(f"🔊 Dominant frequency: {dominant_freq:.4f}")

    return dominant_freq


def nearest_rift_point(p, rift):
    dists = np.linalg.norm(rift - p, axis=1)
    return rift[np.argmin(dists)]


def predictive_frequency_control(trajectory, rift, gain=0.25):
    controlled = trajectory.copy()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    # dominant frequencies
    f1 = extract_dominant_frequency(pc1)
    f2 = extract_dominant_frequency(pc2)

    for t in range(len(controlled)):

        current = controlled[t]
        target = nearest_rift_point(current, rift)

        # phase-based modulation
        phase1 = np.sin(2 * np.pi * f1 * t)
        phase2 = np.sin(2 * np.pi * f2 * t)

        phase_weight = 0.5 * (phase1 + phase2)

        correction = gain * phase_weight * (target - current)

        # clamp → stability
        correction = np.clip(correction, -0.05, 0.05)

        controlled[t] += correction

    return controlled


def plot_result(original, controlled, rift):
    plt.figure(figsize=(10, 6))

    plt.plot(original[:, 0], original[:, 1],
             color="green", label="original")

    plt.plot(rift[:, 0], rift[:, 1],
             color="cyan", label="rift")

    plt.plot(controlled[:, 0], controlled[:, 1],
             color="gold", label="predictive v3 (frequency)")

    plt.scatter(original[-1, 0], original[-1, 1],
                color="red", label="orig end")

    plt.scatter(controlled[-1, 0], controlled[-1, 1],
                color="orange", label="controlled end")

    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "predictive_v3_frequency.png")
    plt.savefig(save_path, dpi=150)
    print(f"💾 Saved → {save_path}")

    plt.close()


def main():
    trajectory, rift = load_data()

    # 🔥 wichtig: auf 2D reduzieren
    trajectory = trajectory[:, :2]

    controlled = predictive_frequency_control(
        trajectory,
        rift,
        gain=0.2
    )

    plot_result(trajectory, controlled, rift)

    print("🚀 Predictive V3 (frequency-aware) complete")


if __name__ == "__main__":
    main()
