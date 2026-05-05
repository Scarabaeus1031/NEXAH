import numpy as np
import matplotlib.pyplot as plt

# =========================
# GRID (Parameterraum = Mandelbrot)
# =========================
res = 800
x = np.linspace(-2.0, 1.0, res)
y = np.linspace(-1.5, 1.5, res)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

# =========================
# ITERATION
# =========================
max_iter = 80
Z = np.zeros_like(C, dtype=np.complex128)

# Speicher für "Dynamik-Intensität"
field = np.zeros_like(C, dtype=float)

for i in range(max_iter):
    Z = Z**2 + C

    # Escape measure (smooth)
    mask = np.abs(Z) < 10
    field[mask] += np.abs(Z[mask])

# Normalisieren
field = field / max_iter

# =========================
# PHASE FIELD (optional)
# =========================
phase = np.angle(Z)

# =========================
# VISUAL
# =========================
plt.figure(figsize=(10, 10))

# Hintergrund = kontinuierliche Julia-Dynamik
plt.imshow(field, extent=(-2,1,-1.5,1.5), origin="lower")

# Phase Overlay (optional Struktur)
plt.imshow(phase, extent=(-2,1,-1.5,1.5), origin="lower", alpha=0.3)

plt.colorbar(label="Julia Field Intensity")

plt.title("Continuous Julia Field (Parameter → Dynamics Mapping)")
plt.xlabel("Re(c)")
plt.ylabel("Im(c)")

plt.tight_layout()
plt.savefig(
    "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/continuous_julia_field.png",
    dpi=300
)

plt.show()
