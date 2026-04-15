# rift_fft_analysis.py

import numpy as np
import os
import matplotlib.pyplot as plt

BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")


def load_data():
    trajectory = None
    rift = None

    # robust loading
    for name in ["trajectory.npy", "states.npy"]:
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            trajectory = np.load(path)
            print(f"✅ Loaded trajectory: {name}")
            break

    for name in ["rift_curve.npy", "rift.npy", "rift_points.npy"]:
        path = os.path.join(RIFT_DIR, name)
        if os.path.exists(path):
            rift = np.load(path)
            print(f"✅ Loaded rift: {name}")
            break

    if trajectory is None or rift is None:
        raise FileNotFoundError("❌ Missing trajectory or rift data")

    return trajectory, rift


def compute_fft(signal):
    n = len(signal)

    # remove mean (important!)
    signal = signal - np.mean(signal)

    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(n)

    power = np.abs(fft_vals)

    return freqs, power


def analyze_signal(signal, label):
    freqs, power = compute_fft(signal)

    # only positive frequencies
    mask = freqs > 0
    freqs = freqs[mask]
    power = power[mask]

    # find dominant peaks
    top_indices = np.argsort(power)[-5:][::-1]

    print(f"\n🔍 Dominant frequencies ({label}):")
    for i in top_indices:
        print(f"  f = {freqs[i]:.4f}  | power = {power[i]:.4f}")

    return freqs, power


def plot_fft(freqs1, power1, freqs2, power2):
    plt.figure(figsize=(10, 5))

    plt.plot(freqs1, power1, label="PC1 spectrum")
    plt.plot(freqs2, power2, label="PC2 spectrum")

    # optional reference line (scaled idea of resonance)
    plt.axvline(x=0.07, linestyle="--", label="~0.07 (reference)")
    plt.axvline(x=0.12, linestyle="--", label="~0.12 (reference)")

    plt.xlabel("frequency (normalized)")
    plt.ylabel("power")
    plt.title("FFT — System Eigenfrequencies")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(RIFT_DIR, "fft_analysis.png")
    plt.savefig(save_path)
    print(f"💾 Saved → {save_path}")

    plt.show()


def main():
    trajectory, _ = load_data()

    pc1 = trajectory[:, 0]
    pc2 = trajectory[:, 1]

    f1, p1 = analyze_signal(pc1, "PC1")
    f2, p2 = analyze_signal(pc2, "PC2")

    plot_fft(f1, p1, f2, p2)

    print("\n🚀 FFT analysis complete")


if __name__ == "__main__":
    main()
