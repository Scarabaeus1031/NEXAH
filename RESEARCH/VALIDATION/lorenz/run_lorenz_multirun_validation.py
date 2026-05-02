"""
NEXAH — Lorenz Multi-Run Validation

Goal:
Check if structure (attractor + trajectories) is reproducible across runs.
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

def simulate(seed):
    np.random.seed(seed)
    x = np.random.randn(3)

    traj = []

    for _ in range(STEPS):
        dx = lorenz(x)
        x = x + DT * dx
        traj.append(x.copy())

    return np.array(traj)

# ============================
# RUN MULTIPLE
# ============================

trajectories = []
endpoints = []

for i in range(N_RUNS):
    traj = simulate(seed=i)
    trajectories.append(traj)
    endpoints.append(traj[-1])

trajectories = np.array(trajectories)
endpoints = np.array(endpoints)

# ============================
# METRICS
# ============================

mean_endpoint = np.mean(endpoints, axis=0)
distances = np.linalg.norm(endpoints - mean_endpoint, axis=1)

mean_dist = np.mean(distances)
std_dist = np.std(distances)

# ============================
# PRINT RESULTS
# ============================

print("\n=== NEXAH VALIDATION RESULT ===\n")

print(f"Runs: {N_RUNS}")
print(f"Mean endpoint distance: {mean_dist:.4f}")
print(f"Std endpoint distance: {std_dist:.4f}")

if mean_dist < 5:
    stability = "HIGH"
elif mean_dist < 10:
    stability = "MEDIUM"
else:
    stability = "LOW"

print(f"Attractor stability: {stability}")

# ============================
# SAVE TEXT SUMMARY
# ============================

summary_path = os.path.join(OUTPUT_DIR, "lorenz_multirun_summary.txt")

with open(summary_path, "w") as f:
    f.write("NEXAH — Lorenz Multi-Run Validation\n\n")
    f.write(f"Runs: {N_RUNS}\n")
    f.write(f"Mean endpoint distance: {mean_dist:.4f}\n")
    f.write(f"Std endpoint distance: {std_dist:.4f}\n")
    f.write(f"Attractor stability: {stability}\n")

print(f"\n✅ Saved summary: {summary_path}")

# ============================
# PLOT: TRAJECTORY OVERLAY
# ============================

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

for traj in trajectories:
    ax.plot(traj[:,0], traj[:,1], traj[:,2], alpha=0.5)

ax.set_title("Lorenz Multi-Run Trajectories")

traj_path = os.path.join(OUTPUT_DIR, "trajectory_overlay.png")
plt.savefig(traj_path, dpi=200)
plt.close()

print(f"✅ Saved: {traj_path}")

# ============================
# PLOT: ENDPOINT SCATTER
# ============================

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(endpoints[:,0], endpoints[:,1], endpoints[:,2], s=50)
ax.scatter(*mean_endpoint, color='red', s=100, label='mean')

ax.set_title("Endpoint Distribution")
ax.legend()

endpoint_path = os.path.join(OUTPUT_DIR, "endpoint_distribution.png")
plt.savefig(endpoint_path, dpi=200)
plt.close()

print(f"✅ Saved: {endpoint_path}")

# ============================
# DONE
# ============================

print("\n✅ Validation complete.\n")
