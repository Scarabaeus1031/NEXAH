"""
NEXAH — Pattern Prediction Demo

Goal:
Predict next state from observed patterns.

This is the step from:
Pattern → Anticipation

Chaos becomes partially predictable.
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
# 3. GENERATE STATE SEQUENCE
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

# --- quantile-based states ---
N_STATES = 6

def risk_to_state(r):
    p = np.sum(risk_series < r) / len(risk_series)
    s = int(np.clip(np.floor(p * N_STATES), 0, N_STATES - 1))
    return s

states = np.array([risk_to_state(r) for r in risk_series])


# ==================================================
# 4. BUILD PREDICTION MODEL
# ==================================================

WINDOW = 3  # pattern length

transition_model = defaultdict(Counter)

for i in range(len(states) - WINDOW):
    pattern = tuple(states[i:i+WINDOW])
    next_state = states[i+WINDOW]

    transition_model[pattern][next_state] += 1


# convert to probabilities
prediction_model = {}

for pattern, counts in transition_model.items():
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    prediction_model[pattern] = probs


# ==================================================
# 5. PREDICTION
# ==================================================

predicted = []
actual = []

for i in range(len(states) - WINDOW):

    pattern = tuple(states[i:i+WINDOW])
    true_next = states[i+WINDOW]

    if pattern in prediction_model:
        probs = prediction_model[pattern]
        pred = max(probs, key=probs.get)
    else:
        pred = np.random.randint(0, N_STATES)

    predicted.append(pred)
    actual.append(true_next)

predicted = np.array(predicted)
actual = np.array(actual)


# ==================================================
# 6. EVALUATION
# ==================================================

accuracy = np.mean(predicted == actual)

print("\n--- PATTERN PREDICTION ---")
print(f"Accuracy: {accuracy:.3f}")

# confusion-like insight
error = np.abs(predicted - actual)
mean_error = np.mean(error)

print(f"Mean state error: {mean_error:.3f}")


# ==================================================
# 7. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 8))

# --- actual vs predicted ---
ax1 = fig.add_subplot(211)
ax1.plot(actual[:1000], label="Actual", color="cyan")
ax1.plot(predicted[:1000], label="Predicted", color="magenta", alpha=0.7)
ax1.set_title("Prediction vs Actual (first 1000 steps)")
ax1.legend()

# --- error ---
ax2 = fig.add_subplot(212)
ax2.plot(error[:1000], color="red")
ax2.set_title("Prediction Error")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_pattern_prediction.png", dpi=150)
plt.show()


# ==================================================
# 8. INTERPRETATION
# ==================================================

print("\n🧭 Interpretation:\n")
print("""
The system is now partially predictable.

It:
- recognizes patterns
- anticipates next states
- reduces uncertainty

----------------------------------------

🧠 Key Insight:

Chaos is NOT fully random.

It contains:
→ short-term predictability
→ structural memory

----------------------------------------

🚀 Meaning:

You now have:

Dynamics → States → Patterns → Prediction

Next step:
→ use prediction for CONTROL
""")
