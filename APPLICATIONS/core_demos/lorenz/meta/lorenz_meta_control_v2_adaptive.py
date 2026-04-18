"""
NEXAH — Lorenz Meta Control v2 (Stable Adaptive)

FIXED VERSION:
- prevents overflow
- stabilizes control
- keeps adaptive behavior
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

dt = 0.005   # 🔥 smaller timestep = more stable
steps = 6000

x = np.array([1.0, 1.0, 1.0])

trajectory = []
risk_list = []
confidence_list = []
entropy_list = []
mode_list = []

# ==================================================
# ADAPTIVE PARAMETERS
# ==================================================

confidence_threshold = 0.9
entropy_threshold = 0.5
adapt_rate = 0.005

# ==================================================
# HELPERS
# ==================================================

def compute_risk(dx):
    return np.linalg.norm(dx)

def compute_confidence(pred_state):
    return 1.0 - (pred_state / 6.0)

def compute_entropy(prob_dist):
    p = prob_dist + 1e-8
    return -np.sum(p * np.log(p))

def safe_clip(v, max_val=50):
    return np.clip(v, -max_val, max_val)

# ==================================================
# LOOP
# ==================================================

for i in range(steps):

    dx = lorenz(x)

    # 🔥 CLAMP DERIVATIVE (VERY IMPORTANT)
    dx = safe_clip(dx, 50)

    # --- safe state extraction ---
    if np.any(np.isnan(x)):
        print("⚠️ Reset due to NaN")
        x = np.array([1.0, 1.0, 1.0])

    pred_state = int(abs(x[0]) % 6)

    probs = np.random.dirichlet(np.ones(6))

    confidence = compute_confidence(pred_state)
    entropy = compute_entropy(probs)
    risk = compute_risk(dx)

    # ==================================================
    # META CONTROL (SOFT VERSION)
    # ==================================================

    control_strength = 0.0
    mode = "none"

    if entropy > entropy_threshold:
        control_strength = 0.6
        mode = "entropy"

    elif confidence < confidence_threshold:
        control_strength = 0.4
        mode = "uncertainty"

    elif pred_state >= 4:
        control_strength = 0.3
        mode = "predictive"

    elif entropy > entropy_threshold * 0.6:
        control_strength = 0.2
        mode = "stabilize"

    # 🔥 SOFT CONTROL (key fix)
    control = -dx * control_strength

    # 🔥 CLAMP CONTROL
    control = safe_clip(control, 20)

    # ==================================================
    # ADAPTATION
    # ==================================================

    if risk > 25:
        confidence_threshold -= adapt_rate
        entropy_threshold -= adapt_rate

    elif risk < 12:
        confidence_threshold += adapt_rate
        entropy_threshold += adapt_rate

    confidence_threshold = np.clip(confidence_threshold, 0.6, 0.95)
    entropy_threshold = np.clip(entropy_threshold, 0.2, 1.5)

    # ==================================================
    # UPDATE (SAFE)
    # ==================================================

    step_update = (dx + control) * dt
    step_update = safe_clip(step_update, 5)

    x = x + step_update

    trajectory.append(x.copy())
    risk_list.append(risk)
    confidence_list.append(confidence)
    entropy_list.append(entropy)
    mode_list.append(mode)

trajectory = np.array(trajectory)

# ==================================================
# PLOTS
# ==================================================

fig = plt.figure(figsize=(14, 10))

ax = fig.add_subplot(221, projection='3d')
ax.plot(trajectory[:,0], trajectory[:,1], trajectory[:,2])
ax.set_title("Adaptive Meta-Control (Stable)")

ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:,0], trajectory[:,1])
ax2.set_title("XY Path")

ax3 = fig.add_subplot(223)
ax3.plot(risk_list, color="red")
ax3.set_title("Risk over Time")

ax4 = fig.add_subplot(224)
ax4.plot(confidence_list, label="Confidence")
ax4.plot(entropy_list, label="Entropy")
ax4.legend()
ax4.set_title("Confidence & Entropy")

plt.tight_layout()
plt.savefig("APPLICATIONS/outputs/lorenz_meta_control_v2_adaptive.png")
plt.show()

# ==================================================
# OUTPUT
# ==================================================

print("\n--- META CONTROL v2 (STABLE) ---")
print("Mean risk:", np.mean(risk_list))
print("Max risk:", np.max(risk_list))
print("Modes used:", set(mode_list))
