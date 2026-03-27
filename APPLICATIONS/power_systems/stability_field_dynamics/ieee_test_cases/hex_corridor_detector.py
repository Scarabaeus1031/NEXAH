import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# LOAD DATA FROM PIPELINE
# ============================================================

try:
    from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.phase_data_pipeline import load_phase_data
    theta_values, c_values, loop_values = load_phase_data()
    print("Loaded data from APPLICATIONS pipeline")
except Exception as e:
    print("Pipeline load failed → fallback:", e)

    # fallback (sicher)
    np.random.seed(0)
    N = 200
    theta_values = np.linspace(0, 2*np.pi, N)
    c_values = 0.02 + 0.01 * np.sin(theta_values * 2) + 0.003*np.random.randn(N)
    loop_values = 3 + 2 * np.cos(theta_values * 3) + np.random.randn(N)


# ============================================================
# GH CORRIDOR
# ============================================================

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)


def compute_gh_corridor(theta, c, loops):

    c_norm = normalize(c)
    l_norm = normalize(loops)

    # BALANCE REGION
    gh_score = (1 - np.abs(c_norm - 0.5)*2) * (1 - np.abs(l_norm - 0.5)*2)

    gh_score_smooth = gaussian_filter(gh_score, sigma=1.0)

    threshold = np.percentile(gh_score_smooth, 75)
    mask = gh_score_smooth > threshold

    return gh_score_smooth, mask


# ============================================================
# COMPUTE
# ============================================================

gh_score, gh_mask = compute_gh_corridor(
    theta_values,
    c_values,
    loop_values
)

theta_corridor = theta_values[gh_mask]
c_corridor = c_values[gh_mask]
loops_corridor = loop_values[gh_mask]


# ============================================================
# VISUALIZATION
# ============================================================

plt.figure(figsize=(14,6))

# θ vs GH
plt.subplot(1,3,1)
plt.scatter(theta_values, gh_score, c="gray", alpha=0.4, label="all")
plt.scatter(theta_corridor, gh_score[gh_mask], c="red", label="GH corridor")
plt.xlabel("theta (rad)")
plt.ylabel("GH score")
plt.title("GH Corridor Detection")
plt.legend()

# Phase space
plt.subplot(1,3,2)
plt.scatter(c_values, loop_values, c="gray", alpha=0.3)
plt.scatter(c_corridor, loops_corridor, c="red")
plt.xlabel("C")
plt.ylabel("loops")
plt.title("Phase Space")

# Polar
plt.subplot(1,3,3, projection="polar")
plt.scatter(theta_values, gh_score, alpha=0.3)
plt.scatter(theta_corridor, gh_score[gh_mask], c="red")
plt.title("GH Corridor (Polar)")

plt.tight_layout()
plt.show()


# ============================================================
# OUTPUT
# ============================================================

print("\n--- GH CORRIDOR ---")
print(f"Points in corridor: {len(theta_corridor)}")

if len(theta_corridor) > 0:
    print(f"theta mean: {np.mean(theta_corridor):.3f} rad")
    print(f"theta std : {np.std(theta_corridor):.3f} rad")
