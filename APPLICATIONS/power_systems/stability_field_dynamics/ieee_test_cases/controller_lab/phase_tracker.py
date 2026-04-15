# phase_tracker.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


def load_data():
    traj = np.load(os.path.join(BASE_DIR, "states.npy"))
    return traj[:, :2]


def dominant_freq(signal):
    fft_vals = np.fft.rfft(signal)
    power = np.abs(fft_vals)
    freqs = np.fft.rfftfreq(len(signal))
    idx = np.argmax(power[1:]) + 1
    return freqs[idx]


def compute_phase(signal, freq):
    t = np.arange(len(signal))
    phase = (2 * np.pi * freq * t) % (2 * np.pi)
    return phase


def plot_phase(traj, phase):

    plt.figure(figsize=(8, 6))

    scatter = plt.scatter(
        traj[:, 0],
        traj[:, 1],
        c=phase,
        cmap='hsv'
    )

    plt.colorbar(scatter, label="phase")

    plt.title("Phase-colored trajectory")
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "phase_colored_trajectory.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.close()


def main():

    traj = load_data()

    pc1 = traj[:, 0]
    freq = dominant_freq(pc1)

    phase = compute_phase(pc1, freq)

    print(f"🔊 Dominant frequency: {freq:.4f}")

    plot_phase(traj, phase)

    print("🚀 Phase tracking complete")


if __name__ == "__main__":
    main()
