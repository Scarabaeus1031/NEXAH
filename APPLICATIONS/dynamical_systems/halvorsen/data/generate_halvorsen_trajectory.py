import numpy as np

# Halvorsen system
def halvorsen(state, a=1.4):
    x, y, z = state
    dx = -a*x - 4*y - 4*z - y*y
    dy = -a*y - 4*z - 4*x - z*z
    dz = -a*z - 4*x - 4*y - x*x
    return np.array([dx, dy, dz])

# integrate
dt = 0.01
T = 5000

traj = np.zeros((T, 3))
state = np.array([1.0, 0.0, 0.0])

for i in range(T):
    traj[i] = state
    state = state + dt * halvorsen(state)

# save
np.save("APPLICATIONS/dynamical_systems/halvorsen/data/trajectory.npy", traj)

print("✓ trajectory saved")
