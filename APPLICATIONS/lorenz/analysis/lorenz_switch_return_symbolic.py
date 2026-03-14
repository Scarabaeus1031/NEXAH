import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
from collections import Counter

# -------------------------------
# Parameters
# -------------------------------

sigma = 10
rho = 28
beta = 8/3

dt = 0.01
steps = 150000

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


# -------------------------------
# Lorenz equations
# -------------------------------

def lorenz(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


# -------------------------------
# Integrate trajectory
# -------------------------------

x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

x[0], y[0], z[0] = 1.0, 1.0, 1.0

for i in range(steps - 1):

    dx, dy, dz = lorenz(x[i], y[i], z[i])

    x[i+1] = x[i] + dt * dx
    y[i+1] = y[i] + dt * dy
    z[i+1] = z[i] + dt * dz


# remove transient
x = x[5000:]
y = y[5000:]
z = z[5000:]


# -------------------------------
# Symbolic sequence
# -------------------------------

symbols = []

for xi in x:
    if xi > 0:
        symbols.append("R")
    else:
        symbols.append("L")


# -------------------------------
# Detect switches
# -------------------------------

switch_idx = []

for i in range(1, len(x)):
    if np.sign(x[i]) != np.sign(x[i-1]):
        switch_idx.append(i)

switch_idx = np.array(switch_idx)


# -------------------------------
# Return map variable
# -------------------------------
# normalize z coordinate

zmin = np.min(z[switch_idx])
zmax = np.max(z[switch_idx])

u = (z[switch_idx] - zmin) / (zmax - zmin)


# -------------------------------
# symbolic patterns around switch
# -------------------------------

patterns = []

window = 3

for idx in switch_idx:

    if idx + window < len(symbols):

        p = "".join(symbols[idx:idx+window])
        patterns.append(p)

counter = Counter(patterns)


print("\nSwitch pattern counts:\n")

for k, v in counter.most_common():

    print(k, v)


# -------------------------------
# Plot 1: Switch map
# -------------------------------

plt.figure(figsize=(8,8))

plt.scatter(x, z, s=0.2, alpha=0.1, label="trajectory")

plt.scatter(
    x[switch_idx],
    z[switch_idx],
    s=8,
    c=u,
    cmap="plasma",
    label="switch points"
)

plt.xlabel("x")
plt.ylabel("z")

plt.title("Lorenz Switch Map (colored by return coordinate)")

plt.legend()

filename = f"{OUTPUT_DIR}/lorenz_switch_return_map_{timestamp}.png"

plt.savefig(filename, dpi=300, bbox_inches="tight")

print("\nsaved:", filename)

plt.show()


# -------------------------------
# Plot 2: Return map
# -------------------------------

plt.figure(figsize=(6,6))

plt.scatter(u[:-1], u[1:], s=4, alpha=0.6)

plt.xlabel("u_n")
plt.ylabel("u_{n+1}")

plt.title("Lorenz Return Map (switch section)")

filename = f"{OUTPUT_DIR}/lorenz_return_map_{timestamp}.png"

plt.savefig(filename, dpi=300, bbox_inches="tight")

print("saved:", filename)

plt.show()
