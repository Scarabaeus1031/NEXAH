import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import Counter
import sympy as sp
import os

# ============================================================
# SETTINGS
# ============================================================

N_PRIMES = 500
MOD = 7
FRAMES = 300
OUTPUT_PATH = "output/plots/mod7_structure_flow.gif"

# ============================================================
# GENERATE PRIMES
# ============================================================

primes = list(sp.primerange(1, 10000))[:N_PRIMES]
residues = [p % MOD for p in primes]

# ============================================================
# TRANSITIONS
# ============================================================

transitions = list(zip(residues[:-1], residues[1:]))
counts = Counter(transitions)

# normalize weights
max_count = max(counts.values())
weights = {k: v / max_count for k, v in counts.items()}

# ============================================================
# NODE POSITIONS (CIRCLE)
# ============================================================

angles = {i: 2*np.pi*i/MOD for i in range(MOD)}
positions = {
    i: np.array([np.cos(angles[i]), np.sin(angles[i])])
    for i in range(MOD)
}

# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

ax.set_xticks([])
ax.set_yticks([])

# node scatter
node_scatter = ax.scatter([], [], s=80)

# edges container
lines = []

# ============================================================
# UPDATE FUNCTION
# ============================================================

def update(frame):
    ax.clear()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    angle = frame * 0.02
    R = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)]
    ])

    # transform nodes
    transformed = {
        i: positions[i] @ R.T
        for i in positions
    }

    # draw edges
    for (a, b), w in weights.items():
        p1 = transformed[a]
        p2 = transformed[b]

        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            linewidth=1 + 4*w,
            alpha=0.2 + 0.8*w
        )

    # draw nodes
    xs = [transformed[i][0] for i in range(MOD)]
    ys = [transformed[i][1] for i in range(MOD)]

    ax.scatter(xs, ys, s=80)

    ax.set_title("mod7 Prime Transition Structure")

    return []

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
    plt.show()
