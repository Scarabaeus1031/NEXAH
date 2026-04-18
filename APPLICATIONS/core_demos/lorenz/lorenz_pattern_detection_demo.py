"""
NEXAH — Pattern Detection Demo

Goal:
Extract recurring patterns from symbolic dynamics.

This reveals:
- attractor rhythms
- transition motifs
- structural sequences

Chaos → Symbols → Patterns
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

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

N_STATES = 6

def risk_to_state(r):
    p = np.sum(risk_series < r) / len(risk_series)
    s = int(np.clip(np.floor(p * N_STATES), 0, N_STATES-1))
    return s

states = np.array([risk_to_state(r) for r in risk_series])


# ==================================================
# 4. PATTERN DETECTION
# ==================================================

def extract_patterns(sequence, window_size=3):
    patterns = []

    for i in range(len(sequence) - window_size):
        pattern = tuple(sequence[i:i+window_size])
        patterns.append(pattern)

    return Counter(patterns)


# 🔥 Try multiple pattern lengths
patterns_3 = extract_patterns(states, 3)
patterns_4 = extract_patterns(states, 4)


# ==================================================
# 5. TOP PATTERNS
# ==================================================

top3 = patterns_3.most_common(10)
top4 = patterns_4.most_common(10)


print("\n--- TOP PATTERNS (length 3) ---")
for p, c in top3:
    print(p, "→", c)

print("\n--- TOP PATTERNS (length 4) ---")
for p, c in top4:
    print(p, "→", c)


# ==================================================
# 6. VISUALIZATION
# ==================================================

fig = plt.figure(figsize=(14, 8))

# --- state sequence ---
ax1 = fig.add_subplot(211)
ax1.plot(states[:1000], color="magenta")
ax1.set_title("State Sequence (first 1000 steps)")

# --- pattern frequency ---
ax2 = fig.add_subplot(212)

labels = [str(p) for p, _ in top3]
counts = [c for _, c in top3]

ax2.bar(labels, counts, color="cyan")
ax2.set_title("Top Patterns (Length 3)")
ax2.set_xticklabels(labels, rotation=45)

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_patterns.png", dpi=150)
plt.show()


# ==================================================
# 7. INTERPRETATION
# ==================================================

print("\n🧭 Interpretation:\n")
print("""
These are NOT random sequences.

They are:
→ recurring transition motifs
→ local attractor rhythms
→ symbolic fingerprints of the system

----------------------------------------

🧠 Key Insight:

Chaos is NOT random.

It contains:
→ grammar
→ repetition
→ structure

----------------------------------------

🚀 Meaning:

You now have:

Dynamics → States → Patterns

Next step:
→ build prediction / memory
""")
