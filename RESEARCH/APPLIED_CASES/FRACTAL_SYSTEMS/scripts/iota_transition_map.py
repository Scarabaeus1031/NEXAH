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
# ITERATION (SAFE)
# =========================
for i in range(max_iter):
    Z[mask] = Z[mask]**2 + C[mask]
    mask &= (np.abs(Z) < 4)

# =========================
# PHASE FIELD
# =========================
phi = np.angle(Z)

# =========================
# GRADIENT (FLOW)
# =========================
grad_y, grad_x = np.gradient(phi)

# mismatch / iota field
M = np.sqrt(grad_x**2 + grad_y**2)

# normalize
M = M / np.max(M)

# =========================
# THRESHOLD (IOTA EVENTS)
# =========================
threshold = 0.4
iota_mask = M > threshold

# =========================
# PLOT
# =========================
fig, ax = plt.subplots(figsize=(8, 8))

# background = mandelbrot mask
ax.imshow(mask.T, extent=[xmin, xmax, ymin, ymax], cmap='gray', alpha=0.3)

# iota field
im = ax.imshow(M.T, extent=[xmin, xmax, ymin, ymax],
               cmap='inferno', alpha=0.8)

# highlight transitions
ax.scatter(X[iota_mask], Y[iota_mask],
           s=1, c='cyan', alpha=0.6)

ax.set_title("IOTA Transition Map — Phase Mismatch Field")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

plt.colorbar(im, label="Mismatch M(x,y)")
plt.tight_layout()

# =========================
# SAVE
# =========================
plt.savefig(
    "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/iota_transition_map.png",
    dpi=200
)

plt.show()
