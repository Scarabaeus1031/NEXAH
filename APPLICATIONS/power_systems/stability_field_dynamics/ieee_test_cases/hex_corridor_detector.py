import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================================
# DATA SOURCE
# ============================================================

def generate_test_data(N=200):
    """
    Fallback data generator (used if no pipeline connected yet)
    """
    np.random.seed(0)

    theta = np.linspace(0, 2*np.pi, N)

    # synthetic but structured (ähnlich deinem System)
    c = 0.02 + 0.01 * np.sin(theta * 2) + 0.003*np.random.randn(N)
    loops = 3 + 2 * np.cos(theta * 3) + 0.5*np.random.randn(N)

    return theta, c, loops


# OPTIONAL: später Pipeline hier einhängen
try:
    from ENGINE.research.experiments.prime_modular_resonance.analysis.phase_data_pipeline import load_phase_data
    theta_values, c_values, loop_values = load_phase_data()
    print("Loaded data from pipeline")
except:
    theta_values, c_values, loop_values = generate_test_data()
    print("Using fallback test data")


# ============================================================
# GH CORRIDOR DETECTION
# ============================================================

def compute_gh_corridor(theta, c, loops):

    # normalize
    c_norm = (c - np.min(c)) / (np.max(c) - np.min(c) + 1e-8)
    l_norm = (loops - np.min(loops)) / (np.max(loops) - np.min(loops) + 1e-8)

    # GH = BALANCE REGION (zentraler Punkt!)
    gh_score = (1 - np.abs(c_norm - 0.5)*2) * (1 - np.abs(l_norm - 0.5)*2)

    # smooth
    gh_score_smooth = gaussian_filter(gh_score, sigma=1.0)

    # threshold → corridor
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

# --- θ vs GH ---
plt.subplot(1,3,1)
plt.scatter(theta_values, gh_score, c="gray", alpha=0.4, label="all")
plt.scatter(theta_corridor, gh_score[gh_mask], c="red", label="GH corridor")
plt.xlabel("theta (rad)")
plt.ylabel("GH score")
plt.title("GH Corridor Detection")
plt.legend()

# --- Phase Space ---
plt.subplot(1,3,2)
plt.scatter(c_values, loop_values, c="gray", alpha=0.3)
plt.scatter(c_corridor, loops_corridor, c="red", label="corridor")
plt.xlabel("C")
plt.ylabel("loops")
plt.title("Phase Space (C vs loops)")
plt.legend()

# --- Polar View (SEHR WICHTIG)
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

# zusätzliche Diagnose
print("\n--- GH METRICS ---")
print(f"GH score mean: {np.mean(gh_score):.4f}")
print(f"GH score max : {np.max(gh_score):.4f}")
