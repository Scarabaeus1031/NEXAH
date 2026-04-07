# ============================================================
# NEXAH v7.0 — Attractor & Basin Detection
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# FIELD (replace with your real system if needed)
# ------------------------------------------------------------
def field(x, y):
    U = y - x*(x**2 + y**2 - 1)
    V = -x - y*(x**2 + y**2 - 1)
    return U, V


# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
N = 80
xs = np.linspace(-1.5, 1.5, N)
ys = np.linspace(-1.5, 1.5, N)

X, Y = np.meshgrid(xs, ys)


# ------------------------------------------------------------
# SIMULATION FUNCTION
# ------------------------------------------------------------
def simulate(x0, y0, steps=200, dt=0.05):
    x, y = x0, y0
    traj = []

    for _ in range(steps):
        U, V = field(x, y)
        x += dt * U
        y += dt * V
        traj.append((x, y))

    return np.array(traj)


# ------------------------------------------------------------
# ATTRACTOR DETECTION
# ------------------------------------------------------------
def detect_attractor(traj):
    """
    classify endpoint behavior
    """
    tail = traj[-50:]

    # center of tail
    cx = np.mean(tail[:, 0])
    cy = np.mean(tail[:, 1])

    # spread
    spread = np.std(tail[:, 0]) + np.std(tail[:, 1])

    if spread < 0.01:
        return ("fixed", cx, cy)
    elif spread < 0.1:
        return ("cycle", cx, cy)
    else:
        return ("chaotic", cx, cy)


# ------------------------------------------------------------
# BASIN COMPUTATION
# ------------------------------------------------------------
basin_map = np.zeros((N, N))

attractors = []
labels = {}

label_counter = 1


for i in range(N):
    for j in range(N):

        x0 = X[i, j]
        y0 = Y[i, j]

        traj = simulate(x0, y0)

        kind, cx, cy = detect_attractor(traj)

        key = (round(cx, 2), round(cy, 2), kind)

        if key not in labels:
            labels[key] = label_counter
            attractors.append((cx, cy, kind))
            label_counter += 1

        basin_map[i, j] = labels[key]


# ------------------------------------------------------------
# PLOT BASINS
# ------------------------------------------------------------
plt.figure(figsize=(8, 7))

plt.imshow(
    basin_map,
    extent=[xs.min(), xs.max(), ys.min(), ys.max()],
    origin='lower'
)

plt.title("NEXAH v7.0 — Basin Map")
plt.xlabel("X")
plt.ylabel("Y")
plt.colorbar(label="Attractor ID")


# ------------------------------------------------------------
# PLOT ATTRACTORS
# ------------------------------------------------------------
for (cx, cy, kind) in attractors:
    if kind == "fixed":
        plt.scatter(cx, cy, color='red', s=80, label='fixed')
    elif kind == "cycle":
        plt.scatter(cx, cy, color='blue', s=80, label='cycle')
    else:
        plt.scatter(cx, cy, color='black', s=60, label='chaotic')


plt.grid(True)
plt.show()


# ------------------------------------------------------------
# PRINT RESULTS
# ------------------------------------------------------------
print("\n=== Attractors detected ===")
for a in attractors:
    print(a)
