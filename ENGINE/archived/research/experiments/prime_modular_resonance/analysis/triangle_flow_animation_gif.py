import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# ============================================================
# SETTINGS
# ============================================================

FRAMES = 300
OUTPUT_PATH = "output/plots/mod7_triangle_rotation.gif"

# ============================================================
# BASE TRIANGLE
# ============================================================

triangle = np.array([
    [0.0, 0.4],
    [-0.35, -0.2],
    [0.35, -0.2],
    [0.0, 0.4]
])

# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')

ax.set_xticks([])
ax.set_yticks([])

line, = ax.plot([], [], lw=2)

# ============================================================
# TRANSFORM
# ============================================================

def transform(t):
    angle = t * 0.05
    
    R = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])
    
    drift = np.array([
        0.2 * np.sin(t * 0.03),
        0.2 * np.cos(t * 0.02)
    ])
    
    return (triangle @ R.T) + drift

# ============================================================
# UPDATE
# ============================================================

def update(frame):
    pts = transform(frame)
    line.set_data(pts[:,0], pts[:,1])
    return line,

# ============================================================
# ANIMATION
# ============================================================

ani = FuncAnimation(fig, update, frames=FRAMES, interval=30)

# ============================================================
# SAVE OR SHOW
# ============================================================

if os.environ.get("AUTO_SAVE") == "1":

    os.makedirs("output/plots", exist_ok=True)

    print("[INFO] Saving GIF...")
    ani.save(OUTPUT_PATH, writer='pillow', fps=30)
    print(f"[OK] Saved to {OUTPUT_PATH}")

else:
    plt.title("Triangle Flow (Generator Layer)")
    plt.show()
