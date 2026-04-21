# diagonal_vortex_zoom_mod7_fixed.py

import numpy as np
import matplotlib.pyplot as plt

# Basin centers (aus deinem Output)
centers = {
    0: np.array([-0.1657, -0.1657]),  # Q1
    1: np.array([-0.0349, -0.0349]),  # Q2
    2: np.array([0.1974, 0.1974])     # Q3
}

# Beispiel: lade deine echte basin sequence hier
# z.B. aus file oder direkt einsetzen
# basin_sequence = [...]

# TEST fallback (falls nichts geladen)
basin_sequence = np.random.choice([0,1,2], size=2000)

# Trajectory erzeugen
points = np.array([centers[b] for b in basin_sequence])

# Diagonalband
mask = np.abs(points[:,1] - points[:,0]) < 0.05
filtered = points[mask]

vectors = np.diff(filtered, axis=0)
positions = filtered[:-1]

plt.figure(figsize=(6,6))
plt.quiver(
    positions[:,0], positions[:,1],
    vectors[:,0], vectors[:,1],
    angles='xy', scale_units='xy', scale=1
)

plt.scatter(filtered[:,0], filtered[:,1], s=5)

plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)

plt.title("Diagonal Vortex Zoom (FIXED)")
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
