# ============================================================
# NEXAH v6.9b — Field Diagnostics (Speed • Divergence • Curl)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Example system (REPLACE with your real system if needed)
# ------------------------------------------------------------
def field(x, y):
    """
    Simple nonlinear flow field
    Replace with your real NEXAH field if needed
    """
    U = y - x*(x**2 + y**2 - 1)
    V = -x - y*(x**2 + y**2 - 1)
    return U, V


# ------------------------------------------------------------
# Grid
# ------------------------------------------------------------
N = 60
xs = np.linspace(-1.2, 1.2, N)
ys = np.linspace(-1.2, 1.2, N)

X, Y = np.meshgrid(xs, ys)

U, V = field(X, Y)


# ------------------------------------------------------------
# 1. SPEED (Magnitude)
# ------------------------------------------------------------
speed = np.sqrt(U**2 + V**2)


# ------------------------------------------------------------
# 2. DIVERGENCE
# div F = dU/dx + dV/dy
# ------------------------------------------------------------
dU_dx = np.gradient(U, xs, axis=1)
dV_dy = np.gradient(V, ys, axis=0)

div = dU_dx + dV_dy


# ------------------------------------------------------------
# 3. CURL (2D → scalar z-component)
# curl F = dV/dx - dU/dy
# ------------------------------------------------------------
dV_dx = np.gradient(V, xs, axis=1)
dU_dy = np.gradient(U, ys, axis=0)

curl = dV_dx - dU_dy


# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))


# ------------------------------------------------------------
# SPEED MAP
# ------------------------------------------------------------
im0 = axes[0].imshow(
    speed,
    extent=[xs.min(), xs.max(), ys.min(), ys.max()],
    origin='lower'
)
axes[0].set_title("Speed (|v|) — Blueshift Map")
axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")
plt.colorbar(im0, ax=axes[0])


# ------------------------------------------------------------
# DIVERGENCE MAP
# ------------------------------------------------------------
im1 = axes[1].imshow(
    div,
    extent=[xs.min(), xs.max(), ys.min(), ys.max()],
    origin='lower'
)
axes[1].set_title("Divergence (Sources / Sinks)")
axes[1].set_xlabel("X")
axes[1].set_ylabel("Y")
plt.colorbar(im1, ax=axes[1])


# ------------------------------------------------------------
# CURL MAP
# ------------------------------------------------------------
im2 = axes[2].imshow(
    curl,
    extent=[xs.min(), xs.max(), ys.min(), ys.max()],
    origin='lower'
)
axes[2].set_title("Curl (Rotation / Vorticity)")
axes[2].set_xlabel("X")
axes[2].set_ylabel("Y")
plt.colorbar(im2, ax=axes[2])


plt.tight_layout()
plt.show()
