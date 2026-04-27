import numpy as np
import os

# =========================
# LORENZ SYSTEM
# =========================

def lorenz(state, sigma=10.0, rho=28.0, beta=8/3):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([dx, dy, dz])

# =========================
# INTEGRATION
# =========================

dt = 0.01
T = 5000

traj = np.zeros((T, 3))
state = np.array([1.0, 1.0, 1.0])

for i in range(T):
    traj[i] = state
    state = state + dt * lorenz(state)

# =========================
# SAVE
# =========================

base = os.path.dirname(__file__)
data_path = os.path.join(base, "../data")

os.makedirs(data_path, exist_ok=True)

out_path = os.path.join(data_path, "trajectory_lorenz.npy")
np.save(out_path, traj)

print(f"[✓] Lorenz trajectory saved: {out_path}")
