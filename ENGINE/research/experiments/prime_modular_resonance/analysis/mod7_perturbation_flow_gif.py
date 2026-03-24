import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import isprime
import os

# =========================
# PARAMETER
# =========================
N_MAX = 120
STEP = 2

points = []
colors = []

fig, ax = plt.subplots(figsize=(6,6))

# =========================
# SETUP
# =========================
theta = np.linspace(0, 2*np.pi, 300)
circle_x = np.cos(theta)
circle_y = np.sin(theta)

sc = ax.scatter([], [], s=30)

ax.plot(circle_x, circle_y, alpha=0.3)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')

title = ax.set_title("mod7 Perturbation Primes — evolving")

# =========================
# UPDATE FUNCTION
# =========================
def update(n):

    global points, colors

    for k in range(1, n, max(1, n // 10)):

        val = 10**n - 10**k - 1

        # reduce size (fast test)
        val_mod = val % (10**10 + 19)

        if isprime(val_mod):

            r = val % 7
            angle = 2 * np.pi * r / 7

            x = np.cos(angle)
            y = np.sin(angle)

            points.append([x, y])
            colors.append(k / n)

    if points:
        pts = np.array(points)
        sc.set_offsets(pts)
        sc.set_array(np.array(colors))

    title.set_text(f"mod7 Perturbation Primes — n ≤ {n}")

    return sc,

# =========================
# ANIMATION
# =========================
ani = FuncAnimation(
    fig,
    update,
    frames=range(10, N_MAX, STEP),
    interval=200,
    blit=False
)

# =========================
# SAVE
# =========================
os.makedirs("output/plots", exist_ok=True)

print("[INFO] Saving GIF...")
ani.save("output/plots/mod7_perturbation_flow.gif", writer="pillow", fps=5)
print("[OK] Saved to output/plots/mod7_perturbation_flow.gif")

plt.show()
