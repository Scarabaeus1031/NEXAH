"""
NEXAH — Lorenz Noise Robustness Validation

Goal:
Test if geometric structure survives noise.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ============================
# CONFIG
# ============================

N_RUNS = 10
STEPS = 2000
DT = 0.01

NOISE_LEVEL = 1.0  # <-- play with this (0.2, 0.5, 1.0, 2.0)

OUTPUT_DIR = "RESEARCH/validation/lorenz/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================
# LORENZ SYSTEM
# ============================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz(x):
    return np.array([
        sigma * (x[1] - x[0]),
        x[0] * (rho - x[2]) - x[1],
        x[0] * x[1] - beta * x[2]
    ])

# ============================
# SIMULATION
# ============================

def simulate(seed, noise=False):
    np.random.seed(seed)
    x = np.random.randn(3)

    traj = []

    for _ in range(STEPS):
        dx = lorenz(x)

        if noise:
            dx += NOISE_LEVEL * np.random.randn(3)

        x = x + DT * dx
        traj.append(x.copy())

    return np.array(traj)

# ============================
# RUN CLEAN + NOISY
# ============================

clean_trajectories = []
noisy_trajectories = []

clean_endpoints = []
noisy_endpoints = []

for i in range(N_RUNS):
    traj_clean = simulate(seed=i, noise=False)
    traj_noisy = simulate(seed=i, noise=True)

    clean_trajectories.append(traj_clean)
    noisy_trajectories.append(traj_noisy)

    clean_endpoints.append(traj_clean[-1])
    noisy_endpoints.append(traj_noisy[-1])

clean_trajectories = np.array(clean_trajectories)
noisy_trajectories = np.array(noisy_trajectories)

clean_endpoints = np.array(clean_endpoints)
noisy_endpoints = np.array(noisy_endpoints)

# ============================
# METRICS
# ============================

def compute_spread(points):
    mean = np.mean(points, axis=0)
    distances = np.linalg.norm(points - mean, axis=1)
    return np.mean(distances), np.std(distances)

clean_mean, clean_std = compute_spread(clean_endpoints)
noisy_mean, noisy_std = compute_spread(noisy_endpoints)

# ============================
# PRINT RESULTS
# ============================

print("\n=== NEXAH NOISE VALIDATION ===\n")

print("CLEAN:")
print(f"Mean distance: {clean_mean:.4f}")
print(f"Std: {clean_std:.4f}")

print("\nNOISY:")
print(f"Mean distance: {noisy_mean:.4f}")
print(f"Std: {noisy_std:.4f}")

# qualitative classification
def classify(d):
    if d < 5:
        return "HIGH"
    elif d < 10:
        return "MEDIUM"
    else:
        return "LOW"

print("\nStability:")
print(f"Clean: {classify(clean_mean)}")
print(f"Noisy: {classify(noisy_mean)}")

# ============================
# SAVE SUMMARY
# ============================

summary_path = os.path.join(OUTPUT_DIR, "lorenz_noise_validation.txt")

with open(summary_path, "w") as f:
    f.write("NEXAH — Lorenz Noise Validation\n\n")
    f.write(f"Runs: {N_RUNS}\n")
    f.write(f"Noise level: {NOISE_LEVEL}\n\n")

    f.write("CLEAN\n")
    f.write(f"Mean distance: {clean_mean:.4f}\n")
    f.write(f"Std: {clean_std:.4f}\n\n")

    f.write("NOISY\n")
    f.write(f"Mean distance: {noisy_mean:.4f}\n")
    f.write(f"Std: {noisy_std:.4f}\n")

print(f"\n✅ Saved summary: {summary_path}")

# ============================
# PLOT: TRAJECTORY OVERLAY
# ============================

fig = plt.figure(figsize=(10,5))

ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

for traj in clean_trajectories:
    ax1.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.5)

for traj in noisy_trajectories:
    ax2.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.5)

ax1.set_title("Clean")
ax2.set_title("Noisy")

plot_path = os.path.join(OUTPUT_DIR, "noise_trajectory_comparison.png")
plt.savefig(plot_path, dpi=200)
plt.close()

print(f"✅ Saved: {plot_path}")

# ============================
# PLOT: ENDPOINT COMPARISON
# ============================

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(clean_endpoints[:,0], clean_endpoints[:,1], clean_endpoints[:,2],
           label="clean", alpha=0.7)

ax.scatter(noisy_endpoints[:,0], noisy_endpoints[:,1], noisy_endpoints[:,2],
           label="noisy", alpha=0.7)

ax.legend()
ax.set_title("Endpoint Comparison")

endpoint_path = os.path.join(OUTPUT_DIR, "noise_endpoint_comparison.png")
plt.savefig(endpoint_path, dpi=200)
plt.close()

print(f"✅ Saved: {endpoint_path}")

# ============================
# DONE
# ============================

print("\n✅ Noise validation complete.\n")
