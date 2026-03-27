import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")

# Winkel berechnen
df["theta"] = 2 * np.pi * df["t"] / 24.0

# GH filtern (copy wichtig!)
gh = df[df["phase"] == "GH"].copy()

# ----------------------------
# BINNING (korrekt!)
# ----------------------------
bins = len(df["t"].unique())  # = 24
theta_bins = np.linspace(0, 2*np.pi, bins + 1)

df["theta_bin"] = pd.cut(df["theta"], bins=theta_bins, labels=False, include_lowest=True)
gh["theta_bin"] = pd.cut(gh["theta"], bins=theta_bins, labels=False, include_lowest=True)

# ----------------------------
# GH-DICHTE PRO WINKEL
# ----------------------------
gh_density = gh.groupby("theta_bin").size()
total_density = df.groupby("theta_bin").size()

density_ratio = (gh_density / total_density)

# fehlende bins auffüllen
density_ratio = density_ratio.reindex(range(bins), fill_value=0)

# ----------------------------
# LOOPS-MITTEL PRO WINKEL
# ----------------------------
loops_mean = df.groupby("theta_bin")["loops"].mean()
loops_mean = loops_mean.reindex(range(bins), fill_value=0)

# ----------------------------
# SMOOTHING (wichtig!)
# ----------------------------
density_smooth = density_ratio.rolling(3, center=True, min_periods=1).mean()
loops_smooth = loops_mean.rolling(3, center=True, min_periods=1).mean()

# ----------------------------
# GRADIENT (echter Übergang)
# ----------------------------
grad_loops = np.gradient(loops_smooth)

# ----------------------------
# KNICK ERKENNEN
# ----------------------------
knick_density_bin = density_smooth.idxmax()
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

plt.plot(bin_centers, density_smooth, label="GH density (smooth)")
plt.plot(bin_centers, loops_smooth / loops_smooth.max(), label="loops (norm)")
plt.plot(bin_centers, np.abs(grad_loops) / np.max(np.abs(grad_loops)), label="|gradient|")

plt.axvline(theta_knick_density, linestyle="--", label="knick (density)")
plt.axvline(theta_knick_gradient, linestyle=":", label="knick (gradient)")

plt.xlabel("theta (rad)")
plt.ylabel("normalized")
plt.title("Knick Angle Detection (Fixed)")
plt.legend()

plt.show()
