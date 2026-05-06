import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# 1. Vector field (stable + nonlinear)
# ----------------------------
def F(x, y):
    return np.array([
        y + 0.2 * x,
        -x - 0.3*y + 0.05 * np.tanh(x)
    ])

# ----------------------------
# 2. Coherence (safe)
# ----------------------------
def coherence(v, f):
    nv = np.linalg.norm(v)
    nf = np.linalg.norm(f)

    if nv < 1e-6 or nf < 1e-6:
        return 1.0

    return np.dot(v, f) / (nv * nf)

# ----------------------------
# 3. Regime classification (ARCHY)
# ----------------------------
def classify_regime(x):
    r = np.linalg.norm(x)

    if r < 1.2:
        return "stable"
    elif r < 2.2:
        return "transition"
    else:
        return "collapse"

# ----------------------------
# 4. NEW: Structured Risk Field (MESO)
# ----------------------------
def compute_risk(x, c):
    r = np.linalg.norm(x)

    # 🔥 1. radial structure
    base = np.tanh(r / 2.0)

    # 🔥 2. field curvature / instability
    fx, fy = F(x[0], x[1])
    curvature = np.abs(fx * fy)
    curvature = np.tanh(curvature)

    # 🔥 3. coherence contribution (small weight)
    coherence_term = (1 - c)

    # 🔥 4. combine
    risk = 0.6 * base + 0.3 * curvature + 0.1 * coherence_term

    return np.clip(risk, 0, 1)

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
            c = 1.0  # baseline

            R[i, j] = compute_risk(pos, c)

    return X, Y, R

# ----------------------------
# 6. Simulation
# ----------------------------
dt = 0.05
steps = 300

x = np.array([-2.0, -1.5])

trajectory = []
coherences = []

for _ in range(steps):
    trajectory.append(x.copy())

    f = F(x[0], x[1])

    noise = np.random.normal(0, 0.2, size=2)
    v = f + noise

    c = coherence(v, f)
    coherences.append(c)

    regime = classify_regime(x)

    # 🔥 regime-aware control
    if regime == "collapse":
        u = np.array([0.0, 1.0])
    elif regime == "transition":
        u = np.array([0.0, 0.4])
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (v + u)

    # safety clip
    if np.linalg.norm(x) > 5:
        x = x / np.linalg.norm(x) * 5

trajectory = np.array(trajectory)
coherences = np.array(coherences)

# ----------------------------
# 7. Field
# ----------------------------
X, Y, R = compute_field((-3, 3), (-3, 3))

# ----------------------------
# 8. Plot
# ----------------------------
fig, ax = plt.subplots()

im = ax.contourf(X, Y, R, levels=50, cmap="plasma")

# 🔥 meaningful boundaries
ax.contour(X, Y, R, levels=[0.3], colors="white", linewidths=2)
ax.contour(X, Y, R, levels=[0.6], colors="red", linewidths=2)

# trajectory colored by coherence
for i in range(len(trajectory) - 1):
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        color=plt.cm.viridis(coherences[i])
    )

# start point
ax.scatter(trajectory[0, 0], trajectory[0, 1], color="red", label="start")

# layout
ax.set_title("NEXAH V9.2: Structured Risk Field")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal')

# colorbars
cbar1 = fig.colorbar(im, ax=ax)
cbar1.set_label("Risk Field")

sm = plt.cm.ScalarMappable(cmap='viridis')
sm.set_array(coherences)
cbar2 = fig.colorbar(sm, ax=ax)
cbar2.set_label("Coherence")

ax.legend()

# save
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

path = os.path.join(output_dir, "v9_2_structured_risk.png")
plt.savefig(path)
print("Saved:", path)

plt.close()
