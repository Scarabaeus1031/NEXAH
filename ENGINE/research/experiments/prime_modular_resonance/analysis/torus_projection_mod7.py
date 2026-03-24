# torus_projection_mod7.py

import numpy as np
import matplotlib.pyplot as plt

# gleiche centers wie oben
centers = {
    0: np.array([-0.1657, -0.1657]),
    1: np.array([-0.0349, -0.0349]),
    2: np.array([0.1974, 0.1974])
}

# gleiche sequence wie oben verwenden
basin_sequence = np.random.choice([0,1,2], size=2000)

points = np.array([centers[b] for b in basin_sequence])

# auf Torus mappen
theta = 2*np.pi * (points[:,0] + 1)/2
phi   = 2*np.pi * (points[:,1] + 1)/2

R = 1.0
r = 0.3

X = (R + r*np.cos(phi)) * np.cos(theta)
Y = (R + r*np.cos(phi)) * np.sin(theta)
Z = r * np.sin(phi)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')

ax.plot(X, Y, Z, linewidth=0.5)

ax.set_title("Torus Projection (mod 7)")
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
