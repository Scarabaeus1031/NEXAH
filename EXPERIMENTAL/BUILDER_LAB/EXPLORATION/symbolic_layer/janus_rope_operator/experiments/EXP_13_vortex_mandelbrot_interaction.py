import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# Funktion zum Generieren der Lagrange-Punkte
def lagrange_points():
    L6 = np.array([1.0, -0.5])  # Lagrange Punkt 6
    L7 = np.array([1.0, 0.5])   # Lagrange Punkt 7
    return L6, L7

# Funktion zur Berechnung der Mandelbrot-Menge
def mandelbrot(c, max_iter=1000):
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return max_iter

# Erstellen der Mandelbrot-Menge im komplexen Raum
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter=1000):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return np.array([[mandelbrot(complex(r, i), max_iter) for r in r1] for i in r2])

# Initialisierung der Lagrange-Punkte
L6, L7 = lagrange_points()

# Mandelbrot-Parameter und -Bereich
xmin, xmax, ymin, ymax = -2, 2, -2, 2
width, height = 800, 800

# Berechnung der Mandelbrot-Menge für beide Lagrange-Punkte
mandelbrot_L6 = mandelbrot_set(xmin, xmax, ymin, ymax, width, height)
mandelbrot_L7 = mandelbrot_set(xmin, xmax, ymin, ymax, width, height)

# Erstellen der Visualisierung
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# Mandelbrot-Lagrange 6 Visualisierung
cax1 = ax[0].imshow(mandelbrot_L6, extent=(xmin, xmax, ymin, ymax), cmap="inferno")
fig.colorbar(cax1, ax=ax[0])
ax[0].set_title("Mandelbrot - Lagrange 6 Phase Map")
ax[0].set_xlabel('Re')
ax[0].set_ylabel('Im')

# Mandelbrot-Lagrange 7 Visualisierung
cax2 = ax[1].imshow(mandelbrot_L7, extent=(xmin, xmax, ymin, ymax), cmap="inferno")
fig.colorbar(cax2, ax=ax[1])
ax[1].set_title("Mandelbrot - Lagrange 7 Phase Map")
ax[1].set_xlabel('Re')
ax[1].set_ylabel('Im')

plt.tight_layout()

# Speichern der Visualisierung
output_dir = "EXPERIMENTAL/BUILDER_LAB/EXPLORATION/symbolic_layer/janus_rope_operator/experiments/EXP_13/"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}mandelbrot_lagrange_interaction.png")

# Anzeigen der Ergebnisse
plt.show()

# Berechnung der numerischen Ergebnisse
numerical_results = {
    "L6 Phase": {"Mean": np.mean(mandelbrot_L6), "Max": np.max(mandelbrot_L6), "Min": np.min(mandelbrot_L6)},
    "L7 Phase": {"Mean": np.mean(mandelbrot_L7), "Max": np.max(mandelbrot_L7), "Min": np.min(mandelbrot_L7)},
}

numerical_results
