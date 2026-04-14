import numpy as np
import matplotlib.pyplot as plt

# =========================
# GRID SETUP
# =========================
N = 80
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)

# =========================
# CORE FIELD DEFINITIONS
# =========================

def instability_measure(x, y):
    r = np.sqrt(x**2 + y**2) + 1e-9
    return np.log(r) + 0.3 * np.sin(3*x) * np.cos(3*y)

def instability_gradient(x, y, eps=1e-4):
    dx = (instability_measure(x + eps, y) - instability_measure(x - eps, y)) / (2 * eps)
    dy = (instability_measure(x, y + eps) - instability_measure(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def flow_field(x, y):
    r = np.sqrt(x**2 + y**2) + 1e-9
    fx = -y / r + 0.5 * x
    fy =  x / r + 0.5 * y
    return np.array([fx, fy])

# =========================
# ENERGY LAYER (NEW)
# =========================

def current_field(x, y):
    grad = instability_gradient(x, y)
    return np.linalg.norm(grad)

def pressure_field(x, y):
    grad = instability_gradient(x, y)
    return grad[0]**2 + grad[1]**2

def power_field(x, y):
    U = instability_measure(x, y)
    I = current_field(x, y)
    return U * I

# =========================
# COMPUTE MAPS
# =========================

U_map = np.zeros_like(X)
I_map = np.zeros_like(X)
P_map = np.zeros_like(X)
Pressure_map = np.zeros_like(X)

for i in range(N):
    for j in range(N):
        xi, yi = X[i, j], Y[i, j]

        U_map[i, j] = instability_measure(xi, yi)
        I_map[i, j] = current_field(xi, yi)
        P_map[i, j] = power_field(xi, yi)
        Pressure_map[i, j] = pressure_field(xi, yi)

# =========================
# TRAJECTORY SIMULATION
# =========================

def simulate_trajectory(x0, y0, steps=300, dt=0.03):
    x, y = x0, y0
    traj = []

    for _ in range(steps):
        grad = instability_gradient(x, y)
        flow = flow_field(x, y)

        dx = -0.8 * grad[0] + 0.6 * flow[0]
        dy = -0.8 * grad[1] + 0.6 * flow[1]

        x += dx * dt
        y += dy * dt

        if not np.isfinite(x) or not np.isfinite(y):
            break

        traj.append((x, y))

    return np.array(traj)

# Generate multiple trajectories
trajectories = []
starts = [(-1, -1), (1, 1), (-1, 1), (1, -1), (0.5, 0), (0, -0.8)]

for sx, sy in starts:
    trajectories.append(simulate_trajectory(sx, sy))

# =========================
# VISUALIZATION
# =========================

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Voltage / Instability
im0 = axs[0, 0].imshow(U_map, origin='lower', extent=[-1.5,1.5,-1.5,1.5])
axs[0, 0].set_title("Voltage / Instability (U)")
plt.colorbar(im0, ax=axs[0, 0])

# Current
im1 = axs[0, 1].imshow(I_map, origin='lower', extent=[-1.5,1.5,-1.5,1.5])
axs[0, 1].set_title("Current (I)")
plt.colorbar(im1, ax=axs[0, 1])

# Power
im2 = axs[1, 0].imshow(P_map, origin='lower', extent=[-1.5,1.5,-1.5,1.5])
axs[1, 0].set_title("Power (P = U * I)")
plt.colorbar(im2, ax=axs[1, 0])

# Pressure
im3 = axs[1, 1].imshow(Pressure_map, origin='lower', extent=[-1.5,1.5,-1.5,1.5])
axs[1, 1].set_title("Pressure / Gradient Energy")
plt.colorbar(im3, ax=axs[1, 1])

plt.tight_layout()
plt.show()

# =========================
# TRAJECTORY OVERLAY
# =========================

plt.figure(figsize=(6,6))
plt.imshow(U_map, origin='lower', extent=[-1.5,1.5,-1.5,1.5], cmap='coolwarm')

for traj in trajectories:
    if len(traj) > 0:
        plt.plot(traj[:,0], traj[:,1], linewidth=2)

plt.title("Trajectory Navigation over Stability Field")
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)
plt.colorbar(label="Instability")
plt.show()

# =========================
# SUMMARY
# =========================

print("\n=== NEXAH v7.3b Summary ===")
print("U min/max:", np.min(U_map), np.max(U_map))
print("I min/max:", np.min(I_map), np.max(I_map))
print("P min/max:", np.min(P_map), np.max(P_map))
print("Pressure min/max:", np.min(Pressure_map), np.max(Pressure_map))
