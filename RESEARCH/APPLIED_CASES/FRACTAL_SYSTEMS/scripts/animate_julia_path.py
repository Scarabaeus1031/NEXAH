# =========================================================
# NEXAH — Julia Path Animation
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
import imageio.v3 as iio
import os

# =========================================================
# CONFIG
# =========================================================
OUT_DIR = "RESEARCH/APPLIED_CASES/FRACTAL_SYSTEMS/scripts/outputs/"
os.makedirs(OUT_DIR, exist_ok=True)

RES = 500
MAX_ITER = 120
FRAMES = 60

# =========================================================
# JULIA GENERATOR
# =========================================================
def compute_julia(c, res=RES, max_iter=MAX_ITER):
    x = np.linspace(-1.5, 1.5, res)
    y = np.linspace(-1.5, 1.5, res)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    img = np.zeros(Z.shape, dtype=float)

    for i in range(max_iter):
        Z = Z**2 + c
        mask = np.abs(Z) < 10
        img[mask] += 1

    return img


# =========================================================
# PATH IN MANDELBROT SPACE
# =========================================================
def generate_path(n=FRAMES):
    t = np.linspace(0, 2*np.pi, n)

    # Kreis um Boundary (sehr interessante Zone)
    path = -0.75 + 0.3*np.cos(t) + 0.3j*np.sin(t)

    return path


# =========================================================
# FRAME RENDER
# =========================================================
def render_frame(img, c, frame_idx):
    fig, ax = plt.subplots(figsize=(5, 5))

    ax.imshow(img, cmap="magma")
    ax.set_title(f"c = {c.real:.4f} + {c.imag:.4f}i")
    ax.axis("off")

    fname = f"{OUT_DIR}/julia_frame_{frame_idx:03d}.png"
    plt.savefig(fname, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return fname


# =========================================================
# MAIN
# =========================================================
def main():
    print("Generating Julia animation...")

    path = generate_path(FRAMES)
    frame_files = []

    for i, c in enumerate(path):
        print(f"Frame {i+1}/{FRAMES} | c = {c}")

        img = compute_julia(c)
        fname = render_frame(img, c, i)

        frame_files.append(fname)

    # =====================================================
    # CREATE GIF
    # =====================================================
    gif_path = f"{OUT_DIR}/julia_path.gif"

    images = []
    for f in frame_files:
        images.append(iio.imread(f))

    iio.imwrite(gif_path, images, duration=0.06, loop=0)

    print("GIF saved at:", gif_path)


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    main()
