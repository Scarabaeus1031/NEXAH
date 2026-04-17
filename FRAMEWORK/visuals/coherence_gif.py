import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# 1. Vector field (STABLE!)
# ----------------------------
def F(x, y):
    return np.array([y, -x - 0.3*y])  # damped spiral → attractor

# ----------------------------
# 2. Grid for field
# ----------------------------
x_vals = np.linspace(-3, 3, 25)
y_vals = np.linspace(-3, 3, 25)
X, Y = np.meshgrid(x_vals, y_vals)

U = np.zeros_like(X)
V = np.zeros_like(Y)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = F(X[i, j], Y[i, j])
        U[i, j], V[i, j] = vec

# ----------------------------
# 3. Simulate trajectory
# ----------------------------
dt = 0.05
steps = 200
trajectory = []

x = np.array([-2.0, -1.5])  # Startpunkt

for _ in range(steps):
    trajectory.append(x.copy())

    dx = F(x[0], x[1])

    # simple control (push upward near center)
    if np.linalg.norm(x) < 1.2:
        u = np.array([0.0, 0.5])
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (dx + u)

trajectory = np.array(trajectory)

# ----------------------------
# 4. Plot
# ----------------------------
plt.figure()

# Field
plt.streamplot(X, Y, U, V)

# Trajectory
plt.plot(trajectory[:,0], trajectory[:,1], label="trajectory")

# Startpunkt
plt.scatter(trajectory[0,0], trajectory[0,1], label="start")

# Fix axes (WICHTIG!)
plt.xlim(-3, 3)
plt.ylim(-3, 3)

plt.title("NEXAH Mini Simulation: Field + Trajectory")
plt.xlabel("State Dimension X")
plt.ylabel("State Dimension Y")
plt.legend()

plt.show()
