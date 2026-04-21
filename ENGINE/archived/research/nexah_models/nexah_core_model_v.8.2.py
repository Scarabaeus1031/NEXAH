# nexah_core_model_v8.2.py

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# LORENZ SYSTEM
# ---------------------------
def lorenz_step(x, y, z, sigma=10, rho=28, beta=8/3, dt=0.01):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return x + dx * dt, y + dy * dt, z + dz * dt

# ---------------------------
# SIMULATION
# ---------------------------
def simulate(n=20000):
    xs, ys, zs = [], [], []
    x, y, z = 0.1, 0.0, 0.0

    for _ in range(n):
        x, y, z = lorenz_step(x, y, z)
        xs.append(x)
        ys.append(y)
        zs.append(z)

    return np.array(xs), np.array(ys), np.array(zs)

# ---------------------------
# RGB CLASSIFICATION
# ---------------------------
def classify_rgb(x, y):
    if x < -2:
        return "blue"
    elif x > 2:
        return "red"
    else:
        return "green"

# ---------------------------
# GREY CHANNEL (center line)
# ---------------------------
def detect_grey_channel(x, y, threshold=1.2):
    return np.abs(x - y) < threshold

# ---------------------------
# MIRROR FIELD
# ---------------------------
def mirror_field(x, y, z):
    return -x, -y, z

# ---------------------------
# YELLOW CONE (transition volume)
# ---------------------------
def compute_cone_mask(x, y, z):
    # distance from origin projected
    r = np.sqrt(x**2 + y**2)
    # cone condition (tunable)
    return (r < 6) & (z > 10) & (z < 30)

# ---------------------------
# MAIN
# ---------------------------
xs, ys, zs = simulate()

# Mirror system
xs_m, ys_m, zs_m = mirror_field(xs, ys, zs)

# classify
colors = np.array([classify_rgb(x, y) for x, y in zip(xs, ys)])

# grey channel (original + mirror)
grey_mask = detect_grey_channel(xs, ys)
grey_mask_m = detect_grey_channel(xs_m, ys_m)

# yellow cone
cone_mask = compute_cone_mask(xs, ys, zs)

# ---------------------------
# PLOT
# ---------------------------
plt.figure(figsize=(10, 8))

# RGB field
plt.scatter(xs[colors == "blue"], ys[colors == "blue"], s=1, label="blue")
plt.scatter(xs[colors == "green"], ys[colors == "green"], s=1, label="green")
plt.scatter(xs[colors == "red"], ys[colors == "red"], s=1, label="red")

# mirror field (faint)
plt.scatter(xs_m, ys_m, s=0.5, alpha=0.15, label="mirror")

# grey channels
plt.scatter(xs[grey_mask], ys[grey_mask], s=2, c="black", label="grey (main)")
plt.scatter(xs_m[grey_mask_m], ys_m[grey_mask_m], s=2, c="gray", label="grey (mirror)")

# yellow cone
plt.scatter(xs[cone_mask], ys[cone_mask], s=2, c="yellow", alpha=0.6, label="cone")

plt.title("NEXAH v8.2 — Mirror + Dual Channel + Cone")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)

plt.show()
