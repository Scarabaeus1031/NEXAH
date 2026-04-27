# ============================================================
# NEXAH — Generate Halvorsen Trajectory (Stable)
# ============================================================

import numpy as np
import os

# ------------------------------------------------------------
# Halvorsen system
# ------------------------------------------------------------
def halvorsen(state, a=1.4):
    x, y, z = state
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return np.array([dx, dy, dz])

# ------------------------------------------------------------
# Simulation (RK4 for stability)
# ------------------------------------------------------------
dt = 0.001
T = 20000

traj = np.zeros((T, 3))
state = np.array([1.0, 0.0, 0.0])

for i in range(T):
    traj[i] = state

    k1 = halvorsen(state)
    k2 = halvorsen(state + 0.5 * dt * k1)
    k3 = halvorsen(state + 0.5 * dt * k2)
    k4 = halvorsen(state + dt * k3)

    state = state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

# remove NaNs if any
traj = traj[np.isfinite(traj).all(axis=1)]

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "..", "data")
os.makedirs(data_path, exist_ok=True)

save_path = os.path.join(data_path, "trajectory.npy")
np.save(save_path, traj)

print(f"[✓] trajectory saved: {save_path}")
