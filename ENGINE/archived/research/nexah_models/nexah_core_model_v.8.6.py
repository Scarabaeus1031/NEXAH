# nexah_core_model_v8.6.py

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PARAMETERS
# -----------------------------
sigma = 10
rho = 28
beta = 8/3

dt = 0.01
steps = 20000

# Elastic line (Spanngurt)
a = 0.7
b = 2.0

# -----------------------------
# STORAGE
# -----------------------------
x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

# initial condition
x[0], y[0], z[0] = 0.1, 0.0, 0.0

theta = np.zeros(steps)
dtheta = np.zeros(steps)

# -----------------------------
# FUNCTIONS
# -----------------------------
def adaptive_k(theta, dtheta, d):
    """
    Adaptive stiffness:
    - stronger when chaotic (high dtheta)
    - stronger when far from channel
    """
    base = 0.02
    
    k_theta = 0.01 * np.abs(np.sin(theta))
    k_dtheta = 0.02 * np.clip(np.abs(dtheta), 0, 5)
    k_dist = 0.05 * np.abs(d)
    
    return base + k_theta + k_dtheta + k_dist


def elastic_constraint(x, y, theta, dtheta):
    """
    Adaptive elastic lock (Spanngurt)
    """
    d = y - (a * x + b)
    k = adaptive_k(theta, dtheta, d)
    return -k * d


# -----------------------------
# SIMULATION
# -----------------------------
for i in range(steps - 1):

    dx = sigma * (y[i] - x[i])
    dy = x[i] * (rho - z[i]) - y[i]
    dz = x[i] * y[i] - beta * z[i]

    # angle
    theta[i] = np.arctan2(y[i], x[i])

    if i > 0:
        dtheta[i] = theta[i] - theta[i-1]

    # apply adaptive elastic constraint
    dy += elastic_constraint(x[i], y[i], theta[i], dtheta[i])

    # integrate
    x[i+1] = x[i] + dx * dt
    y[i+1] = y[i] + dy * dt
    z[i+1] = z[i] + dz * dt


# -----------------------------
# FINAL ANGLES
# -----------------------------
theta[-1] = np.arctan2(y[-1], x[-1])
dtheta[-1] = theta[-1] - theta[-2]


# -----------------------------
# CLASSIFICATION (RGB + Grey)
# -----------------------------
blue = []
green = []
red = []
grey = []

threshold = 0.05

for i in range(steps):
    d = abs(y[i] - (a * x[i] + b))

    if d < threshold:
        grey.append((x[i], y[i]))
    else:
        if x[i] < -5:
            blue.append((x[i], y[i]))
        elif x[i] > 5:
            green.append((x[i], y[i]))
        else:
            red.append((x[i], y[i]))


# -----------------------------
# PLOT FIELD
# -----------------------------
plt.figure(figsize=(10, 6))

if blue:
    bx, by = zip(*blue)
    plt.scatter(bx, by, s=2, label="blue")

if green:
    gx, gy = zip(*green)
    plt.scatter(gx, gy, s=2, label="green")

if red:
    rx, ry = zip(*red)
    plt.scatter(rx, ry, s=2, label="red")

if grey:
    grx, gry = zip(*grey)
    plt.scatter(grx, gry, s=3, c="black", label="grey")

# elastic line
xx = np.linspace(min(x), max(x), 200)
yy = a * xx + b
plt.plot(xx, yy, color="orange", linewidth=2, label="elastic axis")

plt.title("NEXAH v8.6 — Adaptive Elastic Lock")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid()
plt.show()


# -----------------------------
# ANGULAR DISTRIBUTION
# -----------------------------
angles = (np.degrees(theta) + 360) % 360

plt.figure(figsize=(8, 4))
plt.hist(angles, bins=180)
plt.title("Angular Distribution (v8.6)")
plt.xlabel("Degrees")
plt.ylabel("Count")
plt.show()


# -----------------------------
# SUMMARY
# -----------------------------
total = steps

print("\n=== NEXAH v8.6 Summary ===")
print(f"blue: {len(blue)} ({len(blue)/total:.3f})")
print(f"green: {len(green)} ({len(green)/total:.3f})")
print(f"red: {len(red)} ({len(red)/total:.3f})")
print(f"grey: {len(grey)} ({len(grey)/total:.3f})")
