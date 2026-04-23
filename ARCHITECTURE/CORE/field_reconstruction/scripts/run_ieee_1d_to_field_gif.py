# ==========================================================
# NEXAH — IEEE 1D → Field Transition (REAL DATA)
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "data/ieee_sample.csv"
OUTPUT_PATH = "visuals/outputs/ieee_1d_to_field.gif"

N_FRAMES = 120
STEP_SCALE = 0.3

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

t = df["time"].values.astype(float)
v = df["voltage"].values.astype(float)

# normalize
v = (v - v.mean()) / v.std()

# ----------------------------------------------------------
# BUILD PHASE SPACE (KEY STEP)
# ----------------------------------------------------------

# gradient = dynamics
dv = np.gradient(v)

# this is your 2D system now
x = v
y = dv

# ----------------------------------------------------------
# ESTIMATE FLOW
# ----------------------------------------------------------

dx = np.gradient(x)
dy = np.gradient(y)

norm = np.sqrt(dx**2 + dy**2) + 1e-6
u = dx / norm
v_flow = dy / norm

# ----------------------------------------------------------
# BUILD GIF
# ----------------------------------------------------------

frames = []
fig, ax = plt.subplots(figsize=(6, 6))

for i in range(N_FRAMES):

    alpha = i / (N_FRAMES - 1)

    ax.clear()

    # move points along flow
    x_new = x + alpha * u * STEP_SCALE
    y_new = y + alpha * v_flow * STEP_SCALE

    # base structure (points)
    ax.scatter(x_new, y_new, s=4, alpha=0.6)

    # flow overlay appears gradually
    if alpha > 0.2:
        step = max(1, int(50 - 40 * alpha))

        ax.quiver(
            x_new[::step],
            y_new[::step],
            u[::step],
            v_flow[::step],
            scale=20,
            alpha=alpha
        )

    ax.set_title("NEXAH — Structure → Flow (IEEE real signal)")
    ax.set_xlabel("state (voltage)")
    ax.set_ylabel("dynamics (gradient)")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    ax.grid(alpha=0.2)

    fig.canvas.draw()
    buffer = np.asarray(fig.canvas.buffer_rgba())
    frames.append(buffer.copy())

plt.close()

# ----------------------------------------------------------
# SAVE
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

print("\n⚡ NEXAH — IEEE Field GIF built")
print(f"✔ Saved → {OUTPUT_PATH}")

print("\n🧠 Interpretation:")
print("1D signal unfolds into 2D structure")
print("→ dynamics create geometry")
print("→ geometry reveals flow")
