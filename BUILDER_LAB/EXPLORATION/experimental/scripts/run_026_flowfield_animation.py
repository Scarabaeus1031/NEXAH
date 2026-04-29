# run_026_flowfield_animation.py

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# ------------------------------------------------------------
# IMPORT YOUR EXISTING LOGIC
# ------------------------------------------------------------
from run_023_rotation_event_detector import compute_rotation_signal
from run_024_rotation_vs_region_map import compute_regions
from run_017_state_region_map import load_voltage_series  # ggf. anpassen

# ------------------------------------------------------------
# OUTPUT DIR
# ------------------------------------------------------------
OUTPUT_DIR = "../outputs/run_026_flowfield_animation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GIF_PATH = os.path.join(OUTPUT_DIR, "flowfield.gif")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
t, V = load_voltage_series()
dV = np.gradient(V)
ddV = np.gradient(dV)

rotation = compute_rotation_signal(V, dV, ddV)
regions, t_transition, t_collapse = compute_regions(V, dV)

# detect rotation peaks (simple threshold)
threshold = np.mean(rotation) + 2*np.std(rotation)
event_idx = np.where(rotation > threshold)[0]

# ------------------------------------------------------------
# NORMALIZE COLORS
# ------------------------------------------------------------
def get_color(region):
    if region == "stable":
        return "blue"
    elif region == "transition":
        return "orange"
    else:
        return "red"

# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------
frames = []

fig, ax = plt.subplots(figsize=(6, 5))

for i in range(len(t)):

    ax.clear()

    # full trajectory (faint)
    ax.plot(V[:i], dV[:i], color="gray", alpha=0.3)

    # colored trajectory
    for j in range(1, i):
        ax.plot(
            [V[j-1], V[j]],
            [dV[j-1], dV[j]],
            color=get_color(regions[j]),
            linewidth=2
        )

    # current point
    ax.scatter(V[i], dV[i], color="black", s=30)

    # rotation events
    for idx in event_idx:
        if idx < i:
            ax.scatter(V[idx], dV[idx], color="red", s=40)

    # markers
    ax.set_title(f"t = {t[i]:.2f}")
    ax.set_xlabel("V(t)")
    ax.set_ylabel("dV/dt")

    # limits (fix for stable animation)
    ax.set_xlim(np.min(V)-0.5, np.max(V)+0.5)
    ax.set_ylim(np.min(dV)-0.05, np.max(dV)+0.05)

    ax.grid(alpha=0.3)

    # save frame
    fig.canvas.draw()
    frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(frame)

# ------------------------------------------------------------
# SAVE GIF
# ------------------------------------------------------------
imageio.mimsave(GIF_PATH, frames, fps=20)

print("\n=== RUN 026 — FLOWFIELD ANIMATION ===")
print(f"Saved to: {GIF_PATH}")
