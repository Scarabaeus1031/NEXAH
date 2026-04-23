# ==========================================================
# NEXAH — REAL V68 → V69 Transition (IEEE Data)
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/ieee118_v68_off_manifold_cloud.csv"
OUTPUT_PATH = "visuals/outputs/v68_v69_real_transition.gif"

N_FRAMES = 120
STEP_SCALE = 0.5

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

# 👇 anpassen je nach CSV Struktur
x = df.iloc[:, 0].values
y = df.iloc[:, 1].values

# normalize
x = (x - x.mean()) / x.std()
y = (y - y.mean()) / y.std()

# ----------------------------------------------------------
# ESTIMATE FLOW (KEY IDEA)
# ----------------------------------------------------------

# approximate flow via local gradient / direction
dx = np.gradient(x)
dy = np.gradient(y)

# normalize vectors
norm = np.sqrt(dx**2 + dy**2) + 1e-6
u = dx / norm
v = dy / norm

# ----------------------------------------------------------
# BUILD FRAMES
# ----------------------------------------------------------

frames = []
fig, ax = plt.subplots(figsize=(6, 6))

for i in range(N_FRAMES):

    alpha = i / (N_FRAMES - 1)

    ax.clear()

    # movement along estimated flow
    x_new = x + alpha * u * STEP_SCALE
    y_new = y + alpha * v * STEP_SCALE

    # points
    ax.scatter(x_new, y_new, s=2, alpha=0.6)

    # flow overlay
    if alpha > 0.2:
        step = max(1, int(40 - 30 * alpha))
        ax.quiver(
            x_new[::step],
            y_new[::step],
            u[::step],
            v[::step],
            scale=20,
            alpha=alpha
        )

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_title("NEXAH — IEEE Structure → Flow")
    ax.axis("off")

    fig.canvas.draw()
    buffer = np.asarray(fig.canvas.buffer_rgba())
    frame = buffer.copy()

    frames.append(frame)

plt.close()

# ----------------------------------------------------------
# SAVE GIF
# ----------------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

imageio.mimsave(
    OUTPUT_PATH,
    frames,
    duration=0.04
)

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH — REAL IEEE GIF built")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("Flow is derived from real system evolution")
print("→ structure encodes direction")
print("→ field is implicit in data")
