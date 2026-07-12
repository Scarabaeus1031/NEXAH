# ==========================================================
# NEXAH Demo — Noise Robustness Stress Test (v4)
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

np.random.seed(42)

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

N_RUNS = 30
NOISE_LEVELS = np.linspace(0.05, 0.5, 10)

# ----------------------------------------------------------
# SIGNAL
# ----------------------------------------------------------

t = np.linspace(0, 20, 2000)

def gaussian(x, mu, sigma):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2)

signal_clean = (
    gaussian(t, 1.0, 0.1) +
    gaussian(t, 3.0, 0.15) +
    gaussian(t, 7.5, 0.12) +
    gaussian(t, 10.5, 0.2) +
    gaussian(t, 13.0, 0.1) +
    gaussian(t, 19.0, 0.2)
)

signal_clean += 0.02 * np.sin(5 * t)

# clean reference
peaks_clean, _ = find_peaks(signal_clean, height=0.3)

# ----------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------

mean_ratios = []
std_ratios = []

for noise_std in NOISE_LEVELS:

    ratios = []

    for run in range(N_RUNS):

        noise = np.random.normal(0, noise_std, size=t.shape)
        signal_noisy = signal_clean + noise

        peaks_noisy, _ = find_peaks(
            signal_noisy,
            height=0.5,
            distance=50
        )

        matched = 0

        for pc in peaks_clean:
            if np.any(np.abs(peaks_noisy - pc) < 10):  # stricter
                matched += 1

        ratios.append(matched / len(peaks_clean))

    ratios = np.array(ratios)

    mean_ratios.append(np.mean(ratios))
    std_ratios.append(np.std(ratios))

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(NOISE_LEVELS, mean_ratios, marker="o", label="mean match ratio")
plt.fill_between(
    NOISE_LEVELS,
    np.array(mean_ratios) - np.array(std_ratios),
    np.array(mean_ratios) + np.array(std_ratios),
    alpha=0.2,
    label="± std"
)

plt.title("NEXAH — Robustness vs Noise Level")
plt.xlabel("noise std")
plt.ylabel("match ratio")
plt.ylim(0, 1.05)
plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()

output_path = "outputs/demo/nexah_noise_stress_test.png"
plt.savefig(output_path, dpi=150)

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH Stress Test — Noise Robustness Curve")
print(f"✔ Saved plot → {output_path}")

print("\n📊 Summary:")

for n, m, s in zip(NOISE_LEVELS, mean_ratios, std_ratios):
    print(f"Noise {n:.2f} → {m:.3f} ± {s:.3f}")

print("\n🔥 Interpretation:")
print("Shows how structural signal degrades under increasing noise")
print("→ defines operational boundary of the method")
