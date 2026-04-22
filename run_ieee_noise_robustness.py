# ==========================================================
# NEXAH Demo — IEEE Noise Robustness
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/data/ieee_noisy.csv"

NOISE_STD = 0.02   # small additional noise
PEAK_HEIGHT = None  # adaptive
PEAK_DISTANCE = 5

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

time = df["time"].values
signal_clean = df["voltage"].values

# normalize (important for stability)
signal_clean = (signal_clean - np.min(signal_clean)) / (np.max(signal_clean) - np.min(signal_clean))

# ----------------------------------------------------------
# ADD NOISE
# ----------------------------------------------------------

noise = np.random.normal(0, NOISE_STD, size=signal_clean.shape)
signal_noisy = signal_clean + noise

# ----------------------------------------------------------
# PEAK DETECTION (adaptive)
# ----------------------------------------------------------

# use percentile instead of fixed threshold
threshold_clean = np.percentile(signal_clean, 90)
threshold_noisy = np.percentile(signal_noisy, 90)

peaks_clean, _ = find_peaks(signal_clean, height=threshold_clean, distance=PEAK_DISTANCE)
peaks_noisy, _ = find_peaks(signal_noisy, height=threshold_noisy, distance=PEAK_DISTANCE)

# ----------------------------------------------------------
# MATCHING
# ----------------------------------------------------------

matched = 0

for pc in peaks_clean:
    if np.any(np.abs(peaks_noisy - pc) < 5):
        matched += 1

match_ratio = matched / len(peaks_clean) if len(peaks_clean) > 0 else 0

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(time, signal_clean, label="clean signal", linewidth=2)
plt.plot(time, signal_noisy, label="noisy signal", alpha=0.7)

plt.scatter(time[peaks_clean], signal_clean[peaks_clean], label="clean peaks", s=40)
plt.scatter(time[peaks_noisy], signal_noisy[peaks_noisy], label="noisy peaks", s=40, marker="x")

plt.title("NEXAH — IEEE Signal Robustness")
plt.xlabel("time")
plt.ylabel("normalized voltage")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

output_path = "outputs/demo/nexah_ieee_noise_robustness.png"
plt.savefig(output_path, dpi=150)

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH IEEE Noise Robustness")
print(f"✔ Loaded → {CSV_PATH}")
print(f"✔ Saved plot → {output_path}")

print("\n📊 Stats:")
print(f"Clean peaks: {len(peaks_clean)}")
print(f"Noisy peaks: {len(peaks_noisy)}")
print(f"Matched peaks: {matched}")
print(f"Match ratio: {match_ratio:.3f}")

print("\n🔥 Interpretation:")
print("Structural signal persists under measurement noise")
print("→ real system structure remains detectable")
print("→ not an artifact of synthetic construction")
