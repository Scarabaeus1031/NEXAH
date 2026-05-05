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

OUTPUT_PATH = "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/julia_path_final.gif"

# Mandelbrot sampling grid (für Referenz-Plot)
MAND_RES = 400

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

    # Normalize
    julia_norm = julia / np.max(julia)

    # Detect transition
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

    # Save frame to buffer
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    images.append(image)

    plt.close(fig)

# ----------------------------
# SAVE GIF
# ----------------------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
imageio.mimsave(OUTPUT_PATH, images, fps=10)

print(f"\nGIF saved at: {OUTPUT_PATH}")

# ----------------------------
# EXTRA PLOTS
# ----------------------------

# 1️⃣ Mandelbrot + Path
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
plt.show()

# 2️⃣ Delta Plot
deltas = []
for i in range(1, len(images)):
    d = np.mean(np.abs(images[i].astype(float) - images[i-1].astype(float)))
    deltas.append(d)

plt.figure()
plt.plot(deltas)
plt.title("Frame-to-Frame Change (Δ)")
plt.xlabel("Frame")
plt.ylabel("Change")
plt.show()

# 3️⃣ Transition Printout
print("\nDetected Transitions:")
for idx, c, d in transition_frames:
    print(f"Frame {idx} | c = {c} | Δ = {d:.4f}")
