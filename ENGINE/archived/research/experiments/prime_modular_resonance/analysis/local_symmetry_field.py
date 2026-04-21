import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")

df["theta"] = 2 * np.pi * df["t"] / 24.0
gh = df[df["phase"] == "GH"].copy()

# ----------------------------
# BINNING
# ----------------------------
bins = 36
theta_bins = np.linspace(0, 2*np.pi, bins + 1)
bin_centers = (theta_bins[:-1] + theta_bins[1:]) / 2

gh["theta_bin"] = pd.cut(
    gh["theta"],
    bins=theta_bins,
    labels=False,
    include_lowest=True
)

density = gh.groupby("theta_bin").size()
density = density.reindex(range(bins), fill_value=0)

# ----------------------------
# PEAK DETECTION
# ----------------------------
threshold = density.mean() + density.std()

peaks = []
for i in range(1, bins - 1):
    if density[i] > density[i - 1] and density[i] > density[i + 1]:
        if density[i] > threshold:
            peaks.append(i)

peak_angles = bin_centers[peaks]

# ----------------------------
# LOCAL SYMMETRY DETECTOR
# ----------------------------
window = 3  # lokale Umgebung
labels = np.zeros(bins)

phi = 2 * np.pi / 5
hexagon = 2 * np.pi / 6
quad = 2 * np.pi / 4

def score_pattern(local_peaks, target_angle):
    if len(local_peaks) < 2:
        return 999
    diffs = np.diff(local_peaks)
    return np.mean(np.abs(diffs - target_angle))

for i in range(bins):

    # lokale Peaks im Fenster
    local = []
    for p in peak_angles:
        if abs(p - bin_centers[i]) < window * (2*np.pi / bins):
            local.append(p)

    if len(local) < 2:
        labels[i] = 0
        continue

    local = np.sort(local)

    s_phi = score_pattern(local, phi)
    s_hex = score_pattern(local, hexagon)
    s_quad = score_pattern(local, quad)

    best = min([
        ("phi", s_phi),
        ("hex", s_hex),
        ("quad", s_quad)
    ], key=lambda x: x[1])

    if best[0] == "phi":
        labels[i] = 1
    elif best[0] == "hex":
        labels[i] = 2
    elif best[0] == "quad":
        labels[i] = 3

# ----------------------------
# PLOT FIELD
# ----------------------------
plt.figure(figsize=(10,5))

plt.scatter(bin_centers, labels, c=labels, cmap="coolwarm", s=80)

plt.yticks([0,1,2,3], ["none", "phi", "hex", "quad"])
plt.xlabel("theta (rad)")
plt.title("Local Symmetry Field")

# Peaks anzeigen
for angle in peak_angles:
    plt.axvline(angle, linestyle="--", alpha=0.3)

plt.grid(alpha=0.3)
plt.show()
