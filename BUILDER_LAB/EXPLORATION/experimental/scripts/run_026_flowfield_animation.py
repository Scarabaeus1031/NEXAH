# run_026_flowfield_animation.py

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# ------------------------------------------------------------
# OUTPUT DIR
# ------------------------------------------------------------
OUTPUT_DIR = "../outputs/run_026_flowfield_animation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GIF_PATH = os.path.join(OUTPUT_DIR, "flowfield.gif")

# ------------------------------------------------------------
# DATA (SAME AS YOUR EXPERIMENTS)
# ------------------------------------------------------------
t = np.linspace(0, 100, 500)

# synthetic nonlinear voltage (like before)
V = 1 - 0.002*t - 0.0005*(t**2)

# derivatives
dV = np.gradient(V)
ddV = np.gradient(dV)

# ------------------------------------------------------------
# ROTATION SIGNAL (LOCAL)
# ------------------------------------------------------------
def compute_rotation(V, dV, ddV):
    # simple curvature-like proxy
    rotation = np.abs(dV * ddV)
    return rotation

rotation = compute_rotation(V, dV, ddV)

# detect peaks
threshold = np.mean(rotation) + 2*np.std(rotation)
event_idx = np.where(rotation > threshold)[0]

# ------------------------------------------------------------
# REGION CLASSIFICATION
# ------------------------------------------------------------
def compute_regions(V, dV):
    regions = []

    for i in range(len(V)):
        if i < 0.7*len(V):
            regions.append("stable")
        elif i < 0.85*len(V):
            regions.append("transition")
        else:
            regions.append("collapse")

    return regions

regions = compute_regions(V, dV)

# ------------------------------------------------------------
# COLOR MAP
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

    # faint full path
    ax.plot(V[:i], dV[:i], color="gray", alpha=0.3)

    # colored segments
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

    ax.set_title(f"t = {t[i]:.2f}")
    ax.set_xlabel("V(t)")
    ax.set_ylabel("dV/dt")

    ax.set_xlim(np.min(V)-0.5, np.max(V)+0.5)
    ax.set_ylim(np.min(dV)-0.05, np.max(dV)+0.05)

    ax.grid(alpha=0.3)

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
