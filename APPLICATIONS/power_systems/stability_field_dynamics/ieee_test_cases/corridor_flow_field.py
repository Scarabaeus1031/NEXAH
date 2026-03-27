import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# LOAD DATA
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
# FLOW FIELD
# ----------------------------

def flow(theta, c, loops):
    dtheta = 0.4 + 0.2 * np.sin(theta)
    dc = -0.1 * (c - 0.02)
    dloops = -0.05 * (loops - 3)
    return dtheta, dc, dloops

# ----------------------------
# INIT PARTICLES
# ----------------------------

theta = theta_values[gh_mask].copy()
c = c_values[gh_mask].copy()
loops = loop_values[gh_mask].copy()

num_particles = len(theta)

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
