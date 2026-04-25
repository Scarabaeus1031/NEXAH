# V33 — Probabilistic IOTA Field (No Threshold Model)

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.stats import zscore

# =========================
# TEST DATA (falls nichts geladen)
# =========================
try:
    theta = theta_unwrapped
    r_vals = r
except:
    print("No data found → using test data")
    t = np.linspace(0, 1000, 1000)
    theta = np.linspace(0, 300, 1000)
    r_vals = 0.5 + 0.5*np.sin(0.15*theta)

    # Transition hinzufügen
    noise = np.random.normal(0, 0.5, size=1000)
    r_vals[600:] = r_vals[600:] + noise[600:]

# =========================
# DERIVATIVES
# =========================
dr_dtheta = np.gradient(r_vals, theta)

# =========================
# DENSITY FIELD
# =========================
bins = 80
heatmap, xedges, yedges = np.histogram2d(theta, r_vals, bins=bins)
heatmap_smooth = gaussian_filter(heatmap, sigma=2)

# =========================
# GREYSPACE (FIXED VERSION)
# =========================
density_vals = []
for t_, r_ in zip(theta, r_vals):
    xi = np.searchsorted(xedges, t_) - 1
    yi = np.searchsorted(yedges, r_) - 1
    if 0 <= xi < bins and 0 <= yi < bins:
        density_vals.append(heatmap_smooth[xi, yi])
    else:
        density_vals.append(0)

density_vals = np.array(density_vals)

# normalize density
density_norm = (density_vals - density_vals.min()) / (density_vals.max() - density_vals.min() + 1e-6)

# greyspace = inverse normalized
greyspace = 1 - density_norm

# =========================
# FLOW SCORE
# =========================
flow_score = np.abs(zscore(dr_dtheta))

# =========================
# PROBABILITY FIELD
# =========================
alpha = 0.5
beta = 0.5

prob_iota = alpha * greyspace + beta * flow_score
prob_iota = (prob_iota - prob_iota.min()) / (prob_iota.max() - prob_iota.min())

# =========================
# IOTA (soft detection)
# =========================
threshold = np.percentile(prob_iota, 98)
iota_indices = np.where(prob_iota > threshold)[0]

# =========================
# VISUAL
# =========================
plt.figure(figsize=(12,6))

# base cloud
plt.scatter(theta, r_vals, c=prob_iota, cmap="viridis", s=10, alpha=0.6)

# IOTA
plt.scatter(theta[iota_indices], r_vals[iota_indices],
            c="red", s=80, label="IOTA")

# transition line
plt.axvline(x=120, linestyle="--", color="black", label="transition")

plt.colorbar(label="P(IOTA)")
plt.xlabel("theta")
plt.ylabel("r")
plt.title("V33 — Probabilistic IOTA Field")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("v33_probabilistic_iota.png", dpi=150)
plt.show()

# =========================
# OUTPUT
# =========================
print("\n--- V33 RESULTS ---")
print(f"IOTA (soft): {len(iota_indices)}")
print(f"Mean P(IOTA): {np.mean(prob_iota[iota_indices]):.3f}")
