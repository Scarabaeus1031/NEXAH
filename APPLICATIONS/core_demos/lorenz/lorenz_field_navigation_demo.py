"""
NEXAH — Field-Based Navigation Demo (Stable Version)

Fixes:
- smart start inside attractor
- gradient stabilization
- optional smoothing

This is the first TRUE field navigation.
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

# normalize
field = density / (np.max(density) + 1e-8)

# 🔥 optional smoothing (important!)
field = gaussian_filter(field, sigma=1.5)


# ==================================================
# 2. COMPUTE GRADIENT FIELD
# ==================================================

print("→ Computing gradient field...")

grad_y, grad_x = np.gradient(field)


# ==================================================
# 3. SMART START (ATTRACTOR ENTRY)
# ==================================================

def get_start_position():

    # find high-density region
    indices = np.argwhere(field > 0.2)

    if len(indices) > 0:
        idx = indices[np.random.randint(len(indices))]
        print("→ Starting inside attractor")
        return np.array([idx[1], idx[0]], dtype=float)

    # fallback (your "start chord")
    print("⚠️ fallback start (2,1,3 projection)")
    return np.array([150.0, 150.0])  # center-ish


# ==================================================
# 4. NAVIGATION
# ==================================================

def run_field_navigation():

    steps = 4000
    step_size = 0.6

    x = get_start_position()

    traj = []
    risk = []

    for _ in range(steps):

        ix = int(np.clip(x[0], 0, field.shape[1] - 1))
        iy = int(np.clip(x[1], 0, field.shape[0] - 1))

        r = 1 - field[iy, ix]

        gx = grad_x[iy, ix]
        gy = grad_y[iy, ix]

        g = np.array([gx, gy])

        # normalize
        norm = np.linalg.norm(g) + 1e-8
        g = g / norm

        # 🔥 boost movement
        g = g * 2.0

        x = x + step_size * g

        traj.append(x.copy())
        risk.append(r)

    return np.array(traj), np.array(risk)


print("→ Running field navigation...\n")

trajectory, risk = run_field_navigation()


# ==================================================
# 5. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(12, 6))

# FIELD + PATH
ax1 = fig.add_subplot(121)

ax1.imshow(field, origin="lower", cmap="inferno")

ax1.plot(
    trajectory[:, 0],
    trajectory[:, 1],
    color="cyan",
    linewidth=1
)

ax1.set_title("Field Navigation (Stable)")

# RISK
ax2 = fig.add_subplot(122)

ax2.plot(risk, color="red")
ax2.set_title("Risk over Time")

plt.tight_layout()

output_path = "APPLICATIONS/outputs/lorenz_field_navigation.png"
plt.savefig(output_path, dpi=150)

print("Saved:", output_path)

plt.show()


# ==================================================
# 6. OUTPUT
# ==================================================

print("\n--- FIELD NAVIGATION ---")
print("Mean risk:", np.mean(risk))
print("Min risk:", np.min(risk))


print("""
🧭 Interpretation:

Agent starts inside structure.

It:
- detects density
- follows gradient
- stabilizes in attractor

----------------------------------------

🧠 Key Insight:

Navigation requires:

1. field
2. gradient
3. correct entry

----------------------------------------

🚀 Meaning:

This is the first stable NEXAH field navigation.
""")
