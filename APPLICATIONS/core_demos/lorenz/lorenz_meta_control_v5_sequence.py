"""
NEXAH — Lorenz Meta Control v5 (Sequence Memory)

Dynamics → States → Sequences → Meta-Control → Memory
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

plt.style.use("dark_background")


# ==================================================
# 1. LORENZ
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
SEQ_LEN = 3

x = np.array([1.0, 1.0, 1.0], dtype=float)

trajectory = []
risk_list = []
mode_list = []
state_list = []
sequence_list = []

global_score_history = []
sequence_score_history = []

modes = ["entropy", "uncertainty", "predictive", "stabilize", "none"]


# ==================================================
# 3. HELPERS
# ==================================================

def safe_clip(v, max_val=50.0):
    return np.clip(v, -max_val, max_val)

def compute_risk(dx):
    return np.linalg.norm(dx)

def compute_symbolic_state(x):
    x0 = np.clip(x[0], -30, 30)
    bins = np.linspace(-30, 30, N_STATES + 1)
    state = np.digitize(x0, bins[1:-1])
    return int(np.clip(state, 0, N_STATES - 1))

def compute_confidence(x):
    return float(np.clip(abs(x[0]) / 20.0, 0.0, 1.0))

def compute_entropy():
    p = np.random.dirichlet(np.ones(N_STATES))
    return -np.sum(p * np.log(p + 1e-8))

def softmax(scores):
    keys = list(scores.keys())
    vals = np.array([scores[k] for k in keys])
    vals -= np.max(vals)
    probs = np.exp(vals) / np.sum(np.exp(vals))
    return keys, probs


# ==================================================
# 4. MEMORY STRUCTURES
# ==================================================

# global mode preference
global_mode_scores = {m: 1.0 for m in modes}

# sequence memory (tuple of states)
sequence_mode_scores = {}

# recent rewards
recent_rewards = {m: [] for m in modes}
recent_window = 25

last_mode = "none"
prev_risk = None

# initial sequence buffer
sequence_buffer = [0] * SEQ_LEN


# ==================================================
# 5. MAIN LOOP
# ==================================================

for t in range(steps):

    dx = safe_clip(lorenz(x), 50)

    state = compute_symbolic_state(x)
    confidence = compute_confidence(x)
    entropy = compute_entropy()
    risk = compute_risk(dx)

    # update sequence buffer
    sequence_buffer.pop(0)
    sequence_buffer.append(state)
    seq_key = tuple(sequence_buffer)

    # initialize sequence if new
    if seq_key not in sequence_mode_scores:
        sequence_mode_scores[seq_key] = {m: 1.0 for m in modes}

    # ==================================================
    # SCORE BUILDING
    # ==================================================

    combined_scores = {}

    for m in modes:

        recent_avg = np.mean(recent_rewards[m]) if recent_rewards[m] else 0

        score = (
            0.4 * global_mode_scores[m]
            + 0.5 * sequence_mode_scores[seq_key][m]
            + 0.1 * recent_avg
        )

        # stickiness
        if m == last_mode:
            score += 0.1

        # context biases
        if m == "entropy" and entropy > 1.2:
            score += 0.3

        if m == "uncertainty" and confidence < 0.4:
            score += 0.3

        if m == "predictive" and abs(x[0]) > 12:
            score += 0.2

        if m == "stabilize" and risk > 10:
            score += 0.2

        if m == "none" and risk < 10:
            score += 0.3

        combined_scores[m] = score

    # ==================================================
    # MODE SELECTION
    # ==================================================

    keys, probs = softmax(combined_scores)
    mode = np.random.choice(keys, p=probs)

    # ==================================================
    # CONTROL
    # ==================================================

    if mode == "entropy":
        control = -0.6 * dx
    elif mode == "uncertainty":
        control = -0.4 * dx
    elif mode == "predictive":
        control = -0.3 * dx
    elif mode == "stabilize":
        control = -0.2 * dx
    else:
        control = np.zeros(3)

    control = safe_clip(control, 20)

    # update system
    x = x + safe_clip((dx + control) * dt, 5)

    # ==================================================
    # LEARNING
    # ==================================================

    if prev_risk is not None:

        reward = prev_risk - risk

        global_mode_scores[mode] += 0.01 * reward
        sequence_mode_scores[seq_key][mode] += 0.03 * reward

        global_mode_scores[mode] = np.clip(global_mode_scores[mode], -2, 5)
        sequence_mode_scores[seq_key][mode] = np.clip(
            sequence_mode_scores[seq_key][mode], -2, 5
        )

        # recent reward memory
        recent_rewards[mode].append(reward)
        if len(recent_rewards[mode]) > recent_window:
            recent_rewards[mode].pop(0)

    prev_risk = risk
    last_mode = mode

    # ==================================================
    # LOGGING
    # ==================================================

    trajectory.append(x.copy())
    risk_list.append(risk)
    mode_list.append(mode)
    state_list.append(state)
    sequence_list.append(seq_key)

    global_score_history.append(global_mode_scores.copy())
    sequence_score_history.append({
        k: sequence_mode_scores[k].copy()
        for k in list(sequence_mode_scores.keys())[:20]  # limit memory
    })


trajectory = np.array(trajectory)


# ==================================================
# 6. PLOTS
# ==================================================

fig = plt.figure(figsize=(14, 10))

ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2])
ax1.set_title("Trajectory (Sequence Control)")

ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:, 0], trajectory[:, 1])
ax2.set_title("XY Path")

ax3 = fig.add_subplot(223)
ax3.plot(risk_list)
ax3.set_title("Risk")

ax4 = fig.add_subplot(224)
for m in modes:
    ax4.plot([h[m] for h in global_score_history], label=m)
ax4.legend()
ax4.set_title("Global Mode Scores")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control_v5_sequence.png")
plt.show()


# ==================================================
# OUTPUT
# ==================================================

print("\n--- META CONTROL v5 (SEQUENCE) ---")
print("Mean risk:", np.mean(risk_list))
print("Modes used:", set(mode_list))

print("\nSample learned sequences:")
for k in list(sequence_mode_scores.keys())[:10]:
    best = max(sequence_mode_scores[k], key=sequence_mode_scores[k].get)
    print(f"{k} → {best}")
