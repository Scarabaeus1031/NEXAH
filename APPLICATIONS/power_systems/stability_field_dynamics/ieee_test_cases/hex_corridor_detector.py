import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ----------------------------
# INPUT (reuse your data)
# ----------------------------
# expected:
# density (θ histogram)
# bin_centers (θ)
# c_values, loop_values, theta_values

# ----------------------------
# GH CORRIDOR DETECTION
# ----------------------------

# normalize inputs
c_norm = (c_values - np.min(c_values)) / (np.max(c_values) - np.min(c_values) + 1e-8)
l_norm = (loop_values - np.min(loop_values)) / (np.max(loop_values) - np.min(loop_values) + 1e-8)

# GH score = balanced region (not too high, not too low)
gh_score = (1 - np.abs(c_norm - 0.5)*2) * (1 - np.abs(l_norm - 0.5)*2)

# smooth
gh_score_smooth = gaussian_filter(gh_score, sigma=1.0)

# threshold → corridor
threshold = np.percentile(gh_score_smooth, 75)
gh_mask = gh_score_smooth > threshold

# ----------------------------
# CLUSTER CORRIDOR POINTS
# ----------------------------
theta_corridor = theta_values[gh_mask]
c_corridor = c_values[gh_mask]
loops_corridor = loop_values[gh_mask]

# ----------------------------
# PLOT
# ----------------------------

plt.figure(figsize=(12,5))

# θ vs GH score
plt.subplot(1,2,1)
plt.scatter(theta_values, gh_score_smooth, c="gray", alpha=0.4, label="all")
plt.scatter(theta_corridor, gh_score_smooth[gh_mask], c="red", label="GH corridor")
plt.xlabel("theta (rad)")
plt.ylabel("GH score")
plt.title("GH Corridor Detection")
plt.legend()

# C vs loops (phase space)
plt.subplot(1,2,2)
plt.scatter(c_values, loop_values, c="gray", alpha=0.3)
plt.scatter(c_corridor, loops_corridor, c="red", label="corridor")
plt.xlabel("C")
plt.ylabel("loops")
plt.title("Corridor in Phase Space")
plt.legend()

plt.tight_layout()
plt.show()

# ----------------------------
# OUTPUT
# ----------------------------
print("\n--- GH CORRIDOR ---")
print(f"Points in corridor: {len(theta_corridor)}")

if len(theta_corridor) > 0:
    print(f"theta mean: {np.mean(theta_corridor):.3f}")
    print(f"theta std : {np.std(theta_corridor):.3f}")
