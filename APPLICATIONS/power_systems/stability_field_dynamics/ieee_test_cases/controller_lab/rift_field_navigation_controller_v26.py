import os
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
OUT_PATH = os.path.join(BASE_PATH, "rift_extraction")
os.makedirs(OUT_PATH, exist_ok=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
states_path = os.path.join(BASE_PATH, "states.npy")
states = np.load(states_path)
print("Loaded states.npy")

rift_path = os.path.join(BASE_PATH, "rift.npy")
if os.path.exists(rift_path):
    rift = np.load(rift_path)
    print("Loaded rift.npy")
else:
    print("rift.npy not found -> using zeros")
    rift = np.zeros(len(states))

phi = states[:, 0]
instability_raw = states[:, 1]
t = np.arange(len(phi))

# -------------------------------------------------
# BASE PARAMETERS
# -------------------------------------------------
base = np.mean(phi)
std = np.std(phi)

upper = base + std
lower = base - std

base_freq = 0.0083
carrier = base_freq * t

print(f"Base Layer:  {base:.4f} ± {std:.4f}")
print(f"Upper Layer: {upper:.4f}")
print(f"Lower Layer: {lower:.4f}")
print(f"Base frequency: {base_freq:.4f}")

# -------------------------------------------------
# PHASE REPRESENTATION
# -------------------------------------------------
phi_rel = phi - carrier
theta_flow = phi_rel.copy()

# wrapped for ring plot
theta_wrapped = np.mod(theta_flow, 2 * np.pi)

# -------------------------------------------------
# FEEDBACK INSTABILITY
# -------------------------------------------------
instability_feedback = np.zeros_like(instability_raw)
alpha = 0.18
instability_feedback[0] = instability_raw[0]

for i in range(1, len(instability_raw)):
    instability_feedback[i] = (
        (1 - alpha) * instability_feedback[i - 1]
        + alpha * instability_raw[i]
    )

# -------------------------------------------------
# BREATHING RADIUS
# -------------------------------------------------
inst_min = np.min(instability_feedback)
inst_max = np.max(instability_feedback)

if inst_max - inst_min < 1e-12:
    inst_norm = np.zeros_like(instability_feedback)
else:
    inst_norm = (instability_feedback - inst_min) / (inst_max - inst_min)

radius = 1.16 - 0.62 * inst_norm

# -------------------------------------------------
# ANU FIELD (center influence)
# -------------------------------------------------
# stronger near center, weaker outside
anu_strength = np.exp(-((radius - 0.85) ** 2) / 0.02)

# -------------------------------------------------
# NEXIT GATEWAY DETECTION
# -------------------------------------------------
# when relative phase crosses near zero, gateway opens
gateway_eps = 0.035
nexit_mask = np.abs(phi_rel) < gateway_eps

# -------------------------------------------------
# ENTRY / EXIT / TRANSFER / OPERATOR STATES
# -------------------------------------------------
dphi_rel = np.gradient(phi_rel)
dradius = np.gradient(radius)

state_code = np.zeros(len(phi), dtype=int)

# state mapping
# 0 none
# 1 portal
# 2 engage
# 3 lock
# 4 release
# 5 exit
# 6 nexit

portal_mask = (np.abs(phi_rel) < 0.08) & (radius > 0.95)
engage_mask = (phi_rel > 0.02) & (phi_rel < 0.18) & (dradius < 0)
lock_mask = (np.abs(dphi_rel) < 0.01) & (radius > 0.88) & (radius < 1.02)
release_mask = (phi_rel > -0.05) & (phi_rel < 0.08) & (dradius > 0)
exit_mask = (phi_rel < -0.02) & (radius < 0.92)

state_code[portal_mask] = 1
state_code[engage_mask] = 2
state_code[lock_mask] = 3
state_code[release_mask] = 4
state_code[exit_mask] = 5
state_code[nexit_mask] = 6

# -------------------------------------------------
# TORUS / RING PROJECTION
# -------------------------------------------------
x = radius * np.cos(theta_wrapped)
y = radius * np.sin(theta_wrapped)

# -------------------------------------------------
# TRANSITION MATRIX BETWEEN OPERATOR STATES
# -------------------------------------------------
NUM_STATES = 7
transition_matrix = np.zeros((NUM_STATES, NUM_STATES), dtype=float)

for i in range(len(state_code) - 1):
    a = state_code[i]
    b = state_code[i + 1]
    transition_matrix[a, b] += 1.0

row_sums = transition_matrix.sum(axis=1, keepdims=True)
transition_matrix_norm = np.divide(
    transition_matrix,
    row_sums,
    out=np.zeros_like(transition_matrix),
    where=row_sums != 0
)

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------
np.save(os.path.join(OUT_PATH, "field_navigation_v26.npy"), np.vstack([x, y]).T)
np.save(os.path.join(OUT_PATH, "v26_theta_flow.npy"), theta_flow)
np.save(os.path.join(OUT_PATH, "v26_radius.npy"), radius)
np.save(os.path.join(OUT_PATH, "v26_state_code.npy"), state_code)
np.save(os.path.join(OUT_PATH, "v26_transition_matrix.npy"), transition_matrix_norm)
np.save(os.path.join(OUT_PATH, "v26_anu_strength.npy"), anu_strength)

print(f"Saved -> {os.path.join(OUT_PATH, 'field_navigation_v26.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v26_theta_flow.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v26_radius.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v26_state_code.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v26_transition_matrix.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v26_anu_strength.npy')}")

# -------------------------------------------------
# PLOT 1 — PHASE / RELATIVE PHASE / NEXIT
# -------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

axs[0].plot(t, phi, color="royalblue", label="phi")
axs[0].plot(t, carrier, color="orange", label="carrier")
axs[0].set_title("V26 Phase vs Carrier")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, phi_rel, color="purple", label="relative phase")
axs[1].axhline(0, color="gray", linestyle="--", alpha=0.7)
axs[1].scatter(t[nexit_mask], phi_rel[nexit_mask], color="red", s=30, label="NEXIT")
axs[1].set_title("V26 Relative Phase + NEXIT Gateway")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

axs[2].plot(t, instability_raw, color="lightcoral", alpha=0.55, label="raw instability")
axs[2].plot(t, instability_feedback, color="darkred", linewidth=2, label="feedback instability")
axs[2].set_title("V26 Raw vs Feedback Instability")
axs[2].legend()
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
f1 = os.path.join(OUT_PATH, "v26_phase_gateway.png")
plt.savefig(f1, dpi=160)
plt.close()
print(f"Saved -> {f1}")

# -------------------------------------------------
# PLOT 2 — RADIUS / ANU FIELD / STATE TIMELINE
# -------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

axs[0].plot(t, radius, color="teal", label="radius")
axs[0].axhline(1.00, color="magenta", linestyle="--", label="base")
axs[0].axhline(1.16, color="orange", linestyle="--", label="upper")
axs[0].axhline(0.84, color="purple", linestyle="--", label="lower")
axs[0].set_title("V26 Breathing Radius")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, anu_strength, color="goldenrod", label="ANU field strength")
axs[1].set_title("V26 ANU Center Coupling")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

axs[2].plot(t, state_code, color="black", linewidth=1.8)
labels = ["none", "portal", "engage", "lock", "release", "exit", "nexit"]
axs[2].set_yticks(range(len(labels)))
axs[2].set_yticklabels(labels)
axs[2].scatter(t[state_code == 1], state_code[state_code == 1], color="gold", s=28, label="portal")
axs[2].scatter(t[state_code == 2], state_code[state_code == 2], color="limegreen", s=28, label="engage")
axs[2].scatter(t[state_code == 3], state_code[state_code == 3], color="deepskyblue", s=28, label="lock")
axs[2].scatter(t[state_code == 4], state_code[state_code == 4], color="orange", s=28, label="release")
axs[2].scatter(t[state_code == 5], state_code[state_code == 5], color="red", s=28, label="exit")
axs[2].scatter(t[state_code == 6], state_code[state_code == 6], color="darkred", s=36, label="nexit")
axs[2].set_title("V26 Operator Timeline")
axs[2].legend(loc="upper left")
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
f2 = os.path.join(OUT_PATH, "v26_operator_timeline.png")
plt.savefig(f2, dpi=160)
plt.close()
print(f"Saved -> {f2}")

# -------------------------------------------------
# PLOT 3 — OPEN/CLOSED RING FLOW + ANU + NEXIT
# -------------------------------------------------
plt.figure(figsize=(8, 8))

for rr in [0.84, 1.00, 1.16]:
    circle = plt.Circle((0, 0), rr, color="gray", fill=False, linestyle="--", alpha=0.45)
    plt.gca().add_artist(circle)

sc = plt.scatter(x, y, c=t, cmap="viridis", s=38, label="trajectory")
plt.colorbar(sc, label="time index")

plt.scatter(x[state_code == 1], y[state_code == 1], color="gold", edgecolor="black", s=70, label="portal")
plt.scatter(x[state_code == 2], y[state_code == 2], color="limegreen", s=55, label="engage")
plt.scatter(x[state_code == 3], y[state_code == 3], color="deepskyblue", s=55, label="lock")
plt.scatter(x[state_code == 4], y[state_code == 4], color="orange", s=55, label="release")
plt.scatter(x[state_code == 5], y[state_code == 5], color="red", s=55, label="exit")
plt.scatter(x[state_code == 6], y[state_code == 6], color="darkred", marker="X", s=110, label="NEXIT")

# ANU kernel
plt.scatter([0], [0], color="black", s=220, label="ANU / OKO kernel")

plt.axhline(0, color="gray", linestyle=":", alpha=0.7)
plt.axvline(0, color="gray", linestyle=":", alpha=0.7)
plt.gca().set_aspect("equal")
plt.title("V26 Open-Closed Ring Flow + ANU + NEXIT")
plt.legend(loc="best")
plt.grid(True, alpha=0.25)

f3 = os.path.join(OUT_PATH, "v26_ring_anu_nexit.png")
plt.savefig(f3, dpi=160)
plt.close()
print(f"Saved -> {f3}")

# -------------------------------------------------
# PLOT 4 — TRANSITION MATRIX
# -------------------------------------------------
plt.figure(figsize=(8, 6))
plt.imshow(transition_matrix_norm, cmap="magma")
plt.colorbar(label="transition probability")
plt.xticks(range(NUM_STATES), labels, rotation=45)
plt.yticks(range(NUM_STATES), labels)
plt.xlabel("to")
plt.ylabel("from")
plt.title("V26 Operator Transition Matrix")

for i in range(NUM_STATES):
    for j in range(NUM_STATES):
        val = transition_matrix_norm[i, j]
        if val > 0:
            plt.text(j, i, f"{val:.2f}", ha="center", va="center", color="white", fontsize=8)

plt.tight_layout()
f4 = os.path.join(OUT_PATH, "v26_transition_matrix.png")
plt.savefig(f4, dpi=160)
plt.close()
print(f"Saved -> {f4}")

# -------------------------------------------------
# PLOT 5 — HIGHLIGHT GEOMETRY
# -------------------------------------------------
plt.figure(figsize=(8, 8))

for rr in [0.84, 1.00, 1.16]:
    circle = plt.Circle((0, 0), rr, color="gray", fill=False, linestyle="--", alpha=0.35)
    plt.gca().add_artist(circle)

plt.plot(x, y, color="slateblue", alpha=0.35, linewidth=2)
plt.scatter(x, y, c=radius, cmap="plasma", s=34)

plt.scatter(x[nexit_mask], y[nexit_mask], color="red", marker="X", s=120, label="NEXIT gateway")
plt.scatter([0], [0], color="black", s=240, label="ANU core")

plt.annotate("inside-out drift", xy=(x[len(x)//3], y[len(y)//3]), xytext=(-0.9, 0.9),
             arrowprops=dict(arrowstyle="->", color="black"), fontsize=11)
plt.annotate("gateway crossing", xy=(x[nexit_mask][0], y[nexit_mask][0]) if np.any(nexit_mask) else (0.8, 0.0),
             xytext=(0.15, -0.95),
             arrowprops=dict(arrowstyle="->", color="red"), fontsize=11, color="red")

plt.axhline(0, color="gray", linestyle=":", alpha=0.7)
plt.axvline(0, color="gray", linestyle=":", alpha=0.7)
plt.gca().set_aspect("equal")
plt.title("V26 Highlight — ANU / NEXIT / Inside-Out Geometry")
plt.legend()
plt.grid(True, alpha=0.2)

f5 = os.path.join(OUT_PATH, "v26_highlight_geometry.png")
plt.savefig(f5, dpi=160)
plt.close()
print(f"Saved -> {f5}")

print("V26 NEXIT GATEWAY + ANU FIELD DONE")
