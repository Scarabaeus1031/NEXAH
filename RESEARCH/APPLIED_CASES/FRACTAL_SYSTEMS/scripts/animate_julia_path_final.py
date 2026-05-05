import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# ----------------------------
# SETTINGS
# ----------------------------
WIDTH, HEIGHT = 600, 600
MAX_ITER = 200
FRAMES = 60

BASE_PATH = "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs"
GIF_PATH = os.path.join(BASE_PATH, "julia_path_final.gif")
MAND_PATH = os.path.join(BASE_PATH, "mandelbrot_path.png")
DELTA_PATH = os.path.join(BASE_PATH, "delta_plot.png")

MAND_RES = 400

os.makedirs(BASE_PATH, exist_ok=True)

# ----------------------------
# COMPLEX GRID
# ----------------------------
x = np.linspace(-1.5, 1.5, WIDTH)
y = np.linspace(-1.5, 1.5, HEIGHT)
X, Y = np.meshgrid(x, y)
Z0 = X + 1j * Y

# ----------------------------
# JULIA FUNCTION
# ----------------------------
def compute_julia(c):
    Z = Z0.copy()
    mask = np.ones(Z.shape, dtype=bool)
    output = np.zeros(Z.shape)

    for i in range(MAX_ITER):
        Z[mask] = Z[mask]**2 + c

        # Optional stability clamp (prevents overflow noise)
        Z[np.abs(Z) > 10] = 10

        mask = np.abs(Z) < 4
        output += mask

    return output


# ----------------------------
# PATH (Circle)
# ----------------------------
center = -0.75 + 0j
radius = 0.3

t_vals = np.linspace(0, 2*np.pi, FRAMES)
c_vals = center + radius * np.exp(1j * t_vals)

# ----------------------------
# STORAGE
# ----------------------------
images = []
prev_frame = None
transition_frames = []

# ----------------------------
# MAIN LOOP
# ----------------------------
print("Generating Julia animation with transition detection...")

for i, c in enumerate(c_vals):
    print(f"Frame {i+1}/{FRAMES} | c = {c}")

    julia = compute_julia(c)
    julia_norm = julia / np.max(julia)

    # Transition detection
    if prev_frame is not None:
        delta = np.mean(np.abs(julia_norm - prev_frame))
        if delta > 0.08:
            transition_frames.append((i, c, delta))
            print(f"⚡ Transition detected at frame {i} | Δ = {delta:.4f}")

    prev_frame = julia_norm.copy()

    # Plot
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(julia_norm, extent=(-1.5,1.5,-1.5,1.5), cmap='inferno')
    ax.set_title(f"Julia Set | c = {c.real:.3f} + {c.imag:.3f}i")
    ax.axis('off')

    # --- MODERN BUFFER METHOD ---
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    image = buf[:, :, :3]  # drop alpha channel
    images.append(image)

    plt.close(fig)

# ----------------------------
# SAVE GIF
# ----------------------------
imageio.mimsave(GIF_PATH, images, fps=10)
print(f"\nGIF saved at: {GIF_PATH}")

# ----------------------------
# MANDELBROT
# ----------------------------
def compute_mandelbrot():
    x = np.linspace(-2, 1, MAND_RES)
    y = np.linspace(-1.5, 1.5, MAND_RES)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    mask = np.ones(C.shape, dtype=bool)
    output = np.zeros(C.shape)

    for i in range(100):
        Z[mask] = Z[mask]**2 + C[mask]
        mask = np.abs(Z) < 4
        output += mask

    return output, x, y

mand, mx, my = compute_mandelbrot()

plt.figure(figsize=(6,6))
plt.imshow(mand, extent=(mx.min(), mx.max(), my.min(), my.max()), cmap='magma')
plt.plot(c_vals.real, c_vals.imag, color='cyan', linewidth=2)
plt.scatter(c_vals.real, c_vals.imag, s=5, color='white')
plt.title("Mandelbrot + Path")
plt.xlabel("Re")
plt.ylabel("Im")

plt.savefig(MAND_PATH, dpi=200, bbox_inches='tight')
plt.close()

print(f"Mandelbrot plot saved at: {MAND_PATH}")

# ----------------------------
# DELTA PLOT
# ----------------------------
deltas = []
for i in range(1, len(images)):
    d = np.mean(np.abs(images[i].astype(float) - images[i-1].astype(float)))
    deltas.append(d)

plt.figure()
plt.plot(deltas)
plt.title("Frame-to-Frame Change (Δ)")
plt.xlabel("Frame")
plt.ylabel("Change")

plt.savefig(DELTA_PATH, dpi=200, bbox_inches='tight')
plt.close()

print(f"Delta plot saved at: {DELTA_PATH}")

# ----------------------------
# TRANSITIONS
# ----------------------------
print("\nDetected Transitions:")
for idx, c, d in transition_frames:
    print(f"Frame {idx} | c = {c} | Δ = {d:.4f}")
