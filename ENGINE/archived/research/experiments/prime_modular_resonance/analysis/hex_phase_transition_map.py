import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv").copy()

if "theta" not in df.columns:
    df["theta"] = 2 * np.pi * df["t"] / 24.0

# ----------------------------
# GLOBAL THRESHOLDS
# ----------------------------
loops_low = df["loops"].quantile(0.33)
loops_high = df["loops"].quantile(0.66)

c_low = df["C"].quantile(0.33)
c_high = df["C"].quantile(0.66)

print("\n--- GLOBAL THRESHOLDS ---")
print(f"loops_low  = {loops_low:.3f}")
print(f"loops_high = {loops_high:.3f}")
print(f"c_low      = {c_low:.6f}")
print(f"c_high     = {c_high:.6f}")

# ----------------------------
# PHASE CLASSIFIER
# 0 = collapse / KKK
# 1 = transition / GH
# 2 = stable-hex / CCC-like
# ----------------------------
def classify_phase(row):
    if row["loops"] <= loops_low and row["C"] <= c_low:
        return 0
    elif row["loops"] >= loops_high and row["C"] >= c_high:
        return 2
    else:
        return 1

df["phase_code"] = df.apply(classify_phase, axis=1)
phase_names = {0: "KKK", 1: "GH", 2: "HEX"}

# ----------------------------
# PIVOT MAP
# ----------------------------
loads_sorted = sorted(df["load"].unique())
times_sorted = sorted(df["t"].unique())

phase_map = (
    df.pivot_table(index="load", columns="t", values="phase_code", aggfunc="mean")
      .reindex(index=loads_sorted, columns=times_sorted)
)

# ----------------------------
# HEX DENSITY BY ANGLE
# ----------------------------
hex_df = df[df["phase_code"] == 2].copy()

bins = 24
theta_bins = np.linspace(0, 2*np.pi, bins + 1)
bin_centers = (theta_bins[:-1] + theta_bins[1:]) / 2

df["theta_bin"] = pd.cut(df["theta"], bins=theta_bins, labels=False, include_lowest=True)
hex_df["theta_bin"] = pd.cut(hex_df["theta"], bins=theta_bins, labels=False, include_lowest=True)

all_bins = np.arange(bins)
total_density = df.groupby("theta_bin").size().reindex(all_bins, fill_value=0)
hex_density = hex_df.groupby("theta_bin").size().reindex(all_bins, fill_value=0)

hex_ratio = np.divide(
    hex_density.values,
    total_density.values,
    out=np.zeros_like(hex_density.values, dtype=float),
    where=total_density.values > 0
)

# ----------------------------
# PLOTS
# ----------------------------
fig = plt.figure(figsize=(14, 10))

# 1. Heatmap
ax1 = plt.subplot(2, 2, 1)
im = ax1.imshow(
    phase_map.values,
    aspect="auto",
    interpolation="nearest",
    origin="lower"
)
ax1.set_title("Hex Phase Transition Map")
ax1.set_xlabel("t")
ax1.set_ylabel("load")
ax1.set_xticks(np.arange(len(times_sorted)))
ax1.set_xticklabels(times_sorted)
ax1.set_yticks(np.arange(len(loads_sorted)))
ax1.set_yticklabels([f"{x:.1f}" for x in loads_sorted])

cbar = plt.colorbar(im, ax=ax1)
cbar.set_ticks([0, 1, 2])
cbar.set_ticklabels(["KKK", "GH", "HEX"])

# 2. Polar hex density
ax2 = plt.subplot(2, 2, 2, projection="polar")
ax2.plot(bin_centers, hex_ratio, marker="o")
ax2.set_title("HEX Density vs Angle")

# 3. Scatter C vs theta
ax3 = plt.subplot(2, 2, 3)
colors = df["phase_code"].map({0: "black", 1: "orange", 2: "red"})
ax3.scatter(df["theta"], df["C"], c=colors, alpha=0.7)
ax3.set_title("C vs θ by Phase")
ax3.set_xlabel("theta (rad)")
ax3.set_ylabel("C")

# 4. Scatter loops vs theta
ax4 = plt.subplot(2, 2, 4)
ax4.scatter(df["theta"], df["loops"], c=colors, alpha=0.7)
ax4.set_title("Loops vs θ by Phase")
ax4.set_xlabel("theta (rad)")
ax4.set_ylabel("loops")

plt.tight_layout()
plt.show()

# ----------------------------
# SUMMARY
# ----------------------------
print("\n--- PHASE COUNTS ---")
counts = df["phase_code"].value_counts().sort_index()
for code, count in counts.items():
    print(f"{phase_names[code]}: {count}")

hex_peak_bin = int(np.argmax(hex_ratio))
hex_peak_theta = bin_centers[hex_peak_bin]

print("\n--- HEX PEAK ---")
print(f"HEX peak theta = {hex_peak_theta:.3f} rad ({np.degrees(hex_peak_theta):.1f}°)")
