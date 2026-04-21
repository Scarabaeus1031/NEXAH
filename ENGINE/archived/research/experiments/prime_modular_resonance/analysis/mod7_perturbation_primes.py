import numpy as np
import matplotlib.pyplot as plt
from sympy import isprime

# =========================
# PARAMETER
# =========================
N_MAX = 200      # max exponent n
SAMPLES = 200    # number of samples

points = []
colors = []

# =========================
# GENERATE PERTURBATION PRIMES
# =========================
for n in range(10, N_MAX):
    for k in range(1, n, max(1, n // 10)):  # sparse sampling

        val = 10**n - 10**k - 1

        # reduce size for primality test (approx trick)
        val_mod = val % (10**12 + 39)

        if isprime(val_mod):
            r = val % 7
            angle = 2 * np.pi * r / 7

            x = np.cos(angle)
            y = np.sin(angle)

            points.append((x, y))

            # color by perturbation distance
            colors.append((k / n))

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(6,6))

# circle
theta = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(theta), np.sin(theta), alpha=0.3)

# points
if points:
    pts = np.array(points)
    sc = ax.scatter(pts[:,0], pts[:,1], c=colors, cmap='plasma', s=30)

# styling
ax.set_title("mod7 Perturbation Primes")
ax.set_aspect('equal')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.axis('off')

plt.colorbar(sc, label="k / n (perturbation ratio)")

# =========================
# SAVE
# =========================
import os

os.makedirs("output/plots", exist_ok=True)
plt.savefig("output/plots/mod7_perturbation_primes.png", dpi=200)

plt.show()
