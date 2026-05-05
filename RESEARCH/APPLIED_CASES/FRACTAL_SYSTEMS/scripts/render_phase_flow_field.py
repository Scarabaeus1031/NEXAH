import numpy as np
import matplotlib.pyplot as plt

# Grid
N = 400
x = np.linspace(-2, 1, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)
C = X + 1j * Y

Z = np.zeros_like(C)
phase = np.zeros_like(C, dtype=float)

# Iterate Mandelbrot
for i in range(50):
    Z = Z**2 + C

# Phase field
phase = np.angle(Z)

# Phase gradient (flow)
grad_y, grad_x = np.gradient(phase)

# Mismatch proxy
mismatch = np.sqrt(grad_x**2 + grad_y**2)

# Plot
plt.figure(figsize=(8, 10))

# Phase
plt.subplot(2,1,1)
plt.imshow(phase, cmap='twilight', extent=[-2,1,-1.5,1.5])
plt.title("Phase Field φ(x,y)")
plt.colorbar()

# Flow + mismatch
plt.subplot(2,1,2)
plt.imshow(mismatch, cmap='inferno', extent=[-2,1,-1.5,1.5])
plt.quiver(X[::10,::10], Y[::10,::10],
           grad_x[::10,::10], grad_y[::10,::10],
           color='white', scale=50)

plt.title("Phase Flow + Mismatch Field")

plt.tight_layout()
plt.savefig("RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/phase_flow_field.png", dpi=200)
plt.show()
