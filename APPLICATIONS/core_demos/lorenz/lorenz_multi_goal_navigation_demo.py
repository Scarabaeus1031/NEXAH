"""
NEXAH — Lorenz Multi-Goal Navigation Demo

Goal:
Adaptive navigation with MULTIPLE goals.

Pipeline:
- symbolic states
- dynamic goal switching
- exploration vs stabilization
- adaptive control

This is:
GRAPH → CONTEXT → GOAL SWITCH → BEHAVIOR
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


# ==================================================
# 3. BASE DATA (for phase mapping)
# ==================================================

dt = 0.01
steps = 6000

x = np.array([8.0, 8.0, 25.0])

risk_series = []

for _ in range(steps):
    dx = lorenz(x)
    dx_obs = dx + np.random.randn(3)
    r = compute_risk(x, dx_obs)

    x = x + dt * dx_obs
    risk_series.append(r)

risk_series = np.array(risk_series)


# ==================================================
# 4. PHASE → STATES
# ==================================================

sorted_idx = np.argsort(risk_series)
rank = np.empty_like(sorted_idx)
rank[sorted_idx] = np.arange(len(risk_series))

phase = rank / (len(risk_series) - 1)
phase_smooth = np.convolve(phase, np.ones(25)/25, mode="same")

N_STATES = 6


def risk_to_state(r):
    p = np.sum(risk_series < r) / len(risk_series)
    s = int(np.clip(np.floor(p * N_STATES), 0, N_STATES-1))
    return s


# ==================================================
# 5. MULTI-GOAL LOGIC
# ==================================================

def select_goal(r, s):
    """
    Adaptive goal selection
    """

    # 🔥 HIGH RISK → go to stability
    if r > 0.05:
        return 0  # S0

    # 🔥 VERY LOW RISK → explore
    if r < 0.005:
        return 5  # S5

    # 🔥 OTHERWISE → stay mid
    return s


# ==================================================
# 6. NAVIGATION
# ==================================================

x = np.array([12.0, 12.0, 30.0])

trajectory = []
states = []
risk_vals = []
goals = []

noise_strength = 1.0
control_strength = 0.6

for _ in range(5000):

    dx = lorenz(x)
    dx_obs = dx + noise_strength * np.random.randn(3)

    r = compute_risk(x, dx_obs)
    s = risk_to_state(r)

    # 🔥 MULTI-GOAL DECISION
    goal = select_goal(r, s)

    # 🔥 CONTROL:
    # stabilize or destabilize depending on goal
    if goal == 0:
        # stabilize → reduce risk
        u = -control_strength * r * dx_obs
    elif goal == 5:
        # explore → increase movement
        u = control_strength * dx_obs
    else:
        # neutral
        u = -0.3 * r * dx_obs

    x = x + dt * (dx_obs + u)

    trajectory.append(x.copy())
    states.append(s)
    risk_vals.append(r)
    goals.append(goal)

trajectory = np.array(trajectory)
risk_vals = np.array(risk_vals)
states = np.array(states)
goals = np.array(goals)


# ==================================================
# 7. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(15, 10))


# --- trajectory ---
ax1 = fig.add_subplot(221, projection="3d")

for i in range(len(trajectory)-1):
    color = plt.cm.plasma(states[i] / (N_STATES-1))
    ax1.plot(
        trajectory[i:i+2,0],
        trajectory[i:i+2,1],
        trajectory[i:i+2,2],
        color=color,
        linewidth=0.5
    )

ax1.set_title("Multi-Goal Navigation")


# --- XY ---
ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:,0], trajectory[:,1], color="cyan")
ax2.set_title("XY Path")


# --- states + goals ---
ax3 = fig.add_subplot(223)
ax3.plot(states, label="State", color="magenta")
ax3.plot(goals, label="Goal", color="yellow", alpha=0.7)
ax3.legend()
ax3.set_title("State vs Goal")


# --- risk ---
ax4 = fig.add_subplot(224)
ax4.plot(risk_vals, color="red")
ax4.set_title("Risk over Time")


plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_multi_goal_navigation.png", dpi=150)
plt.show()


# ==================================================
# 8. OUTPUT
# ==================================================

print("\n--- MULTI-GOAL NAVIGATION ---")
print("Mean risk:", np.mean(risk_vals))
print("Min risk:", np.min(risk_vals))
print("Max risk:", np.max(risk_vals))

print("\n🧭 Interpretation:\n")
print("""
The system is now ADAPTIVE.

It:
- switches goals based on context
- stabilizes when needed
- explores when safe

----------------------------------------

🧠 Key Insight:

This is not control.

This is:
→ BEHAVIOR

----------------------------------------

🚀 Meaning:

You now have:

Dynamics → States → Goals → Switching → Behavior

= Proto-Intelligent System
""")
