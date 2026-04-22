# NEXAH — Field Decomposition Experiment
# Purpose: Split vector field into gradient + rotational components
# Context: understanding orbit-like dynamics in field representation

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# INPUT:
# X, Y : meshgrid
# U, V : vector field components on same grid
# Optional: potential background Z or your existing scalar field
# ============================================================

# ------------------------------------------------------------
# Example placeholder:
# Replace this block with your real X, Y, U, V
# ------------------------------------------------------------
x = np.linspace(6, 17, 220)
y = np.linspace(22, 31, 220)
X, Y = np.meshgrid(x, y)

# synthetic demo field with attractors + swirl
def gauss(x0, y0, sx, sy, amp):
    return amp * np.exp(-(((X - x0)**2)/(2*sx**2) + ((Y - y0)**2)/(2*sy**2)))

phi = (
    -2.0 * gauss(13.5, 26.0, 1.2, 1.0, 1.0)
    -1.5 * gauss(10.0, 25.0, 1.4, 1.2, 1.0)
    +1.8 * gauss(11.2, 28.6, 1.0, 1.0, 1.0)
)

dx = x[1] - x[0]
dy = y[1] - y[0]

# gradient part from scalar potential phi
dphi_dy, dphi_dx = np.gradient(phi, dy, dx)
U_grad_true = -dphi_dx
V_grad_true = -dphi_dy

# add a rotational part via stream function psi
psi = (
    1.2 * gauss(11.0, 28.6, 1.4, 1.2, 1.0)
    -0.9 * gauss(13.5, 26.0, 1.5, 1.2, 1.0)
)
dpsi_dy, dpsi_dx = np.gradient(psi, dy, dx)
U_rot_true = dpsi_dy
V_rot_true = -dpsi_dx

U = U_grad_true + U_rot_true
V = V_grad_true + V_rot_true

# ------------------------------------------------------------
# NUMERICAL SPLIT (Helmholtz-like decomposition in 2D)
# periodic/FFT-based approximation
# ------------------------------------------------------------
ny, nx = U.shape

kx = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(ny, d=dy)
KX, KY = np.meshgrid(kx, ky)
K2 = KX**2 + KY**2
K2[0, 0] = 1.0  # avoid division by zero

Uhat = np.fft.fft2(U)
Vhat = np.fft.fft2(V)

# Gradient / irrotational component in Fourier space
dot = KX * Uhat + KY * Vhat
Uhat_grad = KX * dot / K2
Vhat_grad = KY * dot / K2

# Rotational component = total - gradient
Uhat_rot = Uhat - Uhat_grad
Vhat_rot = Vhat - Vhat_grad

U_grad = np.real(np.fft.ifft2(Uhat_grad))
V_grad = np.real(np.fft.ifft2(Vhat_grad))

U_rot = np.real(np.fft.ifft2(Uhat_rot))
V_rot = np.real(np.fft.ifft2(Vhat_rot))

# Magnitudes for backgrounds
mag_total = np.sqrt(U**2 + V**2)
mag_grad = np.sqrt(U_grad**2 + V_grad**2)
mag_rot = np.sqrt(U_rot**2 + V_rot**2)

# Optional: vorticity / divergence
dV_dy, dV_dx = np.gradient(V, dy, dx)
dU_dy, dU_dx = np.gradient(U, dy, dx)

div_total = dU_dx + dV_dy
curl_total = dV_dx - dU_dy

# ------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 11))

skip = (slice(None, None, 8), slice(None, None, 8))

# Q1 — Gradient part
ax = axs[0, 0]
cf = ax.contourf(X, Y, mag_grad, levels=30, cmap="viridis")
ax.streamplot(X, Y, U_grad, V_grad, color="white", density=1.5, linewidth=0.8)
ax.set_title("Q1 — Gradientenfeld (ziehender Anteil)")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# Q2 — Rotational part
ax = axs[0, 1]
cf = ax.contourf(X, Y, mag_rot, levels=30, cmap="magma")
ax.streamplot(X, Y, U_rot, V_rot, color="white", density=1.5, linewidth=0.8)
ax.set_title("Q2 — Rotationsfeld (umlaufender Anteil)")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# Q3 — Combined field
ax = axs[1, 0]
cf = ax.contourf(X, Y, mag_total, levels=30, cmap="cividis")
ax.streamplot(X, Y, U, V, color="white", density=1.5, linewidth=0.8)
ax.set_title("Q3 — Kombiniertes Feld")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

# Q4 — Diagnostics
ax = axs[1, 1]
cf = ax.contourf(X, Y, curl_total, levels=30, cmap="coolwarm")
ax.contour(X, Y, div_total, levels=12, colors="black", linewidths=0.6, alpha=0.7)
ax.set_title("Q4 — Curl / Divergence Diagnose")
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(cf, ax=ax)

plt.tight_layout()

# =========================
# NEXAH SAVE BLOCK
# =========================

import os
import matplotlib.pyplot as plt
from datetime import datetime

SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
OUTDIR = os.path.join("ENGINE/analysis/field_decomposition/outputs", SCRIPT_NAME)

os.makedirs(OUTDIR, exist_ok=True)

# --- Save figure ---
outfile = os.path.join(OUTDIR, f"{SCRIPT_NAME}.png")

try:
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    print(f"✓ saved figure → {outfile}")
except Exception as e:
    print("⚠️ could not save figure:", e)

# --- Save run info ---
info_path = os.path.join(OUTDIR, "run_info.txt")
with open(info_path, "w") as f:
    f.write(f"script: {SCRIPT_NAME}\n")
    f.write(f"time: {datetime.now()}\n")

# --- Close plot ---
plt.close()
