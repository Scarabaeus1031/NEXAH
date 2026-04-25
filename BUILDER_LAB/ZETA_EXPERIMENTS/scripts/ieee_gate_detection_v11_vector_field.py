# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v11_vector_field.py
#
# v11: Phase-Radius Vector Field
#
# Goal:
# Compute flow:
#   dr/dt, dθ/dt
# → visualize system movement in (r, θ)

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

OUTPUT_PATH = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v11_vector_field.png"


# --------------------------------------------------
# SIGNAL
# --------------------------------------------------
def generate_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            x[i] = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            x[i] = np.random.normal(0, 1.0)

    return x


# --------------------------------------------------
# MAIN
# --------------------------------------------------
t = np.linspace(0, 100, 1000)
x = generate_signal(t)

dx = np.gradient(x, t)

# phase + radius
theta = np.arctan2(dx, x)
r = np.sqrt(x**2 + dx**2)

# derivatives
dr_dt = np.gradient(r, t)
dtheta_dt = np.gradient(theta, t)

# clean NaNs
mask = ~np.isnan(theta) & ~np.isnan(r)
theta = theta[mask]
r = r[mask]
dr_dt = dr_dt[mask]
dtheta_dt = dtheta_dt[mask]

# --------------------------------------------------
# GRID
# --------------------------------------------------
bins_theta = 30
bins_r = 20

theta_bins = np.linspace(-np.pi, np.pi, bins_theta)
r_bins = np.linspace(0, np.max(r), bins_r)

theta_idx = np.digitize(theta, theta_bins) - 1
r_idx = np.digitize(r, r_bins) - 1

U = np.zeros((bins_theta, bins_r))
V = np.zeros((bins_theta, bins_r))
counts = np.zeros((bins_theta, bins_r))

for i in range(len(theta)):
    ti = theta_idx[i]
    ri = r_idx[i]

    if 0 <= ti < bins_theta and 0 <= ri < bins_r:
        U[ti, ri] += dtheta_dt[i]
        V[ti, ri] += dr_dt[i]
        counts[ti, ri] += 1

# normalize
mask_counts = counts > 0
U[mask_counts] /= counts[mask_counts]
V[mask_counts] /= counts[mask_counts]

# grid centers
theta_centers = (theta_bins[:-1] + theta_bins[1:]) / 2
r_centers = (r_bins[:-1] + r_bins[1:]) / 2

T, R = np.meshgrid(theta_centers, r_centers, indexing="ij")

# --------------------------------------------------
# PLOT
# --------------------------------------------------
plt.figure(figsize=(8, 6))

plt.quiver(
    T, R,
    U, V,
    scale=10,
    width=0.003
)

plt.xlabel("θ (phase)")
plt.ylabel("r (radius)")
plt.title("v11 — Flow Field in (r, θ) Space")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)

print("\n--- NEXAH IEEE Gate Detection v11 ---")
print(f"Saved to: {OUTPUT_PATH}")

plt.show()
