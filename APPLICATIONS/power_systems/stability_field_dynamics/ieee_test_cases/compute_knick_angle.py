import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")

# Winkel berechnen
df["theta"] = 2 * np.pi * df["t"] / 24.0

# GH filtern (WICHTIG: copy!)
gh = df[df["phase"] == "GH"].copy()

# ----------------------------
# BINNING
# ----------------------------
bins = 36
theta_bins = np.linspace(0, 2*np.pi, bins + 1)

df["theta_bin"] = pd.cut(df["theta"], bins=theta_bins, labels=False, include_lowest=True)
gh["theta_bin"] = pd.cut(gh["theta"], bins=theta_bins, labels=False, include_lowest=True)

# ----------------------------
# DICHTEN (FIX: reindex!)
# ----------------------------
all_bins = np.arange(bins)

gh_density = gh.groupby("theta_bin").size().reindex(all_bins, fill_value=0)
total_density = df.groupby("theta_bin").size().reindex(all_bins, fill_value=1)

density_ratio = gh_density / total_density

# ----------------------------
# LOOPS
# ----------------------------
loops_mean = df.groupby("theta_bin")["loops"].mean().reindex(all_bins, fill_value=0)

# ----------------------------
# GRADIENT
# ----------------------------
grad_loops = np.gradient(loops_mean)

# ----------------------------
# KNICK DETECTION
# ----------------------------
knick_density_bin = density_ratio.idxmax()
knick_gradient_bin = np.argmax(np.abs(grad_loops))

bin_centers = (theta_bins[:-1] + theta_bins[1:]) / 2

theta_knick_density = bin_centers[knick_density_bin]
theta_knick_gradient = bin_centers[knick_gradient_bin]

# ----------------------------
# PRINT
# ----------------------------
print("\n--- KNICK ANALYSIS ---")
print(f"Knick (GH density max): {theta_knick_density:.3f} rad ({np.degrees(theta_knick_density):.1f}°)")
print(f"Knick (Gradient max):   {theta_knick_gradient:.3f} rad ({np.degrees(theta_knick_gradient):.1f}°)")

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10,5))

plt.plot(bin_centers, density_ratio, label="GH density")
plt.plot(bin_centers, loops_mean / np.max(loops_mean + 1e-9), label="loops (norm)")
plt.plot(bin_centers, np.abs(grad_loops) / np.max(np.abs(grad_loops) + 1e-9), label="|gradient|")

plt.axvline(theta_knick_density, linestyle="--", label="knick (density)")
plt.axvline(theta_knick_gradient, linestyle=":", label="knick (gradient)")

plt.xlabel("theta (rad)")
plt.ylabel("normalized")
plt.title("Knick Angle Detection")
plt.legend()

plt.show()
