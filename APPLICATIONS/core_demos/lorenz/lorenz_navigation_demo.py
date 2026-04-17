"""
NEXAH — Lorenz Navigation Demo

Goal:
Show active navigation in a chaotic Lorenz system.

Pipeline:
- Lorenz dynamics
- phase breaker instability
- coherence / risk
- risk-gradient control
- controlled navigation path

This is the first real navigation demo.
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
# 2. COHERENCE / RISK
# ==================================================

def compute_coherence(x, dx_obs):
    dx_field = lorenz(x)
    num = np.dot(dx_obs, dx_field)
    denom = np.linalg.norm(dx_obs) * np.linalg.norm(dx_field) + 1e-8
    return num / denom

def compute_risk(x, dx_obs):
    return 1 - compute_coherence(x, dx_obs)


# ==================================================
# 3. GRADIENT OF RISK (NAVIGATION CORE)
# ==================================================

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
# 4. PHASE BREAKER
# ==================================================

def phase_breaker(step, x):
    forcing = np.array([
        np.sin(0.01 * step),
        np.cos(0.015 * step),
        0.5 * np.sin(0.02 * step)
    ])

    asymmetry = np.array([
        0.2 * x[0],
        -0.1 * x[1],
        0.05 * x[2]
    ])

    return forcing + asymmetry


# ==================================================
# 5. SIMULATION WITH NAVIGATION
# ==================================================

def run_navigation():

    dt = 0.01
    steps = 5000

    noise_strength = 5.0
    control_strength = 0.5  # 🔥 navigation strength

    x = np.array([1.0, 1.0, 1.0])

    traj = []
    risk_list = []
    coherence_list = []

    for step in range(steps):

        dx = lorenz(x)

        noise = noise_strength * np.random.randn(3)
        dx_obs = dx + noise

        # 🔥 PHASE BREAKER
        dx_obs += phase_breaker(step, x)

        # metrics BEFORE update
        c = compute_coherence(x, dx_obs)
        r = 1 - c

        # 🔥 NAVIGATION CONTROL
        g = grad_risk(x, dx_obs)
        u = -control_strength * g

        # update system
        x = x + dt * (dx_obs + u)

        traj.append(x.copy())
        risk_list.append(r)
        coherence_list.append(c)

    return (
        np.array(traj),
        np.array(risk_list),
        np.array(coherence_list)
    )


# ==================================================
# 6. RUN
# ==================================================

print("\n🧠 Running NEXAH Navigation Demo...\n")

trajectory, risk, coherence = run_navigation()


# ==================================================
# 7. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 10))


# ----------------------------------------
# A. 3D TRAJECTORY (CONTROLLED)
# ----------------------------------------

ax1 = fig.add_subplot(221, projection='3d')

for i in range(len(trajectory) - 1):
    color = plt.cm.inferno(risk[i] / (np.max(risk) + 1e-8))

    ax1.plot(
        trajectory[i:i+2, 0],
        trajectory[i:i+2, 1],
        trajectory[i:i+2, 2],
        color=color,
        linewidth=0.6
    )

ax1.set_title("Controlled Navigation (colored by Risk)")


# ----------------------------------------
# B. XY PROJECTION
# ----------------------------------------

ax2 = fig.add_subplot(222)

ax2.plot(
    trajectory[:, 0],
    trajectory[:, 1],
    color="cyan",
    linewidth=0.7
)

ax2.set_title("XY Projection (Navigation Path)")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")


# ----------------------------------------
# C. RISK OVER TIME
# ----------------------------------------

ax3 = fig.add_subplot(223)

ax3.plot(risk, color="red")
ax3.set_title("Risk over Time")


# ----------------------------------------
# D. COHERENCE OVER TIME
# ----------------------------------------

ax4 = fig.add_subplot(224)

ax4.plot(coherence, color="cyan")
ax4.set_title("Coherence over Time")


plt.tight_layout()

output_path = "APPLICATIONS/outputs/lorenz_navigation_demo.png"
plt.savefig(output_path, dpi=150)

print("Saved:", output_path)

plt.show()


# ==================================================
# 8. OUTPUT
# ==================================================

print("\n--- NAVIGATION RESULTS ---")
print("Mean coherence:", np.mean(coherence))
print("Min coherence:", np.min(coherence))
print("Mean risk:", np.mean(risk))
print("Max risk:", np.max(risk))


print("""
🧭 Interpretation:

The system is no longer passively evolving.

It actively:
- detects instability (risk)
- computes local gradients
- moves toward stability

----------------------------------------

🧠 Key Insight:

Navigation emerges from:

    u = -∇ risk

NOT from external targets.

----------------------------------------

🚀 Meaning:

This is NOT control in the classical sense.

This is:
→ field-based navigation in a dynamical system
""")
