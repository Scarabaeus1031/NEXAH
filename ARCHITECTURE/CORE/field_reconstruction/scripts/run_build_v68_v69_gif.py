# ==========================================================
# NEXAH — Build V68 → V69 Transition GIF (Fixed)
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

OUTPUT_PATH = "visuals/outputs/v68_v69_transition.gif"

N_POINTS = 1500
N_FRAMES = 60

np.random.seed(42)

# ----------------------------------------------------------
# SYNTHETIC STRUCTURE (approximation of v68)
# ----------------------------------------------------------

t = np.linspace(0, 20, N_POINTS)

x = np.sin(t) + 0.3 * np.random.randn(N_POINTS)
y = np.cos(t) + 0.3 * np.random.randn(N_POINTS)

# normalize
x = (x - x.mean()) / x.std()
y = (y - y.mean()) / y.std()

# ----------------------------------------------------------
# FLOW FIELD (approximation of v69)
# ----------------------------------------------------------

def compute_flow(x, y):
    u = -y + 0.3 * x
    v = x + 0.3 * y
    return u, v

u, v = compute_flow(x, y)

# normalize vectors
norm = np.sqrt(u**2 + v**2) + 1e-6
u /= norm
v /= norm

# ----------------------------------------------------------
# BUILD FRAMES (FIXED)
# ----------------------------------------------------------

frames = []

fig, ax = plt.subplots(figsize=(6, 6))

for i in range(N_FRAMES):

    alpha = i / (N_FRAMES - 1)

    ax.clear()

    # interpolate movement
    x_new = x + alpha * u * 2.0
    y_new = y + alpha * v * 2.0

    # plot points
    ax.scatter(x_new, y_new, s=3, alpha=0.7)

    # flow appears gradually
    if alpha > 0.2:
        step = max(1, int(25 - 20 * alpha))
        ax.quiver(
            x_new[::step],
            y_new[::step],
            u[::step],
            v[::step],
            angles='xy',
            scale_units='xy',
            scale=6,
            alpha=alpha
        )

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_title(f"NEXAH — Structure → Flow (t={alpha:.2f})")
    ax.axis("off")

    # --- CRITICAL PART ---
    fig.canvas.draw()
    buffer = np.asarray(fig.canvas.buffer_rgba())
    frame = buffer.copy()   # <<< prevents same-frame bug

    frames.append(frame)

plt.close()

# ----------------------------------------------------------
# SAVE GIF (FIXED)
# ----------------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

imageio.mimsave(
    OUTPUT_PATH,
    frames,
    duration=0.05
)

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH — V68 → V69 GIF built (Fixed)")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("Structure transforms into flow")
print("→ geometry becomes movement")
print("→ system reveals directionality")
