import numpy as np
import matplotlib.pyplot as plt

# =========================
# GRID
# =========================
N = 600
x = np.linspace(-2.0, 1.0, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

# =========================
# MANDELBROT
# =========================
Z = np.zeros_like(C)
M = np.zeros_like(C, dtype=int)

max_iter = 100

for i in range(max_iter):
    Z = Z**2 + C
    escaped = np.abs(Z) > 2
    M[escaped & (M == 0)] = i
    Z[escaped] = 2

# =========================
# SELECT c (🔥 wichtig)
# =========================
c = -0.75 + 0.1j   # <- hier kannst du spielen

# =========================
# JULIA SET
# =========================
Z_j = X + 1j * Y
J = np.zeros_like(Z_j, dtype=int)

for i in range(max_iter):
    Z_j = Z_j**2 + c
    escaped = np.abs(Z_j) > 2
    J[escaped & (J == 0)] = i
    Z_j[escaped] = 2

# =========================
# PLOT
# =========================
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# --- Mandelbrot ---
axs[0].imshow(M, extent=[-2,1,-1.5,1.5], cmap='inferno')
axs[0].set_title("Mandelbrot (Parameter Space)")
axs[0].plot(c.real, c.imag, 'cyan', markersize=6)  # selected c
axs[0].axis('off')

# --- Connection ---
axs[1].set_title("Mapping")
axs[1].text(0.5, 0.5, f"c = {c.real:.3f} + {c.imag:.3f}i",
            ha='center', va='center', fontsize=12)
axs[1].arrow(0.2, 0.5, 0.6, 0, head_width=0.05, color='cyan')
axs[1].axis('off')

# --- Julia ---
axs[2].imshow(J, extent=[-2,2,-2,2], cmap='inferno')
axs[2].set_title("Julia (Dynamics for c)")
axs[2].axis('off')

# =========================
# SAVE
# =========================
plt.tight_layout()
plt.savefig("RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/dual_mandelbrot_julia.png", dpi=300)
plt.close()

print("Saved dual visualization.")
