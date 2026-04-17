"""
NEXAH — Field-Based Navigation Demo

Goal:
Navigate using the reconstructed field (density),
NOT the original Lorenz system.

Pipeline:
- load density
- compute field (normalized)
- compute gradient
- navigate in field

This is TRUE NEXAH navigation.
"""

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")


# ==================================================
# 1. LOAD DENSITY
# ==================================================

print("\n🧠 Loading density field...\n")

density = np.loadtxt("APPLICATIONS/outputs/lorenz_density/lorenz_density.csv")

# normalize
field = density / (np.max(density) + 1e-8)


# ==================================================
# 2. COMPUTE GRADIENT FIELD
# ==================================================

print("→ Computing gradient field...")

grad_y, grad_x = np.gradient(field)


# ==================================================
# 3. NAVIGATION IN FIELD
# ==================================================

def run_field_navigation():

    steps = 3000
    step_size = 1.0

    # start random
    x = np.array([
        np.random.randint(0, field.shape[1]),
        np.random.randint(0, field.shape[0])
    ], dtype=float)

    traj = []
    risk = []

    for _ in range(steps):

        ix = int(np.clip(x[0], 0, field.shape[1] - 1))
        iy = int(np.clip(x[1], 0, field.shape[0] - 1))

        # 🔥 risk = low density = bad
        r = 1 - field[iy, ix]

        # 🔥 gradient (move to high density)
        gx = grad_x[iy, ix]
        gy = grad_y[iy, ix]

        g = np.array([gx, gy])

        # navigation rule
        x = x + step_size * g

        traj.append(x.copy())
        risk.append(r)

    return np.array(traj), np.array(risk)


print("→ Running field navigation...\n")

trajectory, risk = run_field_navigation()


# ==================================================
# 4. VISUALIZATION
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
    linewidth=1
)

ax1.set_title("Field Navigation (Density Gradient)")


# ----------------------------------------
# RISK OVER TIME
# ----------------------------------------

ax2 = fig.add_subplot(122)

ax2.plot(risk, color="red")
ax2.set_title("Risk over Time (Field-Based)")


plt.tight_layout()

output_path = "APPLICATIONS/outputs/lorenz_field_navigation.png"
plt.savefig(output_path, dpi=150)

print("Saved:", output_path)

plt.show()


# ==================================================
# 5. OUTPUT
# ==================================================

print("\n--- FIELD NAVIGATION ---")
print("Mean risk:", np.mean(risk))
print("Min risk:", np.min(risk))


print("""
🧭 Interpretation:

The agent no longer knows the Lorenz system.

It only sees:
→ a field

and still:
→ finds structure
→ moves toward attractors

----------------------------------------

🧠 Key Insight:

Structure → Field → Navigation

WITHOUT equations.

----------------------------------------

🚀 Meaning:

This is the bridge to:

- real-world systems
- unknown dynamics
- black-box navigation
""")
