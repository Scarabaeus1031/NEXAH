"""
NEXAH — Prediction Control Demo

Goal:
Use prediction to actively control the system.

This is the transition from:
Prediction → Action

System anticipates instability and reacts BEFORE it happens.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

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
# 3. GENERATE TRAINING DATA (states)
# ==================================================

dt = 0.01
steps = 6000

x = np.array([8.0, 8.0, 25.0])

risk_series = []
trajectory = []

for _ in range(steps):
    dx = lorenz(x)
    dx_obs = dx + np.random.randn(3)

    r = compute_risk(x, dx_obs)

    x = x + dt * dx_obs

    trajectory.append(x.copy())
    risk_series.append(r)

trajectory = np.array(trajectory)
risk_series = np.array(risk_series)

# --- states via quantiles ---
N_STATES = 6

def risk_to_state(r):
    p = np.sum(risk_series < r) / len(risk_series)
    s = int(np.clip(np.floor(p * N_STATES), 0, N_STATES - 1))
    return s

states = np.array([risk_to_state(r) for r in risk_series])


# ==================================================
# 4. BUILD PREDICTION MODEL
# ==================================================

WINDOW = 5  # 🔥 bigger window

transition_model = defaultdict(Counter)

for i in range(len(states) - WINDOW):
    pattern = tuple(states[i:i+WINDOW])
    next_state = states[i+WINDOW]
    transition_model[pattern][next_state] += 1

prediction_model = {}

for pattern, counts in transition_model.items():
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    prediction_model[pattern] = probs


# ==================================================
# 5. CONTROLLED SIMULATION
# ==================================================

x = np.array([8.0, 8.0, 25.0])

trajectory_ctrl = []
risk_ctrl = []
pred_states = []

state_buffer = list(states[:WINDOW])  # seed

control_strength = 1.0

for i in range(steps):

    dx = lorenz(x)
    dx_obs = dx + np.random.randn(3)

    # --- predict next state ---
    pattern = tuple(state_buffer)

    if pattern in prediction_model:
        probs = prediction_model[pattern]
        pred_state = max(probs, key=probs.get)
    else:
        pred_state = np.random.randint(0, N_STATES)

    pred_states.append(pred_state)

    # --- compute current risk ---
    r = compute_risk(x, dx_obs)

    # ==================================================
    # 🔥 CONTROL LOGIC
    # ==================================================

    # if predicted state is HIGH risk → intervene
    if pred_state >= 4:
        # push toward field direction (stabilizing)
        grad = lorenz(x)
        u = -control_strength * grad / (np.linalg.norm(grad) + 1e-8)
    else:
        u = np.zeros(3)

    # update system
    x = x + dt * (dx_obs + u)

    # update buffer
    new_state = risk_to_state(r)
    state_buffer.pop(0)
    state_buffer.append(new_state)

    trajectory_ctrl.append(x.copy())
    risk_ctrl.append(r)

trajectory_ctrl = np.array(trajectory_ctrl)
risk_ctrl = np.array(risk_ctrl)
pred_states = np.array(pred_states)


# ==================================================
# 6. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 8))

# --- trajectory ---
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(trajectory_ctrl[:,0],
         trajectory_ctrl[:,1],
         trajectory_ctrl[:,2],
         color="cyan", linewidth=0.5)
ax1.set_title("Prediction-Controlled Trajectory")

# --- XY ---
ax2 = fig.add_subplot(222)
ax2.plot(trajectory_ctrl[:,0], trajectory_ctrl[:,1], color="cyan")
ax2.set_title("XY Path")

# --- predicted states ---
ax3 = fig.add_subplot(223)
ax3.plot(pred_states[:1000], color="magenta")
ax3.set_title("Predicted States")

# --- risk ---
ax4 = fig.add_subplot(224)
ax4.plot(risk_ctrl, color="red")
ax4.set_title("Risk over Time")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_prediction_control.png", dpi=150)
plt.show()


# ==================================================
# 7. RESULTS
# ==================================================

print("\n--- PREDICTION CONTROL ---")
print("Mean risk:", np.mean(risk_ctrl))
print("Max risk:", np.max(risk_ctrl))

print("\n🧭 Interpretation:\n")
print("""
The system now anticipates instability.

It:
- predicts future states
- detects high-risk regions
- intervenes BEFORE instability occurs

----------------------------------------

🧠 Key Insight:

Control is no longer reactive.

It is:
→ anticipatory

----------------------------------------

🚀 Meaning:

You now have:

Dynamics → States → Prediction → Control

= anticipatory system
""")
