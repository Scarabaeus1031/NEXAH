import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
# ----------------------------
try:
    from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.phase_data_pipeline import get_phase_data
    theta_values, c_values, loop_values, gh_mask = get_phase_data()
    print("Loaded pipeline data")

except Exception:
    print("Fallback random data")

    n = 200
    theta_values = np.random.uniform(0, 2*np.pi, n)
    c_values = np.random.uniform(0.005, 0.035, n)
    loop_values = np.random.randint(0, 7, n)

    gh_mask = (c_values > 0.015) & (c_values < 0.03) & (loop_values > 1) & (loop_values < 4)

# ----------------------------
# FLOW FIELD
# ----------------------------

def flow(theta, c, loops):
    dtheta = 0.4 + 0.2 * np.sin(theta)
    dc = -0.1 * (c - 0.02)
    dloops = -0.05 * (loops - 3)
    return dtheta, dc, dloops

# ----------------------------
# INIT PARTICLES (GH CORRIDOR)
# ----------------------------

theta = theta_values[gh_mask].copy()
c = c_values[gh_mask].copy()
loops = loop_values[gh_mask].copy()

num_particles = len(theta)

if num_particles == 0:
    print("⚠️ No GH corridor points found!")
    exit()

# ----------------------------
# STORAGE
# ----------------------------

steps = 50
theta_traj = np.zeros((num_particles, steps))
c_traj = np.zeros((num_particles, steps))

# ----------------------------
# SIMULATION
# ----------------------------

for t in range(steps):
    theta_traj[:, t] = theta
    c_traj[:, t] = c

    dtheta, dc, dloops = flow(theta, c, loops)

    theta = (theta + dtheta) % (2*np.pi)
    c = np.clip(c + dc, 0, 1)
    loops = np.clip(loops + dloops, 0, 10)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(12, 5))

# Polar Plot
plt.subplot(1, 2, 1, projection="polar")
for i in range(num_particles):
    plt.plot(theta_traj[i], c_traj[i], alpha=0.3)
plt.title("GH Corridor Flow (Polar)")

# Phase Plot
plt.subplot(1, 2, 2)
for i in range(num_particles):
    plt.plot(c_traj[i], theta_traj[i], alpha=0.3)

plt.xlabel("C")
plt.ylabel("theta")
plt.title("Phase Trajectories")

plt.tight_layout()
plt.show()

# ----------------------------
# METRICS
# ----------------------------

print("\n--- FLOW METRICS ---")
print(f"Particles: {num_particles}")
print(f"Final theta spread: {np.std(theta_traj[:, -1]):.3f}")
print(f"Final C spread    : {np.std(c_traj[:, -1]):.6f}")
