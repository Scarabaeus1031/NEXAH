import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v7.3 — Stability Navigation / Control
# ============================================================

# ------------------------------------------------------------
# FIELD
# ------------------------------------------------------------
def field(x, y):
    r = np.sqrt(x**2 + y**2) + 1e-9

    fx = x * (1 - r)
    fy = y * (1 - r)

    fx += -0.5 * y
    fy +=  0.5 * x

    return fx, fy


# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def simulate(x0, y0, steps=200, dt=0.05):
    x, y = x0, y0
    traj = []

    for _ in range(steps):
        fx, fy = field(x, y)
        x += fx * dt
        y += fy * dt
        traj.append((x, y))

    return np.array(traj)


# ------------------------------------------------------------
# INSTABILITY (same as v7.2)
# ------------------------------------------------------------
def instability(x, y, eps=1e-4):
    traj1 = simulate(x, y, steps=150)
    traj2 = simulate(x + eps, y + eps, steps=150)

    d0 = np.sqrt(eps**2 + eps**2)
    d1 = np.linalg.norm(traj1[-1] - traj2[-1])

    return np.log((d1 + 1e-12) / d0)


# ------------------------------------------------------------
# GRADIENT OF INSTABILITY (numerical)
# ------------------------------------------------------------
def instability_gradient(x, y, h=1e-3):
    f0 = instability(x, y)

    fx = instability(x + h, y)
    fy = instability(x, y + h)

    dfdx = (fx - f0) / h
    dfdy = (fy - f0) / h

    return np.array([dfdx, dfdy])


# ------------------------------------------------------------
# NAVIGATION STEP
# ------------------------------------------------------------
def navigate_to_stability(x0, y0, steps=50, lr=0.05):
    x, y = x0, y0
    path = [(x, y)]

    for _ in range(steps):
        grad = instability_gradient(x, y)

        # move AGAINST instability gradient
        x -= lr * grad[0]
        y -= lr * grad[1]

        path.append((x, y))

    return np.array(path)


# ------------------------------------------------------------
# GRID FOR BACKGROUND MAP
# ------------------------------------------------------------
N = 80
x_vals = np.linspace(-1.5, 1.5, N)
y_vals = np.linspace(-1.5, 1.5, N)

stability_map = np.zeros((N, N))

for i, x in enumerate(x_vals):
    for j, y in enumerate(y_vals):
        stability_map[j, i] = instability(x, y)


# ------------------------------------------------------------
# TEST NAVIGATION FROM MULTIPLE START POINTS
# ------------------------------------------------------------
start_points = [
    (0.0, 0.0),        # center (chaotic)
    (0.2, 0.0),
    (0.0, 0.2),
    (-0.5, 0.5),
    (0.8, -0.3),
]

nav_paths = []
for pt in start_points:
    nav_paths.append(navigate_to_stability(pt[0], pt[1], steps=60, lr=0.03))


# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
plt.figure(figsize=(8, 8))

plt.imshow(stability_map, cmap="coolwarm", origin="lower")
plt.colorbar(label="instability")

# overlay navigation paths
for path in nav_paths:
    xs = (path[:, 0] - x_vals.min()) / (x_vals.max() - x_vals.min()) * (N - 1)
    ys = (path[:, 1] - y_vals.min()) / (y_vals.max() - y_vals.min()) * (N - 1)

    plt.plot(xs, ys, linewidth=2)

plt.title("NEXAH v7.3 — Stability Navigation")
plt.show()
