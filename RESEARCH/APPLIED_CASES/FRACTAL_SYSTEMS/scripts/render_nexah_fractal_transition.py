import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Mandelbrot (oben)
# -----------------------------
def mandelbrot(width, height, max_iter=50):
    re = np.linspace(-2, 1, width)
    im = np.linspace(-1.5, 1.5, height)
    c = re[np.newaxis, :] + 1j * im[:, np.newaxis]
    z = np.zeros_like(c)
    div_time = np.zeros(c.shape, dtype=int)

    for i in range(max_iter):
        z = z*z + c
        diverged = np.abs(z) > 2
        div_time[diverged & (div_time == 0)] = i
        z[diverged] = 2

    return div_time

# -----------------------------
# Julia (unten)
# -----------------------------
def julia(width, height, c=-0.7+0.27015j, max_iter=50):
    re = np.linspace(-1.5, 1.5, width)
    im = np.linspace(-1.5, 1.5, height)
    z = re[np.newaxis, :] + 1j * im[:, np.newaxis]
    div_time = np.zeros(z.shape, dtype=int)

    for i in range(max_iter):
        z = z*z + c
        diverged = np.abs(z) > 2
        div_time[diverged & (div_time == 0)] = i
        z[diverged] = 2

    return div_time

# -----------------------------
# Transition Field (Mitte)
# -----------------------------
def generate_transition_field(n_points=2000):
    angles = np.random.uniform(0, 2*np.pi, n_points)
    radii = np.random.uniform(0.1, 1.0, n_points)

    x = radii * np.cos(angles)
    y = radii * np.sin(angles)

    # Drift (Flow)
    dx = -y
    dy = x

    # Mismatch / IOTA intensity
    mismatch = np.abs(np.sin(3*angles)) * radii

    return x, y, dx, dy, mismatch

# -----------------------------
# Rendering
# -----------------------------
fig = plt.figure(figsize=(10, 15))
fig.patch.set_facecolor("black")

# Mandelbrot
ax1 = plt.subplot2grid((3,1), (0,0))
mandel = mandelbrot(500, 500)
ax1.imshow(mandel, cmap="inferno", extent=[-2,1,-1.5,1.5])
ax1.set_title("Mandelbrot (Structure)", color="white")
ax1.axis("off")

# Transition Layer
ax2 = plt.subplot2grid((3,1), (1,0))
ax2.set_facecolor("black")

x, y, dx, dy, mismatch = generate_transition_field()

# Flow lines
ax2.quiver(x, y, dx, dy, mismatch,
           cmap="plasma", scale=20, alpha=0.7)

# IOTA points (high mismatch)
mask = mismatch > 0.7
ax2.scatter(x[mask], y[mask],
            color="white", s=5, label="IOTA")

ax2.set_title("Transition Layer (Phase • Drift • IOTA)", color="white")
ax2.axis("off")

# Julia
ax3 = plt.subplot2grid((3,1), (2,0))
julia_set = julia(500, 500)
ax3.imshow(julia_set, cmap="cool", extent=[-1.5,1.5,-1.5,1.5])
ax3.set_title("Julia (Behavior)", color="white")
ax3.axis("off")

plt.tight_layout()
import os

output_dir = "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "nexah_fractal_transition.png")

plt.savefig(output_path, dpi=300, facecolor="black")

print(f"Saved to: {output_path}")
