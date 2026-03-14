import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

sigma = 10
rho = 28
beta = 8/3

dt = 0.01
steps = 120000

OUTPUT_DIR = "APPLICATIONS/outputs/lorenz_navigation"
os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


def lorenz(x, y, z):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz


x = np.zeros(steps)
y = np.zeros(steps)
z = np.zeros(steps)

x[0], y[0], z[0] = 1.0, 1.0, 1.0

for i in range(steps - 1):
    dx, dy, dz = lorenz(x[i], y[i], z[i])
    x[i+1] = x[i] + dt * dx
    y[i+1] = y[i] + dt * dy
    z[i+1] = z[i] + dt * dz

# transient abschneiden
x = x[5000:]
y = y[5000:]
z = z[5000:]

switch_idx = []
for i in range(1, len(x)):
    if np.sign(x[i]) != np.sign(x[i-1]):
        switch_idx.append(i)

switch_idx = np.array(switch_idx)

plt.figure(figsize=(8, 8))
plt.scatter(x, z, s=0.2, alpha=0.15, label="trajectory cloud")
plt.scatter(x[switch_idx], z[switch_idx], s=6, c="red", label="L/R switches")

plt.xlabel("x")
plt.ylabel("z")
plt.title("Lorenz Switch Map (L/R transition points)")
plt.legend()

filename = f"{OUTPUT_DIR}/lorenz_switch_map_{timestamp}.png"
plt.savefig(filename, dpi=300, bbox_inches="tight")
print("saved:", filename)
plt.show()
