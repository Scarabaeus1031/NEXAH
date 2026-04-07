# nexah_core_model_v8.4.py

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# CONTROLLED LORENZ SYSTEM
# ---------------------------
def lorenz_controlled_step(x1, y1, z1, x2, y2, z2,
                          target=(5, 5, 25),
                          sigma=10, rho=28, beta=8/3,
                          dt=0.01,
                          coupling=0.08,
                          channel_strength=0.12,
                          control_strength=0.15,
                          damping=0.02):

    tx, ty, tz = target

    # --- base dynamics ---
    dx1 = sigma * (y1 - x1)
    dy1 = x1 * (rho - z1) - y1
    dz1 = x1 * y1 - beta * z1

    dx2 = sigma * (y2 - x2)
    dy2 = x2 * (rho - z2) - y2
    dz2 = x2 * y2 - beta * z2

    # ---------------------------
    # COUPLING
    # ---------------------------
    dx1 += coupling * (x2 - x1)
    dy1 += coupling * (y2 - y1)

    dx2 += coupling * (x1 - x2)
    dy2 += coupling * (y1 - y2)

    # ---------------------------
    # CHANNEL COUPLING
    # ---------------------------
    channel = np.exp(-abs(x1 - y1))

    dx1 += channel_strength * channel * (x2 - x1)
    dx2 += channel_strength * channel * (x1 - x2)

    # ---------------------------
    # TARGET STEERING
    # ---------------------------
    dx1 += control_strength * (tx - x1)
    dy1 += control_strength * (ty - y1)
    dz1 += control_strength * (tz - z1)

    dx2 += control_strength * (tx - x2)
    dy2 += control_strength * (ty - y2)
    dz2 += control_strength * (tz - z2)

    # ---------------------------
    # DAMPING (stability)
    # ---------------------------
    dx1 -= damping * x1
    dy1 -= damping * y1

    dx2 -= damping * x2
    dy2 -= damping * y2

    return (
        x1 + dx1 * dt,
        y1 + dy1 * dt,
        z1 + dz1 * dt,
        x2 + dx2 * dt,
        y2 + dy2 * dt,
        z2 + dz2 * dt,
    )

# ---------------------------
# SIMULATION
# ---------------------------
def simulate(n=25000):
    x1, y1, z1 = 0.1, 0.0, 0.0
    x2, y2, z2 = -0.1, 0.0, 0.0

    A = []
    B = []

    for _ in range(n):
        x1, y1, z1, x2, y2, z2 = lorenz_controlled_step(
            x1, y1, z1, x2, y2, z2
        )

        A.append((x1, y1, z1))
        B.append((x2, y2, z2))

    return np.array(A), np.array(B)

# ---------------------------
# HELPERS
# ---------------------------
def classify(x):
    if x < -2:
        return "blue"
    elif x > 2:
        return "red"
    else:
        return "green"

def grey_mask(x, y):
    return np.abs(x - y) < 1.2

def cone_mask(x, y, z):
    r = np.sqrt(x**2 + y**2)
    return (r < 6) & (z > 10) & (z < 30)

# ---------------------------
# RUN
# ---------------------------
A, B = simulate()

x1, y1, z1 = A[:,0], A[:,1], A[:,2]
x2, y2, z2 = B[:,0], B[:,1], B[:,2]

colors = np.array([classify(x) for x in x1])

grey1 = grey_mask(x1, y1)
grey2 = grey_mask(x2, y2)
cone = cone_mask(x1, y1, z1)

# distance to target
target = np.array([5, 5, 25])
dist = np.linalg.norm(A - target, axis=1)

# ---------------------------
# PLOT
# ---------------------------
plt.figure(figsize=(10,8))

# field
plt.scatter(x1[colors=="blue"], y1[colors=="blue"], s=1, label="blue")
plt.scatter(x1[colors=="green"], y1[colors=="green"], s=1, label="green")
plt.scatter(x1[colors=="red"], y1[colors=="red"], s=1, label="red")

# mirror
plt.scatter(x2, y2, s=0.5, alpha=0.2, label="controlled mirror")

# grey channels
plt.scatter(x1[grey1], y1[grey1], s=2, c="black", label="grey A")
plt.scatter(x2[grey2], y2[grey2], s=2, c="gray", label="grey B")

# cone
plt.scatter(x1[cone], y1[cone], s=2, c="yellow", alpha=0.6, label="cone")

# target
plt.scatter(5, 5, c="magenta", s=80, label="target")

# highlight convergence
close = dist < 3
plt.scatter(x1[close], y1[close], s=3, c="cyan", label="target lock")

plt.title("NEXAH v8.4 — Controlled Navigation + Target Lock")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)

plt.show()
