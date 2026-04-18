"""
NEXAH — Meta Field Navigation Demo

Goal:
Move from simple gradient following
→ to real navigation behavior

Adds:
- exploration (noise)
- escape mechanism
- meta-field dynamics

This is the first adaptive navigation layer.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

plt.style.use("dark_background")


# ==================================================
# 1. LOAD DENSITY
# ==================================================

print("\n🧠 Loading density field...\n")

density = np.loadtxt(
    "APPLICATIONS/outputs/lorenz_density/lorenz_density.csv",
    delimiter=","
)

field = density / (np.max(density) + 1e-8)
field = gaussian_filter(field, sigma=1.5)


# ==================================================
# 2. GRADIENT
# ==================================================

print("→ Computing gradient...")

grad_y, grad_x = np.gradient(field)


# ==================================================
# 3. START POSITION
# ==================================================

def get_start():
    idx = np.argwhere(field > 0.2)
    p = idx[np.random.randint(len(idx))]
    return np.array([p[1], p[0]], dtype=float)


# ==================================================
# 4. META NAVIGATION
# ==================================================

def run_meta_navigation():

    steps = 5000
    step_size = 0.6

    noise_strength = 0.3
    escape_threshold = 0.65   # risk level
    escape_boost = 3.0

    x = get_start()

    traj = []
    risk = []

    for _ in range(steps):

        ix = int(np.clip(x[0], 0, field.shape[1] - 1))
        iy = int(np.clip(x[1], 0, field.shape[0] - 1))

        # ----------------------------
        # RISK
        # ----------------------------
        r = 1 - field[iy, ix]

        # ----------------------------
        # GRADIENT (stability seeking)
        # ----------------------------
        g = np.array([grad_x[iy, ix], grad_y[iy, ix]])
        norm = np.linalg.norm(g) + 1e-8
        g = g / norm

        # ----------------------------
        # EXPLORATION (noise)
        # ----------------------------
        noise = noise_strength * np.random.randn(2)

        # ----------------------------
        # ESCAPE LOGIC
        # ----------------------------
        if r > escape_threshold:
            # 🔥 push away strongly
            u = escape_boost * (g + noise)
        else:
            # normal movement
            u = g + noise * 0.5

        # update
        x = x + step_size * u

        traj.append(x.copy())
        risk.append(r)

    return np.array(traj), np.array(risk)


print("→ Running META navigation...\n")

trajectory, risk = run_meta_navigation()


# ==================================================
# 5. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(12, 6))

# ----------------------------------------
# FIELD + TRAJECTORY
# ----------------------------------------

ax1 = fig.add_subplot(121)

ax1.imshow(field, origin="lower", cmap="inferno")

ax1.plot(
    trajectory[:, 0],
    trajectory[:, 1],
    color="cyan",
    linewidth=0.8
)

ax1.set_title("Meta Navigation (Exploration + Escape)")


# ----------------------------------------
# RISK
# ----------------------------------------

ax2 = fig.add_subplot(122)

ax2.plot(risk, color="red")
ax2.set_title("Risk over Time (Meta Navigation)")


plt.tight_layout()

output_path = "APPLICATIONS/outputs/lorenz_meta_navigation.png"
plt.savefig(output_path, dpi=150)

print("Saved:", output_path)

plt.show()


# ==================================================
# 6. OUTPUT
# ==================================================

print("\n--- META NAVIGATION ---")
print("Mean risk:", np.mean(risk))
print("Min risk:", np.min(risk))
print("Max risk:", np.max(risk))


print("""
🧭 Interpretation:

The agent is no longer passive.

It now:
- follows structure (gradient)
- explores (noise)
- escapes instability (risk)

----------------------------------------

🧠 Key Insight:

Navigation emerges from:

    stability + exploration + escape

----------------------------------------

🚀 Meaning:

This is the first REAL navigation layer.

System is now:
→ adaptive
→ responsive
→ dynamic
""")
