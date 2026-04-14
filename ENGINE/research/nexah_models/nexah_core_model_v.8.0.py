import numpy as np
import matplotlib.pyplot as plt

# ================================
# PARAMETERS
# ================================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

dt = 0.01
steps = 15000

alpha_mirror = 0.35
cone_strength = 0.15

# ================================
# LORENZ SYSTEM
# ================================

def lorenz(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

# ================================
# SIMULATION
# ================================

x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

x[0], y[0], z[0] = 0.1, 0.0, 0.0

for i in range(steps - 1):
    dx, dy, dz = lorenz(x[i], y[i], z[i])

    # Mirror field
    dx_m, dy_m, dz_m = lorenz(-x[i], -y[i], z[i])

    # Combine original + mirror
    dx_total = dx + alpha_mirror * dx_m
    dy_total = dy + alpha_mirror * dy_m
    dz_total = dz + alpha_mirror * dz_m

    # Cone constraint (radial structure)
    r_xy = np.sqrt(x[i]**2 + y[i]**2) + 1e-6
    cone = r_xy / (z[i] + 20.0)

    dx_total += cone_strength * x[i] * cone
    dy_total += cone_strength * y[i] * cone

    x[i+1] = x[i] + dx_total * dt
    y[i+1] = y[i] + dy_total * dt
    z[i+1] = z[i] + dz_total * dt

# ================================
# R/T PROXY (DYNAMICS)
# ================================

velocity = np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)
radius = np.sqrt(x[:-1]**2 + y[:-1]**2)

rt = radius / (velocity + 1e-6)

# normalize
rt_norm = (rt - rt.min()) / (rt.max() - rt.min())

# ================================
# STATE CLASSIFICATION (RGB + GREY)
# ================================

states = []

for i in range(len(rt_norm)):
    val = rt_norm[i]

    if val < 0.25:
        states.append("blue")      # stable basin
    elif val < 0.5:
        states.append("green")     # transition
    elif val < 0.75:
        states.append("red")       # drift
    else:
        states.append("grey")      # interference / nodes

states = np.array(states)

# ================================
# GREY STAR NODE DETECTION (MYZEL)
# ================================

grey_mask = (states == "grey")

# zusätzliche Bedingung: geringe Bewegung → stabile Knoten
low_velocity = velocity < np.percentile(velocity, 20)

nodes = grey_mask & low_velocity

# ================================
# PLOT 1 — FIELD WITH STATES
# ================================

plt.figure(figsize=(8, 6))

plt.scatter(x[:-1][states=="blue"], y[:-1][states=="blue"], s=1, label="blue")
plt.scatter(x[:-1][states=="green"], y[:-1][states=="green"], s=1, label="green")
plt.scatter(x[:-1][states=="red"], y[:-1][states=="red"], s=1, label="red")
plt.scatter(x[:-1][states=="grey"], y[:-1][states=="grey"], s=2, c="black", label="grey")

plt.title("NEXAH v8.0 — Full Field (RGB + Grey)")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()

# ================================
# PLOT 2 — GREY STAR NODES
# ================================

plt.figure(figsize=(6, 6))

plt.scatter(x[:-1], y[:-1], s=0.2, alpha=0.1)
plt.scatter(x[:-1][nodes], y[:-1][nodes], s=8, c="black")

plt.title("Grey Star Nodes — Mycel Network")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

# ================================
# PLOT 3 — R/T FIELD
# ================================

plt.figure(figsize=(6, 4))
plt.plot(rt_norm)
plt.title("R/T Field Dynamics")
plt.show()

# ================================
# SUMMARY
# ================================

unique, counts = np.unique(states, return_counts=True)
total = len(states)

print("\n=== NEXAH v8.0 Summary ===")
for u, c in zip(unique, counts):
    print(f"{u}: {c} ({c/total:.3f})")
