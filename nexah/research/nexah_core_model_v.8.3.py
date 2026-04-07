# nexah_core_model_v8.3.py

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# LORENZ SYSTEM (COUPLED)
# ---------------------------
def lorenz_coupled_step(x1, y1, z1, x2, y2, z2,
                        sigma=10, rho=28, beta=8/3,
                        dt=0.01,
                        coupling=0.08,
                        channel_strength=0.12):

    # --- base Lorenz dynamics ---
    dx1 = sigma * (y1 - x1)
    dy1 = x1 * (rho - z1) - y1
    dz1 = x1 * y1 - beta * z1

    dx2 = sigma * (y2 - x2)
    dy2 = x2 * (rho - z2) - y2
    dz2 = x2 * y2 - beta * z2

    # ---------------------------
    # COUPLING TERM
    # ---------------------------

    # direct coupling
    dx1 += coupling * (x2 - x1)
    dy1 += coupling * (y2 - y1)

    dx2 += coupling * (x1 - x2)
    dy2 += coupling * (y1 - y2)

    # ---------------------------
    # CHANNEL COUPLING (grey line)
    # ---------------------------
    channel = np.exp(-abs(x1 - y1))  # stronger near channel

    dx1 += channel_strength * channel * (x2 - x1)
    dx2 += channel_strength * channel * (x1 - x2)

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
    x2, y2, z2 = -0.1, 0.0, 0.0  # mirror initial

    A = []
    B = []

    for _ in range(n):
        x1, y1, z1, x2, y2, z2 = lorenz_coupled_step(
            x1, y1, z1, x2, y2, z2
        )

        A.append((x1, y1, z1))
        B.append((x2, y2, z2))

    A = np.array(A)
    B = np.array(B)

    return A, B

# ---------------------------
# CLASSIFICATION
# ---------------------------
def classify(x):
    if x < -2:
        return "blue"
    elif x > 2:
        return "red"
    else:
        return "green"

# ---------------------------
# GREY CHANNEL
# ---------------------------
def grey_mask(x, y, threshold=1.2):
    return np.abs(x - y) < threshold

# ---------------------------
# CONE
# ---------------------------
def cone_mask(x, y, z):
    r = np.sqrt(x**2 + y**2)
    return (r < 6) & (z > 10) & (z < 30)

# ---------------------------
# RUN
# ---------------------------
A, B = simulate()

x1, y1, z1 = A[:,0], A[:,1], A[:,2]
x2, y2, z2 = B[:,0], B[:,1], B[:,2]

# classify
colors = np.array([classify(x) for x in x1])

# masks
grey1 = grey_mask(x1, y1)
grey2 = grey_mask(x2, y2)

cone = cone_mask(x1, y1, z1)

# ---------------------------
# PHASE LOCK DETECTION
# ---------------------------
phase_diff = np.abs(x1 - x2)
locked = phase_diff < 1.0

# ---------------------------
# PLOT
# ---------------------------
plt.figure(figsize=(10,8))

# main field
plt.scatter(x1[colors=="blue"], y1[colors=="blue"], s=1, label="blue")
plt.scatter(x1[colors=="green"], y1[colors=="green"], s=1, label="green")
plt.scatter(x1[colors=="red"], y1[colors=="red"], s=1, label="red")

# mirror (now active system!)
plt.scatter(x2, y2, s=0.5, alpha=0.2, label="coupled mirror")

# grey channels
plt.scatter(x1[grey1], y1[grey1], s=2, c="black", label="grey A")
plt.scatter(x2[grey2], y2[grey2], s=2, c="gray", label="grey B")

# cone
plt.scatter(x1[cone], y1[cone], s=2, c="yellow", alpha=0.6, label="cone")

# phase lock points
plt.scatter(x1[locked], y1[locked], s=3, c="magenta", label="phase lock")

plt.title("NEXAH v8.3 — Coupled Dual Field + Phase Lock")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)

plt.show()
