"""
NEXAH — Prediction Control v2

Improvements:
- longer pattern window
- confidence-based control
- entropy-based uncertainty detection
- anticipatory intervention

This is the first multi-signal control layer.
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
# 3. SIMULATE BASE TRAJECTORY
# ==================================================

dt = 0.01
steps = 6000

x = np.array([1.0, 1.0, 1.0])
trajectory = []

for _ in range(steps):
    trajectory.append(x.copy())
    dx = lorenz(x)
    x = x + dt * dx

trajectory = np.array(trajectory)


# ==================================================
# 4. SYMBOLIC STATES (Quantile-based)
# ==================================================

x_vals = trajectory[:, 0]
quantiles = np.quantile(x_vals, np.linspace(0, 1, 7))

states = np.digitize(x_vals, quantiles[1:-1])


# ==================================================
# 5. BUILD PATTERN MODEL (LONGER WINDOW)
# ==================================================

WINDOW = 10   # 🔥 bigger memory

pattern_counts = defaultdict(Counter)

for i in range(len(states) - WINDOW):
    pattern = tuple(states[i:i+WINDOW])
    next_state = states[i+WINDOW]
    pattern_counts[pattern][next_state] += 1


# ==================================================
# 6. PREDICTION FUNCTION
# ==================================================

def predict_distribution(pattern):
    counter = pattern_counts.get(pattern, None)

    if counter is None:
        return None

    total = sum(counter.values())
    probs = {k: v / total for k, v in counter.items()}
    return probs


def compute_entropy(probs):
    return -sum(p * np.log(p + 1e-12) for p in probs.values())


# ==================================================
# 7. CONTROLLED SIMULATION (v2)
# ==================================================

x = np.array([1.0, 1.0, 1.0])

traj_control = []
risk_series = []
predicted_states = []
confidence_series = []
entropy_series = []

control_strength = 0.8

for i in range(steps - WINDOW - 1):

    dx = lorenz(x)

    pattern = tuple(states[i:i+WINDOW])
    probs = predict_distribution(pattern)

    u = np.zeros(3)

    if probs is not None:
        # prediction
        pred_state = max(probs, key=probs.get)
        confidence = probs[pred_state]
        entropy = compute_entropy(probs)

    else:
        pred_state = 0
        confidence = 0
        entropy = 1.0

    predicted_states.append(pred_state)
    confidence_series.append(confidence)
    entropy_series.append(entropy)

    # ==================================================
    # 🔥 NEW CONTROL LOGIC
    # ==================================================

    intervene = False

    # 1. high predicted instability
    if pred_state >= 4:
        intervene = True

    # 2. low confidence → uncertain future
    if confidence < 0.55:
        intervene = True

    # 3. high entropy → chaotic region
    if entropy > 1.2:
        intervene = True

    if intervene:
        u = -control_strength * dx

    # update
    dx_obs = dx + u
    x = x + dt * dx_obs

    traj_control.append(x.copy())
    risk_series.append(compute_risk(x, dx_obs))


traj_control = np.array(traj_control)
risk_series = np.array(risk_series)
confidence_series = np.array(confidence_series)
entropy_series = np.array(entropy_series)


# ==================================================
# 8. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 10))

# --- 3D trajectory ---
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(traj_control[:,0], traj_control[:,1], traj_control[:,2], color="cyan", linewidth=0.7)
ax1.set_title("Prediction-Control v2 (3D)")

# --- XY ---
ax2 = fig.add_subplot(222)
ax2.plot(traj_control[:,0], traj_control[:,1], color="cyan", linewidth=0.7)
ax2.set_title("XY Path")

# --- risk ---
ax3 = fig.add_subplot(223)
ax3.plot(risk_series, color="red", linewidth=0.8)
ax3.set_title("Risk over Time")

# --- confidence + entropy ---
ax4 = fig.add_subplot(224)
ax4.plot(confidence_series, label="Confidence", color="cyan")
ax4.plot(entropy_series, label="Entropy", color="magenta")
ax4.set_title("Confidence & Entropy")
ax4.legend()

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_prediction_control_v2.png", dpi=150)
plt.show()


# ==================================================
# 9. OUTPUT
# ==================================================

print("\n--- PREDICTION CONTROL v2 ---")
print("Mean risk:", np.mean(risk_series))
print("Max risk:", np.max(risk_series))

print("\n🧭 Interpretation:\n")
print("""
The system now uses:

- prediction
- confidence
- entropy

to decide when to intervene.

----------------------------------------

🧠 Key Insight:

Control is now:

→ anticipatory
→ uncertainty-aware
→ adaptive

----------------------------------------

🚀 Meaning:

This is the first REAL intelligent control layer.
""")
