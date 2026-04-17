"""
NEXAH — Lorenz Orbit Phase Map Demo

Goal:
Convert micro-structure (risk) into continuous phase regions.

We visualize:
- trajectory colored by phase
- smooth segmentation of the attractor
- internal "zones" of chaotic motion

This reveals:
→ hidden structure inside chaos
"""

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")


# ==================================================
# 1. LORENZ SYSTEM
# ==================================================

sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

def lorenz(x):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])


# ==================================================
# 2. RISK
# ==================================================

def compute_coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def compute_risk(x, dx_obs):
    return 1 - compute_coherence(x, dx_obs)

def grad_risk(x, dx_obs, eps=1e-3):
    grad = np.zeros(3)

    for i in range(3):
        dx = np.zeros(3)
        dx[i] = eps

        r1 = compute_risk(x + dx, dx_obs)
        r2 = compute_risk(x - dx, dx_obs)

        grad[i] = (r1 - r2) / (2 * eps)

    return grad


# ==================================================
# 3. SIMULATION
# ==================================================

dt = 0.01
steps = 6000

noise_strength = 1.0
control_strength = 0.3

x = np.array([8.0, 8.0, 25.0])  # inside attractor

trajectory = []
risk_series = []

for _ in range(steps):

    dx = lorenz(x)
    noise = noise_strength * np.random.randn(3)

    dx_obs = dx + noise

    r = compute_risk(x, dx_obs)
    g = grad_risk(x, dx_obs)

    u = -control_strength * g

    x = x + dt * (dx_obs + u)

    trajectory.append(x.copy())
    risk_series.append(r)

trajectory = np.array(trajectory)
risk_series = np.array(risk_series)


# ==================================================
# 4. PHASE MAPPING
# ==================================================

# normalize risk to [0,1]
r_min = np.min(risk_series)
r_max = np.max(risk_series)

phase = (risk_series - r_min) / (r_max - r_min + 1e-8)

# optional smoothing (important!)
window = 25
phase_smooth = np.convolve(phase, np.ones(window)/window, mode='same')


# ==================================================
# 5. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 10))


# -----------------------------------
# 3D PHASE MAP
# -----------------------------------

ax = fig.add_subplot(221, projection='3d')

for i in range(len(trajectory) - 1):
    color = plt.cm.plasma(phase_smooth[i])
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        trajectory[i:i+2, 2],
        color=color,
        linewidth=0.6
    )

ax.set_title("Orbit Phase Map (3D)")


# -----------------------------------
# XY PROJECTION (CLEAN VIEW)
# -----------------------------------

ax2 = fig.add_subplot(222)

for i in range(len(trajectory) - 1):
    color = plt.cm.plasma(phase_smooth[i])
    ax2.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        color=color,
        linewidth=0.5
    )

ax2.set_title("Phase Map (XY Projection)")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")


# -----------------------------------
# PHASE OVER TIME
# -----------------------------------

ax3 = fig.add_subplot(223)

ax3.plot(phase_smooth, color="cyan", linewidth=1)
ax3.set_title("Phase over Time")
ax3.set_xlabel("Step")


# -----------------------------------
# HISTOGRAM
# -----------------------------------

ax4 = fig.add_subplot(224)

ax4.hist(phase_smooth, bins=50, color="magenta")
ax4.set_title("Phase Distribution")


plt.tight_layout()

plt.savefig("APPLICATIONS/outputs/lorenz_orbit_phase_map.png", dpi=150)

plt.show()


# ==================================================
# 6. OUTPUT
# ==================================================

print("\n--- ORBIT PHASE MAP ---")
print("Steps:", steps)
print("Mean phase:", np.mean(phase_smooth))
print("Min phase:", np.min(phase_smooth))
print("Max phase:", np.max(phase_smooth))

print("\n🧭 Interpretation:")
print("""
The attractor is no longer uniform.

It contains:
→ continuous phase regions
→ structured orbit segmentation

----------------------------------------

🧠 Key Insight:

Chaos is not random.

It has:
→ internal geometry
→ phase structure
→ navigable regions

----------------------------------------

🚀 Meaning:

This is the bridge to:

- symbolic dynamics
- state graphs
- real navigation systems
""")
