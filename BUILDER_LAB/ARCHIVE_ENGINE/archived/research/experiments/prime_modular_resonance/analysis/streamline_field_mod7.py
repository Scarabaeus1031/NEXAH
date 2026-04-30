# streamline_field_mod7.py

import numpy as np
import matplotlib.pyplot as plt

# Grid
x = np.linspace(-1,1,100)
y = np.linspace(-1,1,100)
X, Y = np.meshgrid(x, y)

U = np.zeros_like(X)
V = np.zeros_like(Y)

# Einfluss der Basin-Zentren
centers = np.array([
    [-0.1657, -0.1657],
    [-0.0349, -0.0349],
    [0.1974, 0.1974]
])

for cx, cy in centers:
    dx = X - cx
    dy = Y - cy
    r2 = dx**2 + dy**2 + 1e-4
    
    # Rotationsfeld (Curl)
    U += -dy / r2
    V += dx / r2

# Drift hinzufügen (deine Diagonale)
U += 0.5
V += 0.5

plt.figure(figsize=(6,6))
plt.streamplot(X, Y, U, V, density=2)

plt.scatter(centers[:,0], centers[:,1], color='red')

plt.title("Stream Flow Field (mod 7)")
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.grid()
plt.show()


# ================= AUTO SAVE HOOK =================
import os
import matplotlib.pyplot as plt

if os.environ.get("AUTO_SAVE") == "1":

    figs = list(map(plt.figure, plt.get_fignums()))

    if not figs:
        print("[WARN] No figures to save.")

    for i, fig in enumerate(figs):
        filename = __file__.split("/")[-1].replace(".py", f"_{i}.png")
        fig.savefig(f"output/plots/{filename}", dpi=150, bbox_inches="tight")

    plt.close("all")

else:
    plt.show()

# =================================================
