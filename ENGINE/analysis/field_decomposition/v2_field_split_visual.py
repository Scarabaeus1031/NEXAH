import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

# --- INPUT: dein Feld ---
# V = Potential
# U, Vx = Gradientenfeld Komponenten (dx/dt)

# Beispiel:
# X, Y meshgrid
# U = -dV/dx
# Vx = -dV/dy

fig, ax = plt.subplots(figsize=(8, 8))

# --- 1. Basisfeld ---
contour = ax.contourf(X, Y, V, levels=50, cmap="viridis", alpha=0.85)

# --- 2. Flow Lines ---
ax.streamplot(X, Y, U, Vx, color="white", density=1.5, linewidth=1)

# --- 3. Gradient Magnitude → zeigt „aktive Zonen“ ---
grad_mag = gaussian_gradient_magnitude(V, sigma=1.0)
ax.contour(X, Y, grad_mag, levels=10, colors="white", alpha=0.2)

# --- 4. Attraktoren markieren (Minima) ---
attractors = [
    (10, 25, "C0"),
    (12, 24, "C1"),
    (14, 26, "C2"),
    (11, 28.5, "C3"),
]

for x, y, label in attractors:
    ax.scatter(x, y, s=120, edgecolor="black", linewidth=1.5)
    ax.text(x + 0.2, y + 0.2, label, color="white", fontsize=10)

# --- 5. Saddle / „Zahn“ markieren ---
# (Position musst du ggf. leicht anpassen)
saddle = (12.8, 27.2)

ax.scatter(*saddle, color="white", s=100, marker="X")
ax.text(saddle[0] + 0.2, saddle[1] + 0.2, "FLOW GATE", color="white")

# --- 6. Separatrix (Boundary) approx ---
# einfache Variante: hohe Gradientenbereiche
boundary = grad_mag > np.percentile(grad_mag, 85)

ax.contour(X, Y, boundary, levels=[0.5], colors="magenta", linewidths=2)

# --- 7. Labels für Regionen ---
ax.text(9, 29.5, "SOURCE REGION", color="white", fontsize=9)
ax.text(13.5, 24, "ATTRACTOR BASIN", color="white", fontsize=9)
ax.text(7, 23, "LOW FLOW ZONE", color="white", fontsize=9)

# --- Styling ---
ax.set_title("NEXAH Field Structure — V2 (Readable Geometry)")
ax.set_xlabel("α")
ax.set_ylabel("β")

plt.colorbar(contour)
plt.show()
