import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD
# ----------------------------
df = pd.read_csv("v34_physical_coupling.csv")
df["theta"] = 2 * np.pi * df["t"] / 24.0

# ----------------------------
# PHASE MASKS
# ----------------------------
df["is_GH"] = (df["phase"] == "GH").astype(int)
df["is_CCC"] = (df["phase"] == "CCC").astype(int)
df["is_KKK"] = (df["phase"] == "KKK").astype(int)

# ----------------------------
# BINNING
# ----------------------------
bins = len(df["t"].unique())
theta_bins = np.linspace(0, 2*np.pi, bins + 1)

df["theta_bin"] = pd.cut(df["theta"], bins=theta_bins, labels=False, include_lowest=True)

# ----------------------------
# PHASE DISTRIBUTION
# ----------------------------
gh_ratio = df.groupby("theta_bin")["is_GH"].mean()
ccc_ratio = df.groupby("theta_bin")["is_CCC"].mean()
kkk_ratio = df.groupby("theta_bin")["is_KKK"].mean()

# ----------------------------
# LOOPS & C FIELD
# ----------------------------
loops_mean = df.groupby("theta_bin")["loops"].mean()
c_mean = df.groupby("theta_bin")["C"].mean()

# fehlende bins
for arr in [gh_ratio, ccc_ratio, kkk_ratio, loops_mean, c_mean]:
    arr[:] = arr.reindex(range(bins), fill_value=0)

# ----------------------------
# TRANSITION SCORE
# ----------------------------
transition_score = (
    gh_ratio * loops_mean
    - ccc_ratio * 0.5
    - kkk_ratio * 0.2
)

# smoothing
transition_smooth = pd.Series(transition_score).rolling(3, center=True, min_periods=1).mean()

# ----------------------------
# KNICK / TRANSITION REGION
# ----------------------------
grad = np.gradient(transition_smooth)
transition_idx = np.argmax(np.abs(grad))

theta_bins_centers = (theta_bins[:-1] + theta_bins[1:]) / 2
theta_transition = theta_bins_centers[transition_idx]

# ----------------------------
# PRINT
# ----------------------------
print("\n--- PHASE TRANSITION FIELD ---")
print(f"Transition angle: {theta_transition:.3f} rad ({np.degrees(theta_transition):.1f}°)")

# ----------------------------
# PLOT
# ----------------------------
plt.figure(figsize=(10,5))

plt.plot(theta_bins_centers, gh_ratio, label="GH")
plt.plot(theta_bins_centers, ccc_ratio, label="CCC")
plt.plot(theta_bins_centers, kkk_ratio, label="KKK")

plt.plot(theta_bins_centers, transition_smooth / np.max(np.abs(transition_smooth)), label="transition score")

plt.axvline(theta_transition, linestyle="--", label="transition")

plt.xlabel("theta (rad)")
plt.ylabel("normalized")
plt.title("Phase Transition Field")
plt.legend()

plt.show()
