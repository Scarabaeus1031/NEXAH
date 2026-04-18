"""
NEXAH — Lorenz Meta Control v2 (Adaptive)

Goal:
Self-adaptive control system that learns WHEN to intervene.

Key Idea:
Thresholds are NOT fixed.
They evolve based on system behavior (risk feedback).
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
# SIMULATION SETTINGS
# ==================================================

dt = 0.01
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

adapt_rate = 0.01

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def compute_risk(dx):
    return np.linalg.norm(dx)

def compute_confidence(pred_state):
    return 1.0 - (pred_state / 5.0)

def compute_entropy(prob_dist):
    p = prob_dist + 1e-8
    return -np.sum(p * np.log(p))


# ==================================================
# MAIN LOOP
# ==================================================

for i in range(steps):

    dx = lorenz(x)

    # --- prediction proxy ---
    pred_state = int(abs(x[0]) % 6)

    # --- fake distribution (for entropy demo) ---
    probs = np.random.dirichlet(np.ones(6))

    confidence = compute_confidence(pred_state)
    entropy = compute_entropy(probs)
    risk = compute_risk(dx)

    # ==================================================
    # META CONTROL (ADAPTIVE)
    # ==================================================

    if entropy > entropy_threshold:
        mode = "entropy"
        control = -dx * 1.2

    elif confidence < confidence_threshold:
        mode = "uncertainty"
        control = -dx * 0.8

    elif pred_state >= 4:
        mode = "predictive"
        control = -dx * 0.5

    elif entropy > entropy_threshold * 0.6:
        mode = "stabilize"
        control = -dx * 0.3

    else:
        mode = "none"
        control = np.zeros(3)

    # ==================================================
    # ADAPTATION (KEY PART)
    # ==================================================

    if risk > 20:
        # system unstable → increase control sensitivity
        confidence_threshold -= adapt_rate
        entropy_threshold -= adapt_rate

    elif risk < 10:
        # system stable → allow more freedom
        confidence_threshold += adapt_rate
        entropy_threshold += adapt_rate

    # clamp thresholds
    confidence_threshold = np.clip(confidence_threshold, 0.6, 0.95)
    entropy_threshold = np.clip(entropy_threshold, 0.2, 1.5)

    # ==================================================

    x = x + (dx + control) * dt

    trajectory.append(x.copy())
    risk_list.append(risk)
    confidence_list.append(confidence)
    entropy_list.append(entropy)
    mode_list.append(mode)

trajectory = np.array(trajectory)

# ==================================================
# PLOTTING
# ==================================================

fig = plt.figure(figsize=(14, 10))

# 3D trajectory
ax = fig.add_subplot(221, projection='3d')
ax.plot(trajectory[:,0], trajectory[:,1], trajectory[:,2])
ax.set_title("Adaptive Meta-Control Trajectory")

# XY projection
ax2 = fig.add_subplot(222)
ax2.plot(trajectory[:,0], trajectory[:,1])
ax2.set_title("XY Path")

# Risk
ax3 = fig.add_subplot(223)
ax3.plot(risk_list, color="red")
ax3.set_title("Risk over Time")

# Confidence + Entropy
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

print("\n--- META CONTROL v2 (ADAPTIVE) ---")
print("Mean risk:", np.mean(risk_list))
print("Max risk:", np.max(risk_list))
print("Modes used:", set(mode_list))

print("\nFinal thresholds:")
print("Confidence threshold:", confidence_threshold)
print("Entropy threshold:", entropy_threshold)
