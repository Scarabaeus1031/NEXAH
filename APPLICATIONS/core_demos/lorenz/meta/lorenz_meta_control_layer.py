"""
NEXAH — Meta Control Layer

Goal:
Control is no longer fixed.

The system decides:
- when to trust prediction
- when to trust entropy
- how strongly to intervene

This is CONTROL OVER CONTROL.
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
# 3. BASE TRAJECTORY (for symbolic model)
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
# 4. SYMBOLIC STATES
# ==================================================

x_vals = trajectory[:, 0]
quantiles = np.quantile(x_vals, np.linspace(0, 1, 7))
states = np.digitize(x_vals, quantiles[1:-1])


# ==================================================
# 5. PATTERN MODEL
# ==================================================

WINDOW = 10
pattern_counts = defaultdict(Counter)

for i in range(len(states) - WINDOW):
    pattern = tuple(states[i:i+WINDOW])
    next_state = states[i+WINDOW]
    pattern_counts[pattern][next_state] += 1


# ==================================================
# 6. PREDICTION + ENTROPY
# ==================================================

def predict_distribution(pattern):
    counter = pattern_counts.get(pattern, None)
    if counter is None:
        return None
    total = sum(counter.values())
    return {k: v / total for k, v in counter.items()}

def compute_entropy(probs):
    return -sum(p * np.log(p + 1e-12) for p in probs.values())


# ==================================================
# 7. META CONTROL FUNCTION
# ==================================================

def meta_control_logic(pred_state, confidence, entropy):
    """
    Decide:
    - whether to intervene
    - how strong
    - which mode
    """

    # --- baseline ---
    intervene = False
    strength = 0.0
    mode = "none"

    # ==================================================
    # 🔥 META DECISION LAYER
    # ==================================================

    # 1. HIGH CONFIDENCE → trust prediction
    if confidence > 0.8:
        if pred_state >= 4:
            intervene = True
            strength = 0.6
            mode = "predictive"

    # 2. LOW CONFIDENCE → uncertainty control
    elif confidence < 0.5:
        intervene = True
        strength = 1.0
        mode = "uncertainty"

    # 3. HIGH ENTROPY → chaotic region
    if entropy > 1.0:
        intervene = True
        strength = max(strength, 1.2)
        mode = "entropy"

    # 4. MID REGION → gentle stabilization
    if not intervene and entropy > 0.7:
        intervene = True
        strength = 0.3
        mode = "stabilize"

    return intervene, strength, mode


# ==================================================
# 8. META-CONTROLLED SIMULATION
# ==================================================

x = np.array([1.0, 1.0, 1.0])

traj = []
risk_series = []
confidence_series = []
entropy_series = []
mode_series = []

for i in range(steps - WINDOW - 1):

    dx = lorenz(x)

    pattern = tuple(states[i:i+WINDOW])
    probs = predict_distribution(pattern)

    if probs is not None:
        pred_state = max(probs, key=probs.get)
        confidence = probs[pred_state]
        entropy = compute_entropy(probs)
    else:
        pred_state = 0
        confidence = 0
        entropy = 1.2

    confidence_series.append(confidence)
    entropy_series.append(entropy)

    intervene, strength, mode = meta_control_logic(pred_state, confidence, entropy)
    mode_series.append(mode)

    u = np.zeros(3)

    if intervene:
        u = -strength * dx

    dx_obs = dx + u
    x = x + dt * dx_obs

    traj.append(x.copy())
    risk_series.append(compute_risk(x, dx_obs))


traj = np.array(traj)
risk_series = np.array(risk_series)


# ==================================================
# 9. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 10))

# --- 3D ---
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(traj[:,0], traj[:,1], traj[:,2], color="cyan", linewidth=0.7)
ax1.set_title("Meta-Control Trajectory")

# --- XY ---
ax2 = fig.add_subplot(222)
ax2.plot(traj[:,0], traj[:,1], color="cyan", linewidth=0.7)
ax2.set_title("XY Path")

# --- risk ---
ax3 = fig.add_subplot(223)
ax3.plot(risk_series, color="red")
ax3.set_title("Risk over Time")

# --- confidence + entropy ---
ax4 = fig.add_subplot(224)
ax4.plot(confidence_series, label="Confidence", color="cyan")
ax4.plot(entropy_series, label="Entropy", color="magenta")
ax4.legend()
ax4.set_title("Confidence & Entropy")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control.png", dpi=150)
plt.show()


# ==================================================
# 10. OUTPUT
# ==================================================

unique_modes = set(mode_series)

print("\n--- META CONTROL ---")
print("Mean risk:", np.mean(risk_series))
print("Max risk:", np.max(risk_series))
print("Modes used:", unique_modes)

print("\n🧭 Interpretation:\n")
print("""
The system now dynamically chooses:

- predictive control
- uncertainty control
- entropy control
- stabilization

----------------------------------------

🧠 Key Insight:

Control is no longer fixed.

It is:
→ contextual
→ adaptive
→ self-modulating

----------------------------------------

🚀 Meaning:

You now have:

Dynamics → Prediction → Uncertainty → Meta-Control

= Proto-Intelligent System
""")
