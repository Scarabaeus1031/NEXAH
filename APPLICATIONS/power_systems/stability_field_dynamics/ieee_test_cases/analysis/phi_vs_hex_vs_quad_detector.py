import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")
df["theta"] = 2 * np.pi * df["t"] / 24.0

# GH Fokus
gh = df[df["phase"] == "GH"].copy()

# ----------------------------
# BINNING
# ----------------------------
bins = 36
theta_bins = np.linspace(0, 2*np.pi, bins + 1)
bin_centers = (theta_bins[:-1] + theta_bins[1:]) / 2

gh["theta_bin"] = pd.cut(gh["theta"], bins=theta_bins, labels=False, include_lowest=True)

all_bins = np.arange(bins)
density = gh.groupby("theta_bin").size().reindex(all_bins, fill_value=0)

# ----------------------------
# PEAK DETECTION
# ----------------------------
threshold = np.percentile(density, 80)
peaks = np.where(density > threshold)[0]

peak_angles = bin_centers[peaks]

# sortiert
peak_angles = np.sort(peak_angles)

# ----------------------------
# ABSTÄNDE
# ----------------------------
diffs = np.diff(np.concatenate([peak_angles, [peak_angles[0] + 2*np.pi]]))

# ----------------------------
# REFERENZEN
# ----------------------------
ref_phi = 2*np.pi / 5      # 72°
ref_hex = 2*np.pi / 6      # 60°
ref_quad = 2*np.pi / 4     # 90°

def score(diffs, ref):
    return np.mean(np.abs(diffs - ref))

score_phi = score(diffs, ref_phi)
score_hex = score(diffs, ref_hex)
score_quad = score(diffs, ref_quad)

# ----------------------------
# PRINT
# ----------------------------
print("\n--- GEOMETRY DETECTOR ---")
print(f"phi (72°) score : {score_phi:.4f}")
print(f"hex (60°) score : {score_hex:.4f}")
print(f"quad (90°) score: {score_quad:.4f}")

best = min([
    ("phi", score_phi),
    ("hex", score_hex),
    ("quad", score_quad)
], key=lambda x: x[1])

print(f"\nBest match: {best[0]}")

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(8,6))
plt.plot(bin_centers, density, label="GH density")

for angle in peak_angles:
    plt.axvline(angle, linestyle="--", alpha=0.5)

plt.title("Peak Detection (θ space)")
plt.xlabel("theta (rad)")
plt.ylabel("density")
plt.legend()

plt.show()
