import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------
# 1. Vector field (leicht asymmetrisch!)
# ----------------------------
def F(x, y):
    return np.array([
        y + 0.2 * x,
        -x - 0.3*y + 0.1 * x**2
    ])


# ----------------------------
# 2. Coherence
# ----------------------------
def coherence(v, f):
    denom = np.linalg.norm(v) * np.linalg.norm(f)
    if denom < 1e-8:
        return 1.0
    return np.dot(v, f) / denom


# ----------------------------
# 3. Risk Field
# ----------------------------
def compute_risk_field(x_range, y_range, resolution=120):
    X, Y = np.meshgrid(
        np.linspace(*x_range, resolution),
        np.linspace(*y_range, resolution)
    )

    R = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            f = F(X[i, j], Y[i, j])
            R[i, j] = np.linalg.norm(f)

    R = R / np.max(R)

    return X, Y, R


# ----------------------------
# 4. Simulation
# ----------------------------
dt = 0.05
steps = 250

x = np.array([-2.0, -1.5])
trajectory = []
coherences = []

for _ in range(steps):
    trajectory.append(x.copy())

    field = F(x[0], x[1])

    noise = np.random.normal(0, 0.35, size=2)
    velocity = field + noise

    c = coherence(velocity, field)
    coherences.append(c)

    # 🔥 smarter control
    if c < 0.2:
        u = np.array([0.0, 1.0])  # starke Korrektur
    elif c < 0.5:
        u = np.array([0.0, 0.4])  # leichte Korrektur
    else:
        u = np.array([0.0, 0.0])

    x = x + dt * (velocity + u)

trajectory = np.array(trajectory)
coherences = np.array(coherences)

# ----------------------------
# 5. Risk Field
# ----------------------------
x_range = (-3, 3)
y_range = (-3, 3)

X, Y, R = compute_risk_field(x_range, y_range)

# 🔥 MULTI THRESHOLDS
tau1 = 0.4   # stable
tau2 = 0.7   # collapse

# ----------------------------
# 6. Output folder
# ----------------------------
output_dir = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(output_dir, exist_ok=True)

# ----------------------------
# 7. Plot
# ----------------------------
fig, ax = plt.subplots()

# Base heatmap
im = ax.contourf(X, Y, R, levels=50, cmap="plasma")

# 🔥 Stable basin
ax.contourf(X, Y, R < tau1, levels=[0.5, 1], colors=["#00ff0033"])

# 🔥 Transition zone
ax.contourf(X, Y, (R >= tau1) & (R < tau2), levels=[0.5, 1], colors=["#ffff0033"])

# 🔥 Collapse basin
ax.contourf(X, Y, R >= tau2, levels=[0.5, 1], colors=["#ff000033"])

# 🔥 Separatrices
ax.contour(X, Y, R, levels=[tau1], colors="white", linewidths=2)
ax.contour(X, Y, R, levels=[tau2], colors="red", linewidths=2)

# Trajectory colored by coherence
for i in range(len(trajectory) - 1):
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        color=plt.cm.viridis(coherences[i])
    )

# Start point
ax.scatter(trajectory[0, 0], trajectory[0, 1], color="red", label="start")

# Labels
ax.set_title("NEXAH V8: Multi-Regime Field (Stable / Transition / Collapse)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal', adjustable='box')

# Colorbars
cbar1 = fig.colorbar(im, ax=ax)
cbar1.set_label("Risk Field")

sm = plt.cm.ScalarMappable(cmap='viridis')
sm.set_array(coherences)
cbar2 = fig.colorbar(sm, ax=ax)
cbar2.set_label("Coherence")

ax.legend()

# Save
path = os.path.join(output_dir, "v8_multi_regime.png")
plt.savefig(path)
print("Saved:", path)

plt.close()
