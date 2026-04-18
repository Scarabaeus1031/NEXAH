"""
NEXAH — Lorenz Meta Control v3 (Learning)

Goal:
System learns which control mode works best.

New:
- mode scoring
- reward-based adaptation
- behavior evolution
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.style.use("dark_background")

# ==================================================
# LORENZ SYSTEM
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
# SETTINGS
# ==================================================

dt = 0.005
steps = 6000

x = np.array([1.0, 1.0, 1.0])

trajectory = []
risk_list = []
mode_list = []
mode_score_history = []

# ==================================================
# LEARNING STRUCTURE
# ==================================================

modes = ["entropy", "uncertainty", "predictive", "stabilize", "none"]

mode_scores = {m: 1.0 for m in modes}

learning_rate = 0.01

# ==================================================
# HELPERS
# ==================================================

def compute_risk(dx):
    return np.linalg.norm(dx)

def compute_entropy():
    p = np.random.dirichlet(np.ones(6))
    return -np.sum(p * np.log(p + 1e-8))

def compute_confidence(x):
    return 1.0 - (abs(x[0]) % 6) / 6.0

def safe_clip(v, max_val=50):
    return np.clip(v, -max_val, max_val)

def softmax(scores):
    s = np.array(list(scores.values()))
    exp = np.exp(s - np.max(s))
    probs = exp / np.sum(exp)
    return dict(zip(scores.keys(), probs))


# ==================================================
# MAIN LOOP
# ==================================================

prev_risk = None

for i in range(steps):

    dx = lorenz(x)
    dx = safe_clip(dx, 50)

    entropy = compute_entropy()
    confidence = compute_confidence(x)
    risk = compute_risk(dx)

    # ==================================================
    # MODE SELECTION (learned)
    # ==================================================

    mode_probs = softmax(mode_scores)
    chosen_mode = np.random.choice(list(mode_probs.keys()), p=list(mode_probs.values()))

    # ==================================================
    # CONTROL
    # ==================================================

    if chosen_mode == "entropy":
        control = -dx * 0.6

    elif chosen_mode == "uncertainty":
        control = -dx * 0.4

    elif chosen_mode == "predictive":
        control = -dx * 0.3

    elif chosen_mode == "stabilize":
        control = -dx * 0.2

    else:
        control = np.zeros(3)

    control = safe_clip(control, 20)

    # ==================================================
    # UPDATE SYSTEM
    # ==================================================

    step_update = (dx + control) * dt
    step_update = safe_clip(step_update, 5)

    x = x + step_update

    # ==================================================
    # LEARNING STEP (KEY)
    # ==================================================

    if prev_risk is not None:

        delta = prev_risk - risk  # improvement if positive

        # reward / penalty
        mode_scores[chosen_mode] += learning_rate * delta

        # keep scores bounded
        for m in mode_scores:
            mode_scores[m] = np.clip(mode_scores[m], -2.0, 5.0)

    prev_risk = risk

    # ==================================================

    trajectory.append(x.copy())
    risk_list.append(risk)
    mode_list.append(chosen_mode)
    mode_score_history.append(mode_scores.copy())

trajectory = np.array(trajectory)

# ==================================================
# PLOTTING
# ==================================================

fig = plt.figure(figsize=(14, 10))

# 3D trajectory
ax = fig.add_subplot(221, projection='3d')
ax.plot(trajectory[:,0], trajectory[:,1], trajectory[:,2])
ax.set_title("Meta-Control v3 (Learning)")

# XY path
ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:,0], trajectory[:,1])
ax2.set_title("XY Path")

# Risk
ax3 = fig.add_subplot(223)
ax3.plot(risk_list, color="red")
ax3.set_title("Risk over Time")

# Mode scores
ax4 = fig.add_subplot(224)

for m in modes:
    ax4.plot([h[m] for h in mode_score_history], label=m)

ax4.legend()
ax4.set_title("Mode Scores (Learning)")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control_v3_learning.png")
plt.show()

# ==================================================
# OUTPUT
# ==================================================

print("\n--- META CONTROL v3 (LEARNING) ---")
print("Mean risk:", np.mean(risk_list))
print("Final mode scores:")

for m, s in mode_scores.items():
    print(m, "→", round(s, 3))
