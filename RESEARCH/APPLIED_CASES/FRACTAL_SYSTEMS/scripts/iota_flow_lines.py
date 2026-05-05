import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
res = 800
max_iter = 100

xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5

# =========================
# GRID
# =========================
x = np.linspace(xmin, xmax, res)
y = np.linspace(ymin, ymax, res)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

Z = np.zeros_like(C)
mask = np.ones(C.shape, dtype=bool)

# =========================
# MANDELBROT ITERATION
# =========================
for i in range(max_iter):
    Z[mask] = Z[mask]**2 + C[mask]
    mask &= (np.abs(Z) < 4)

# =========================
# PHASE FIELD
# =========================
phi = np.angle(Z)

# =========================
# PHASE GRADIENT (FLOW)
# =========================
grad_y, grad_x = np.gradient(phi)

# =========================
# NORMALIZE FLOW (optional, stabilisiert streamplot)
# =========================
norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-8
ux = grad_x / norm
uy = grad_y / norm

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(10, 10))

# Background: Mandelbrot mask
ax.imshow(mask.T, extent=[xmin, xmax, ymin, ymax],
          cmap='gray', alpha=0.3)

# Optional: Phase field coloring
phase_plot = ax.imshow(phi.T, extent=[xmin, xmax, ymin, ymax],
                       cmap='twilight', alpha=0.6)

# Flow lines (KEY PART)
ax.streamplot(
    X, Y,
    ux, uy,
    color='cyan',
    density=2.0,
    linewidth=0.7,
    arrowsize=0.7
)

ax.set_title("IOTA Flow Lines — Phase Field Geometry")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

plt.colorbar(phase_plot, label="Phase φ(x,y)")
plt.tight_layout()

# =========================
# SAVE
# =========================
plt.savefig(
    "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/iota_flow_lines.png",
    dpi=200
)

plt.show()
