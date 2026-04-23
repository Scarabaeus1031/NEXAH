import numpy as np
import matplotlib.pyplot as plt
import os

print("⚡ NEXAH Adaptive Control Navigation")

# --------------------------------------------------
# Output Path (robust!)
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../outputs/demo"))
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------
# 1. Synthetic Field (stable demo)
# --------------------------------------------------

def flow_field(x, y):
    # nonlinear swirl field (like your previous ones)
    dx = y - x * (x**2 + y**2)
    dy = -x - y * (x**2 + y**2)
    return np.array([dx, dy])

def boundary_field(x, y):
    # high near edges / unstable zones
    return np.exp((x**2 + y**2))

def target_field(x, y, tx, ty):
    return np.array([tx - x, ty - y])


# --------------------------------------------------
# 2. Adaptive Control Step
# --------------------------------------------------

def control_step(pos, target):

    x, y = pos

    flow = flow_field(x, y)
    target_vec = target_field(x, y, target[0], target[1])

    # normalize
    flow_norm = flow / (np.linalg.norm(flow) + 1e-8)
    target_norm = target_vec / (np.linalg.norm(target_vec) + 1e-8)

    # boundary penalty
    b = boundary_field(x, y)

    # adaptive weights
    w_flow = 0.6
    w_target = 0.6

    # near boundary → reduce aggressive movement
    w_boundary = min(1.5, b * 0.2)

    direction = (
        w_flow * flow_norm +
        w_target * target_norm -
        w_boundary * np.array([x, y]) * 0.05
    )

    return direction


# --------------------------------------------------
# 3. Trajectory Simulation
# --------------------------------------------------

start = np.array([-1.5, 0.5])
target = np.array([1.5, 0.5])

trajectory = [start.copy()]

pos = start.copy()

for i in range(600):

    d = control_step(pos, target)

    pos = pos + 0.03 * d
    trajectory.append(pos.copy())

trajectory = np.array(trajectory)


# --------------------------------------------------
# 4. Plot Field + Trajectory
# --------------------------------------------------

x = np.linspace(-2, 2, 60)
y = np.linspace(-2, 2, 60)

X, Y = np.meshgrid(x, y)

U = np.zeros_like(X)
V = np.zeros_like(Y)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = flow_field(X[i, j], Y[i, j])
        U[i, j] = vec[0]
        V[i, j] = vec[1]

plt.figure(figsize=(8, 8))

# Flow field
plt.streamplot(X, Y, U, V, density=1.2)

# Trajectory
plt.plot(trajectory[:, 0], trajectory[:, 1], color="red", linewidth=2)

# Start & Target
plt.scatter(start[0], start[1], color="green", s=100, label="Start")
plt.scatter(target[0], target[1], color="blue", s=100, label="Target")

plt.legend()
plt.title("NEXAH Adaptive Control Navigation")

out_path = os.path.join(OUT_DIR, "nexah_adaptive_control.png")
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

# --------------------------------------------------
# 5. Interpretation
# --------------------------------------------------

print("\n🧠 Interpretation:\n")
print("Red path = controlled trajectory")
print("→ balances flow + target + boundary avoidance")
print("→ avoids unstable outer regions")
print("→ follows natural field curvature\n")
