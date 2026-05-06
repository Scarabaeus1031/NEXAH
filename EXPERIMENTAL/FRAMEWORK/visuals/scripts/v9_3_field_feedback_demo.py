import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# 1. Vector field
# ----------------------------
def F(x, y):
    return np.array([
        y + 0.2 * x,
        -x - 0.3*y + 0.05 * np.tanh(x)
    ])

# ----------------------------
# 2. Coherence
# ----------------------------
def coherence(v, f):
    nv = np.linalg.norm(v)
    nf = np.linalg.norm(f)

    if nv < 1e-6 or nf < 1e-6:
        return 1.0

    return np.dot(v, f) / (nv * nf)

# ----------------------------
# 3. Structured Risk
# ----------------------------
def compute_risk(x, c):
    r = np.linalg.norm(x)

    base = np.tanh(r / 2.0)

    fx, fy = F(x[0], x[1])
    curvature = np.abs(fx * fy)
    curvature = np.tanh(curvature)

    coherence_term = (1 - c)

    risk = 0.6 * base + 0.3 * curvature + 0.1 * coherence_term

    return np.clip(risk, 0, 1)

# ----------------------------
# 4. Gradient of Risk (NUMERICAL!)
# ----------------------------
def grad_risk(x, eps=1e-3):
    dx = np.array([eps, 0])
    dy = np.array([0, eps])

    c = 1.0

    r_x1 = compute_risk(x + dx, c)
    r_x2 = compute_risk(x - dx, c)

    r_y1 = compute_risk(x + dy, c)
    r_y2 = compute_risk(x - dy, c)

    dRx = (r_x1 - r_x2) / (2 * eps)
    dRy = (r_y1 - r_y2) / (2 * eps)

    return np.array([dRx, dRy])

# ----------------------------
# 5. Grid Field
# ----------------------------
def compute_field(x_range, y_range, res=120):
    X, Y = np.meshgrid(
        np.linspace(*x_range, res),
        np.linspace(*y_range, res)
    )

    R = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            pos = np.array([X[i, j], Y[i, j]])

            f = F(pos[0], pos[1])
            c = 1.0

            R[i, j] = compute_risk(pos, c)

    return X, Y, R

# ----------------------------
# 6. Simulation (FIELD CONTROL!)
# ----------------------------
dt = 0.05
steps = 300

x = np.array([-2.0, -1.5])

trajectory = []
coherences = []
risks = []

for _ in range(steps):
    trajectory.append(x.copy())

    f = F(x[0], x[1])

    noise = np.random.normal(0, 0.15, size=2)
    v = f + noise

    c = coherence(v, f)
    r = compute_risk(x, c)

    coherences.append(c)
    risks.append(r)

    # 🔥 CORE IDEA: control from field gradient
    grad = grad_risk(x)

    u = -0.8 * grad   # ← tuning parameter

    x = x + dt * (v + u)

    # safety
    if np.linalg.norm(x) > 5:
        x = x / np.linalg.norm(x) * 5

trajectory = np.array(trajectory)
coherences = np.array(coherences)
risks = np.array(risks)

# ----------------------------
# 7. Field
# ----------------------------
X, Y, R = compute_field((-3, 3), (-3, 3))

# ----------------------------
# 8. Plot
# ----------------------------
fig, ax = plt.subplots()

im = ax.contourf(X, Y, R, levels=50, cmap="plasma")

# boundaries
ax.contour(X, Y, R, levels=[0.3], colors="white", linewidths=2)
ax.contour(X, Y, R, levels=[0.6], colors="red", linewidths=2)

# trajectory (colored by risk now 🔥)
for i in range(len(trajectory) - 1):
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        color=plt.cm.inferno(risks[i])
    )

ax.scatter(trajectory[0, 0], trajectory[0, 1], color="cyan", label="start")

ax.set_title("NEXAH V9.3: Field-Driven Control (u = -∇R)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal')

# colorbars
cbar1 = fig.colorbar(im, ax=ax)
cbar1.set_label("Risk Field")

sm = plt.cm.ScalarMappable(cmap='inferno')
sm.set_array(risks)
cbar2 = fig.colorbar(sm, ax=ax)
cbar2.set_label("Trajectory Risk")

ax.legend()

# save
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

path = os.path.join(output_dir, "v9_3_field_control.png")
plt.savefig(path)
print("Saved:", path)

plt.close()
