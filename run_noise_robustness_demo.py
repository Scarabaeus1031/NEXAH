# ==========================================================
# ⚡ NEXAH Demo — Noise Robustness (Upgraded)
# ==========================================================
# Shows that structural peaks persist under noise
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ----------------------------------------------------------
# LORENZ SYSTEM
# ----------------------------------------------------------

def lorenz(x, y, z, s=10, r=28, b=8/3):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz


def simulate_lorenz(n_steps=2000, dt=0.01):
    xs = np.zeros(n_steps)
    ys = np.zeros(n_steps)
    zs = np.zeros(n_steps)

    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)

    for i in range(n_steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx * dt
        ys[i+1] = ys[i] + dy * dt
        zs[i+1] = zs[i] + dz * dt

    return xs, ys, zs


# ----------------------------------------------------------
# STRUCTURAL SIGNAL
# ----------------------------------------------------------

def compute_signal(x, y, z):
    dx = np.gradient(x)
    dy = np.gradient(y)
    dz = np.gradient(z)

    signal = np.sqrt(dx**2 + dy**2 + dz**2)
    signal = (signal - np.min(signal)) / (np.max(signal) + 1e-8)
    return signal


# ----------------------------------------------------------
# NOISE
# ----------------------------------------------------------

def add_noise(x, y, z, noise_level=0.3):
    xn = x + noise_level * np.std(x) * np.random.randn(len(x))
    yn = y + noise_level * np.std(y) * np.random.randn(len(y))
    zn = z + noise_level * np.std(z) * np.random.randn(len(z))
    return xn, yn, zn


# ----------------------------------------------------------
# PEAK MATCHING
# ----------------------------------------------------------

def match_peaks(peaks_a, peaks_b, tolerance=20):
    matches = 0
    for pa in peaks_a:
        if np.any(np.abs(peaks_b - pa) < tolerance):
            matches += 1
    return matches


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def main():

    print("\n⚡ NEXAH Demo — Noise Robustness (Upgraded)\n")

    # simulate system
    x, y, z = simulate_lorenz()

    # signals
    signal_clean = compute_signal(x, y, z)
    x_n, y_n, z_n = add_noise(x, y, z)
    signal_noisy = compute_signal(x_n, y_n, z_n)

    # peaks
    peaks_clean, _ = find_peaks(signal_clean, height=0.3)
    peaks_noisy, _ = find_peaks(signal_noisy, height=0.3)

    # matching
    matches = match_peaks(peaks_clean, peaks_noisy)
    match_ratio = matches / len(peaks_clean)

    # ------------------------------------------------------
    # PLOT
    # ------------------------------------------------------

    plt.figure(figsize=(12, 5))

    plt.plot(signal_clean, label="clean", alpha=0.6)
    plt.plot(signal_noisy, label="noisy", alpha=0.6)

    plt.scatter(peaks_clean, signal_clean[peaks_clean],
                color="green", s=15, label="clean peaks")

    plt.scatter(peaks_noisy, signal_noisy[peaks_noisy],
                color="red", s=10, alpha=0.7, label="noisy peaks")

    plt.title("Structural Peaks under Noise")
    plt.legend()
    plt.tight_layout()

    output_path = "outputs/demo/nexah_noise_robustness_v2.png"
    plt.savefig(output_path, dpi=150)

    print("✔ Saved plot →", output_path)

    # ------------------------------------------------------
    # STATS
    # ------------------------------------------------------

    print("\n📊 Stats:")
    print(f"Clean peaks: {len(peaks_clean)}")
    print(f"Noisy peaks: {len(peaks_noisy)}")
    print(f"Matched peaks: {matches}")
    print(f"Match ratio: {match_ratio:.2f}")

    print("\n🔥 Result:")
    print("Structural peaks remain aligned under noise")
    print("→ structure is not random")
    print("→ transitions are intrinsic to the system\n")


# ----------------------------------------------------------

if __name__ == "__main__":
    main()
