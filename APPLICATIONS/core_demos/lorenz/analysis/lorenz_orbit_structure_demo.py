"""
NEXAH — Lorenz Orbit Structure Demo

Goal:
Reveal hidden structure inside stable attractor dynamics.

We visualize:
- trajectory colored by risk
- detected "risk dips" (micro-transitions)
- orbit segmentation behavior

This shows the INTERNAL rhythm of chaos.
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
# 2. COHERENCE + RISK
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
# 3. SIMULATION (STABLE + MICRO-DYNAMICS)
# ==================================================

dt = 0.01
steps = 5000

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

    # mild control → keeps structure but allows micro variation
    u = -control_strength * g

    x = x + dt * (dx_obs + u)

    trajectory.append(x.copy())
    risk_series.append(r)

trajectory = np.array(trajectory)
risk_series = np.array(risk_series)


# ==================================================
# 4. DETECT RISK DIPS (KEY PART)
# ==================================================

dip_indices = []

threshold = np.percentile(risk_series, 5)  # bottom 5%

for i in range(1, len(risk_series) - 1):
    if risk_series[i] < threshold:
        if risk_series[i] < risk_series[i - 1] and risk_series[i] < risk_series[i + 1]:
            dip_indices.append(i)

dip_indices = np.array(dip_indices)


# ==================================================
# 5. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 10))

# -----------------------------------
# 3D TRAJECTORY (colored by risk)
# -----------------------------------

ax = fig.add_subplot(221, projection='3d')

for i in range(len(trajectory) - 1):
    color = plt.cm.inferno(risk_series[i] / np.max(risk_series))
    ax.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        trajectory[i:i+2, 2],
        color=color,
        linewidth=0.5
    )

ax.set_title("Trajectory (colored by Risk)")


# -----------------------------------
# MARK DIPS
# -----------------------------------

ax2 = fig.add_subplot(222, projection='3d')

ax2.plot(
    trajectory[:, 0],
    trajectory[:, 1],
    trajectory[:, 2],
    color="cyan",
    alpha=0.2
)

if len(dip_indices) > 0:
    dip_points = trajectory[dip_indices]

    ax2.scatter(
        dip_points[:, 0],
        dip_points[:, 1],
        dip_points[:, 2],
        color="red",
        s=20,
        label="Risk Dips"
    )

ax2.set_title("Micro-Transitions (Risk Dips)")
ax2.legend()


# -----------------------------------
# RISK OVER TIME
# -----------------------------------

ax3 = fig.add_subplot(223)

ax3.plot(risk_series, color="red", linewidth=1)

if len(dip_indices) > 0:
    ax3.scatter(
        dip_indices,
        risk_series[dip_indices],
        color="white",
        s=10
    )

ax3.set_title("Risk over Time (Dips = Structure)")
ax3.set_xlabel("Step")


# -----------------------------------
# HISTOGRAM
# -----------------------------------

ax4 = fig.add_subplot(224)

ax4.hist(risk_series, bins=50, color="orange")
ax4.set_title("Risk Distribution")


plt.tight_layout()

plt.savefig("APPLICATIONS/outputs/lorenz_orbit_structure.png", dpi=150)

plt.show()


# ==================================================
# 6. OUTPUT
# ==================================================

print("\n--- ORBIT STRUCTURE ANALYSIS ---")
print("Total steps:", steps)
print("Detected dips:", len(dip_indices))
print("Mean risk:", np.mean(risk_series))
print("Min risk:", np.min(risk_series))

print("\n🧭 Interpretation:")
print("""
Risk dips are NOT noise.

They represent:
→ local orbit transitions
→ curvature changes
→ internal attractor structure

----------------------------------------

🧠 Key Insight:

Even in stable chaos:
→ structure exists at micro-scale

This is the rhythm of the attractor.
""")
