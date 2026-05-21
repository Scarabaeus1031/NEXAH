#!/usr/bin/env python3
"""
NEXAH Mandelbrot–Julia Contact Lab
----------------------------------
Generates a cinematic scientific visualization showing:

Mandelbrot boundary contact -> Julia local weather -> oval containment field.

Outputs:
  1. static contact atlas PNG
  2. optional animated GIF of boundary points / Julia morphing

Run:
  python nexah_mandelbrot_julia_contact_lab.py
  python nexah_mandelbrot_julia_contact_lab.py --gif
  python nexah_mandelbrot_julia_contact_lab.py --hires --gif

Dependencies:
  pip install numpy matplotlib pillow
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle
from matplotlib.animation import FuncAnimation, PillowWriter


def mandelbrot(xmin, xmax, ymin, ymax, w=1000, h=760, max_iter=240):
    x = np.linspace(xmin, xmax, w)
    y = np.linspace(ymin, ymax, h)
    c = x[None, :] + 1j * y[:, None]
    z = np.zeros_like(c)
    m = np.zeros(c.shape, dtype=float)
    mask = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c[mask]
        escaped = np.abs(z) > 2
        newly = mask & escaped
        if np.any(newly):
            m[newly] = i + 1 - np.log2(np.log(np.abs(z[newly])) + 1e-12)
        mask &= ~escaped

    m[mask] = max_iter
    return x, y, m


def julia(c, xmin=-1.55, xmax=1.55, ymin=-1.55, ymax=1.55, w=320, h=320, max_iter=180):
    x = np.linspace(xmin, xmax, w)
    y = np.linspace(ymin, ymax, h)
    z = x[None, :] + 1j * y[:, None]
    m = np.zeros(z.shape, dtype=float)
    mask = np.ones(z.shape, dtype=bool)

    for i in range(max_iter):
        z[mask] = z[mask] * z[mask] + c
        escaped = np.abs(z) > 2
        newly = mask & escaped
        if np.any(newly):
            m[newly] = i + 1 - np.log2(np.log(np.abs(z[newly])) + 1e-12)
        mask &= ~escaped

    m[mask] = max_iter
    return m


def make_contact_atlas(outdir: Path, hires: bool = False):
    outdir.mkdir(parents=True, exist_ok=True)

    if hires:
        dpi = 220
        main_w, main_h = 1300, 950
        zoom_w = zoom_h = 850
        julia_w = 360
    else:
        dpi = 160
        main_w, main_h = 900, 680
        zoom_w = zoom_h = 620
        julia_w = 260

    # Carefully chosen near-boundary parameters.
    c_values = [
        -0.75 + 0.10j,
        -0.74543 + 0.11301j,
        -0.70176 - 0.3842j,
        -0.123 + 0.745j,
        0.285 + 0.01j,
        -0.8 + 0.156j,
    ]

    print("[1/4] Computing Mandelbrot global map...")
    x, y, m = mandelbrot(-2.1, 0.75, -1.25, 1.25, main_w, main_h, 240)

    print("[2/4] Computing Mandelbrot boundary zoom...")
    xz, yz, mz = mandelbrot(-0.82, -0.70, 0.05, 0.19, zoom_w, zoom_h, 380)

    print("[3/4] Computing Julia local regimes...")
    j_maps = [julia(c, w=julia_w, h=julia_w, max_iter=190) for c in c_values]

    fig = plt.figure(figsize=(18, 11), dpi=dpi, facecolor="#05070b")
    gs = fig.add_gridspec(
        3, 6,
        height_ratios=[1.08, 1.08, 0.55],
        wspace=0.08,
        hspace=0.12,
    )

    ax_main = fig.add_subplot(gs[0:2, 0:3])
    ax_zoom = fig.add_subplot(gs[0:2, 3:5])
    ax_oval = fig.add_subplot(gs[0:2, 5])
    j_axes = [fig.add_subplot(gs[2, i]) for i in range(6)]

    for ax in [ax_main, ax_zoom, ax_oval] + j_axes:
        ax.set_facecolor("#070b12")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#1b2b34")

    fig.suptitle(
        "NEXAH Mandelbrot–Julia Contact Lab",
        color="#f3d18a",
        fontsize=22,
        y=0.985,
    )
    fig.text(
        0.5,
        0.952,
        "Boundary contact becomes local Julia weather — one equation, many regimes.",
        ha="center",
        color="#9ad7ff",
        fontsize=10,
    )

    # Main Mandelbrot panel
    ax_main.imshow(
        m,
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        cmap="inferno",
        vmin=0,
        vmax=95,
    )
    ax_main.set_title("Mandelbrot Set — global stability map", color="#f3d18a", fontsize=12)
    ax_main.set_xlim(-2.05, 0.72)
    ax_main.set_ylim(-1.22, 1.22)

    for idx, c in enumerate(c_values):
        ax_main.scatter([c.real], [c.imag], s=44, c="#5ef0ff", edgecolors="white", linewidths=0.45, zorder=4)
        ax_main.text(c.real + 0.03, c.imag + 0.03, f"J{idx+1}", color="#eafcff", fontsize=8)

    ax_main.add_patch(Ellipse((-0.38, 0.0), 1.65, 1.92, fill=False, edgecolor="#5ef0ff", lw=1.0, alpha=0.50))
    ax_main.add_patch(Ellipse((-0.38, 0.0), 1.25, 1.46, fill=False, edgecolor="#ffd166", lw=0.7, alpha=0.35))
    ax_main.text(
        -1.96,
        -1.12,
        "Mandelbrot = global map. Contact points seed local Julia regimes.",
        color="#b6c7d7",
        fontsize=9,
    )

    # Zoom panel
    ax_zoom.imshow(
        mz,
        extent=[xz.min(), xz.max(), yz.min(), yz.max()],
        origin="lower",
        cmap="magma",
        vmin=0,
        vmax=170,
    )
    ax_zoom.set_title("Boundary Zoom — recursion hides full copies inside edges", color="#ff8bd1", fontsize=12)
    ax_zoom.set_xlim(-0.82, -0.70)
    ax_zoom.set_ylim(0.05, 0.19)

    near = [
        (-0.74543 + 0.11301j, "A", "#5ef0ff"),
        (-0.743643887037151 + 0.13182590420533j, "B", "#ffd166"),
    ]
    for c, lab, col in near:
        ax_zoom.scatter([c.real], [c.imag], s=55, c=col, edgecolors="white", linewidths=0.55)
        ax_zoom.text(c.real + 0.002, c.imag + 0.002, lab, color=col, fontsize=11)

    ax_zoom.text(
        -0.817,
        0.056,
        "Surprise: the edge is not a line — it is a generator of worlds.",
        color="#e8d7ff",
        fontsize=8,
    )

    # Oval mechanism panel
    ax_oval.set_title("OVAL CONTACT MECHANISM", color="#5ef0ff", fontsize=11)
    ax_oval.set_xlim(-1.2, 1.2)
    ax_oval.set_ylim(-1.65, 1.65)
    ax_oval.set_aspect("equal")

    for i in range(8):
        ax_oval.add_patch(
            Ellipse(
                (0, 0),
                1.12 + i * 0.06,
                2.18 + i * 0.075,
                fill=False,
                edgecolor="#5ef0ff",
                lw=0.8,
                alpha=0.10 + i * 0.04,
            )
        )

    for rr, alpha in zip(np.linspace(0.08, 0.42, 8), np.linspace(0.65, 0.03, 8)):
        ax_oval.add_patch(Circle((0, 0), rr, color="#ffb000", alpha=alpha))
    ax_oval.scatter([0], [0], s=85, c="#fff4bf")

    ax_oval.scatter([-1.02], [0.05], s=70, c="#ffd166", edgecolors="white", linewidths=0.45)
    ax_oval.scatter([1.02], [-0.05], s=70, c="#ff4bd8", edgecolors="white", linewidths=0.45)
    ax_oval.plot([-1.02, 0, 1.02], [0.05, 0, -0.05], color="#f3d18a", lw=1.15, alpha=0.82)
    ax_oval.plot([-0.8, 0.72], [0.65, -0.84], color="#5ef0ff", lw=0.9, alpha=0.7)

    ax_oval.text(0, -0.16, "7.83", ha="center", color="#ffd166", fontsize=14)
    ax_oval.text(-1.08, 0.18, "M", color="#ffd166", fontsize=10)
    ax_oval.text(1.0, 0.08, "J", color="#ff8bd1", fontsize=10)
    ax_oval.text(0, -1.5, "boundary contact → gate → local weather", color="#b6c7d7", ha="center", fontsize=8)

    # Julia strip
    for i, ax in enumerate(j_axes):
        c = c_values[i]
        ax.imshow(
            j_maps[i],
            extent=[-1.55, 1.55, -1.55, 1.55],
            origin="lower",
            cmap="twilight_shifted",
            vmin=0,
            vmax=85,
        )
        ax.set_title(f"J{i+1}  c={c.real:.3f}{c.imag:+.3f}i", color="#e8d7ff", fontsize=7)
        ax.text(0, -1.37, "local regime", color="#9ad7ff", fontsize=7, ha="center")

    fig.text(
        0.5,
        0.075,
        "Mandelbrot = global map   •   Julia = local weather   •   boundary contact = regime switch",
        ha="center",
        color="#f3d18a",
        fontsize=11,
    )

    out_png = outdir / "nexah_mandelbrot_julia_contact_lab.png"
    plt.savefig(out_png, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[4/4] Saved {out_png}")
    return out_png


def make_morph_gif(outdir: Path, hires: bool = False):
    outdir.mkdir(parents=True, exist_ok=True)

    frames = 72 if not hires else 120
    w = 320 if not hires else 460
    max_iter = 160 if not hires else 220

    # A path walking along interesting near-boundary values.
    anchors = np.array([
        -0.75 + 0.10j,
        -0.74543 + 0.11301j,
        -0.743643887037151 + 0.13182590420533j,
        -0.70176 - 0.3842j,
        -0.123 + 0.745j,
        0.285 + 0.01j,
        -0.8 + 0.156j,
        -0.75 + 0.10j,
    ], dtype=complex)

    # Smooth interpolation between anchors.
    path = []
    steps_per = frames // (len(anchors) - 1)
    for a, b in zip(anchors[:-1], anchors[1:]):
        for k in range(steps_per):
            u = k / steps_per
            u = 0.5 - 0.5 * np.cos(np.pi * u)
            path.append(a * (1 - u) + b * u)
    path = np.array(path[:frames])

    fig = plt.figure(figsize=(8, 8), dpi=130, facecolor="#05070b")
    gs = fig.add_gridspec(2, 1, height_ratios=[0.16, 1.0], hspace=0.05)
    ax_text = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])

    for a in (ax_text, ax):
        a.set_facecolor("#070b12")
        a.set_xticks([])
        a.set_yticks([])
        for s in a.spines.values():
            s.set_color("#1b2b34")

    ax_text.text(0.5, 0.65, "NEXAH Julia Weather Morph", ha="center", color="#f3d18a", fontsize=15)
    c_label = ax_text.text(0.5, 0.20, "", ha="center", color="#9ad7ff", fontsize=9)

    im = ax.imshow(
        np.zeros((w, w)),
        extent=[-1.55, 1.55, -1.55, 1.55],
        origin="lower",
        cmap="twilight_shifted",
        vmin=0,
        vmax=85,
    )

    # Subtle oval shell overlay
    for i in range(4):
        ax.add_patch(Ellipse((0, 0), 1.6 + i * 0.10, 2.25 + i * 0.12, fill=False, edgecolor="#5ef0ff", alpha=0.12 + i * 0.04, lw=0.8))
    ax.scatter([0], [0], s=36, c="#ffd166", alpha=0.7)

    def update(frame):
        c = path[frame]
        m = julia(c, w=w, h=w, max_iter=max_iter)
        im.set_data(m)
        c_label.set_text(f"c = {c.real:.6f} {c.imag:+.6f}i   |   tiny parameter motion → changing local world")
        return [im, c_label]

    ani = FuncAnimation(fig, update, frames=len(path), interval=80, blit=False)
    out_gif = outdir / "nexah_julia_weather_morph.gif"
    ani.save(out_gif, writer=PillowWriter(fps=14))
    plt.close(fig)
    print(f"Saved {out_gif}")
    return out_gif


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", default="nexah_mandelbrot_output", help="Output directory")
    parser.add_argument("--hires", action="store_true", help="Higher resolution, slower")
    parser.add_argument("--gif", action="store_true", help="Also render Julia morph GIF")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    make_contact_atlas(outdir, hires=args.hires)
    if args.gif:
        make_morph_gif(outdir, hires=args.hires)


if __name__ == "__main__":
    main()
