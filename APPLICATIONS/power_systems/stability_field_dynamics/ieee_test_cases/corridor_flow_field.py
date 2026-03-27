```python
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA (from pipeline if available)
# ----------------------------
try:
    from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.phase_data_pipeline import (
        theta_values,
        c_values,
        loop_values,
        gh_mask
    )
    print("Loaded pipeline data")

except Exception:
    print("Fallback random data")

    n = 200
    theta_values = np.random.uniform(0, 2*np.pi, n)
    c_values = np.random.uniform(0.005, 0.035, n)
    loop_values = np.random.randint(0, 7, n)

    gh_mask = (c_values > 0.015) & (c_values < 0.03) & (loop_values > 1) & (loop_values < 4)

# ----------------------------
# FLOW FIELD DEFINITION
# ----------------------------

def flow(theta, c, loops):
    """
    Simple GH corridor flow model:
    - theta drift dominates (transport)
    - weak radial correction
    """

    dtheta = 0.4 + 0.2 * np.sin(theta)      # directional flow
    dc = -0.1 * (c - 0.02)                  # weak attraction band
    dloops = -0.05 * (loops - 3)            # weak stabilization

    return dtheta, dc, dloops


# ----------------------------
# INIT PARTICLES IN GH CORRIDOR
# ----------------------------

gh_theta = theta_values[gh_mask]
gh_c = c_values[gh_mask]
gh_loops = loop_values[gh_mask]

num_particles = len(gh_theta)

theta = gh_theta.copy()
c = gh_c.copy()
loops = gh_loops.copy()

# ----------------------------
# TRAJECTORY STORAGE
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

# ---- Polar Trajectories ----
plt.subplot(1, 2, 1, projection="polar")
for i in range(num_particles):
    plt.plot(theta_traj[i], c_traj[i], alpha=0.3)

plt.title("GH Corridor Flow (Polar)")

# ---- Phase Space ----
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

theta_dispersion = np.std(theta_traj[:, -1])
c_dispersion = np.std(c_traj[:, -1])

print("\n--- FLOW METRICS ---")
print(f"Final theta spread: {theta_dispersion:.3f}")
print(f"Final C spread    : {c_dispersion:.3f}")
```
