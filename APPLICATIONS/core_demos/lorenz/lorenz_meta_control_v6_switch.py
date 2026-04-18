"""
NEXAH — Lorenz Meta Control v6 (Switch Awareness)

Improved Version:
- proper switch scaling
- stable reward learning
- bounded mode scores
- plot saving fixed
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

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
# 2. SETTINGS
# ==================================================

dt = 0.005
steps = 6000
N_STATES = 6

x = np.array([1.0, 1.0, 1.0], dtype=float)

trajectory = []
risk_list = []
switch_list = []
mode_list = []

modes = ["predictive", "stabilize", "none", "switch"]

mode_scores = {m: 1.0 for m in modes}
transition_memory = {}

last_state = None
prev_x = x.copy()
prev_risk = None


# ==================================================
# 3. HELPERS
# ==================================================

def compute_state(x):
    x0 = np.clip(x[0], -30, 30)
    bins = np.linspace(-30, 30, N_STATES + 1)
    return int(np.digitize(x0, bins[1:-1]))

def compute_risk(dx):
    return np.linalg.norm(dx)

def safe_clip(v, max_val=50):
    return np.clip(v, -max_val, max_val)


# ==================================================
# 4. MAIN LOOP
# ==================================================

for t in range(steps):

    dx = lorenz(x)
    dx = safe_clip(dx, 50)

    state = compute_state(x)
    risk = compute_risk(dx)

    # ============================================
    # SWITCH DETECTION (IMPROVED)
    # ============================================

    if last_state is None:
        switch_strength = 0.0
    else:
        state_jump = abs(state - last_state)
        position_jump = np.linalg.norm(x - prev_x)

        switch_strength = 2.0 * state_jump + 0.3 * position_jump

    switch_list.append(switch_strength)

    # ============================================
    # MODE SCORING
    # ============================================

    scores = {}

    for m in modes:

        score = mode_scores[m]

        if m == "switch" and switch_strength > 2.5:
            score += 1.2

        if m == "stabilize" and risk > 50:
            score += 0.5

        if m == "predictive" and risk < 40:
            score += 0.3

        scores[m] = score

    # softmax selection
    keys = list(scores.keys())
    vals = np.array([scores[k] for k in keys])
    vals = np.exp(vals - np.max(vals))
    probs = vals / np.sum(vals)

    mode = np.random.choice(keys, p=probs)

    # ============================================
    # CONTROL
    # ============================================

    if mode == "switch":
        control = -0.8 * dx
    elif mode == "stabilize":
        control = -0.4 * dx
    elif mode == "predictive":
        control = -0.25 * dx
    else:
        control = np.zeros(3)

    control = safe_clip(control, 20)

    # ============================================
    # UPDATE SYSTEM
    # ============================================

    step_update = (dx + control) * dt
    step_update = safe_clip(step_update, 5)

    x = x + step_update

    # ============================================
    # LEARNING (FIXED)
    # ============================================

    if prev_risk is not None:

        reward = (prev_risk - risk) * 0.01  # improvement-based

        mode_scores[mode] += reward

        # clamp scores (critical for stability)
        for m in mode_scores:
            mode_scores[m] = float(np.clip(mode_scores[m], -5.0, 5.0))

    prev_risk = risk
    last_state = state
    prev_x = x.copy()

    # ============================================
    # LOGGING
    # ============================================

    trajectory.append(x.copy())
    risk_list.append(risk)
    mode_list.append(mode)

trajectory = np.array(trajectory)


# ==================================================
# 5. PLOTTING
# ==================================================

fig = plt.figure(figsize=(14, 10))

# 3D Trajectory
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], color="cyan")
ax1.set_title("v6 Switch-Aware Trajectory")

# XY Path
ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:, 0], trajectory[:, 1], color="cyan")
ax2.set_title("XY Path")

# Risk
ax3 = fig.add_subplot(223)
ax3.plot(risk_list, color="red")
ax3.set_title("Risk")

# Switch Strength
ax4 = fig.add_subplot(224)
ax4.plot(switch_list, color="yellow")
ax4.set_title("Switch Strength")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control_v6_switch.png", dpi=150)
plt.show()


# ==================================================
# 6. OUTPUT
# ==================================================

print("\n--- META CONTROL v6 (SWITCH, FIXED) ---")
print("Mean risk:", np.mean(risk_list))
print("Max switch strength:", np.max(switch_list))

print("\nMode scores:")
for m, s in mode_scores.items():
    print(f"{m} → {round(s, 3)}")

print("Modes used:", set(mode_list))
