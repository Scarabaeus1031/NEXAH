import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")

# Winkel berechnen
df["theta"] = 2 * np.pi * df["t"] / 24.0

# GH filtern
gh = df[df["phase"] == "GH"]

# ----------------------------
# BINNING (Winkel in Sektoren)
# ----------------------------
bins = 36  # 10° Auflösung
theta_bins = np.linspace(0, 2*np.pi, bins + 1)

df["theta_bin"] = pd.cut(df["theta"], bins=theta_bins, labels=False, include_lowest=True)
gh["theta_bin"] = pd.cut(gh["theta"], bins=theta_bins, labels=False, include_lowest=True)

# ----------------------------
# GH-DICHTE PRO WINKEL
# ----------------------------
gh_density = gh.groupby("theta_bin").size()
total_density = df.groupby("theta_bin").size()

density_ratio = (gh_density / total_density).fillna(0)

# ----------------------------
# LOOPS-MITTEL PRO WINKEL
# ----------------------------
loops_mean = df.groupby("theta_bin")["loops"].mean()

# ----------------------------
# GRADIENT (Übergang finden)
# ----------------------------
grad_loops = np.gradient(loops_mean)

# ----------------------------
# KNICK ERKENNEN
# ----------------------------
# 1. Maximum GH-Dichte
knick_density_bin = density_ratio.idxmax()

# 2. Maximum Gradient (stärkster Übergang)
knick_gradient_bin = np.argmax(np.abs(grad_loops))

# Winkel berechnen
bin_centers = (theta_bins[:-1] + theta_bins[1:]) / 2

theta_knick_density = bin_centers[knick_density_bin]
theta_knick_gradient = bin_centers[knick_gradient_bin]

# ----------------------------
# PRINT RESULTS
# ----------------------------
print("\n--- KNICK ANALYSIS ---")
print(f"Knick (GH density max): {theta_knick_density:.3f} rad ({np.degrees(theta_knick_density):.1f}°)")
print(f"Knick (Gradient max):   {theta_knick_gradient:.3f} rad ({np.degrees(theta_knick_gradient):.1f}°)")

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10,5))

plt.plot(bin_centers, density_ratio, label="GH density")
plt.plot(bin_centers, loops_mean / loops_mean.max(), label="loops (norm)")
plt.plot(bin_centers, np.abs(grad_loops) / np.max(np.abs(grad_loops)), label="|gradient|")

plt.axvline(theta_knick_density, linestyle="--", label="knick (density)")
plt.axvline(theta_knick_gradient, linestyle=":", label="knick (gradient)")

plt.xlabel("theta (rad)")
plt.ylabel("normalized")
plt.title("Knick Angle Detection")
plt.legend()

plt.show()
