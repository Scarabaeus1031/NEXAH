import os
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export/"
OUT_PATH = os.path.join(BASE_PATH, "rift_extraction")
os.makedirs(OUT_PATH, exist_ok=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
states = np.load(os.path.join(BASE_PATH, "states.npy"))
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

print(f"Base Layer:  {base:.4f} ± {std:.4f}")
print(f"Upper Layer: {upper:.4f}")
print(f"Lower Layer: {lower:.4f}")
print(f"Base frequency: {base_freq:.4f}")

# -------------------------------------------------
# PHASE SYSTEM
# -------------------------------------------------
carrier = base_freq * t
phi_rel = phi - carrier
theta_flow = np.mod(phi_rel, 2 * np.pi)

# -------------------------------------------------
# FEEDBACK INSTABILITY
# -------------------------------------------------
feedback_instability = np.convolve(instability_raw, np.ones(7)/7, mode="same")

# -------------------------------------------------
# BREATHING RADIUS
# -------------------------------------------------
phi_rel_norm = phi_rel - np.mean(phi_rel)
phi_rel_norm = phi_rel_norm / (np.max(np.abs(phi_rel_norm)) + 1e-9)

radius = 1.0 + 0.18 * phi_rel_norm

# -------------------------------------------------
# STRUCTURAL LEVELS
# 0 = local
# 1 = ring
# 2 = gateway
# -------------------------------------------------
level_code = np.zeros(len(phi), dtype=int)

for i in range(len(phi)):
    if radius[i] > 1.04:
        level_code[i] = 2
    elif radius[i] > 0.90:
        level_code[i] = 1
    else:
        level_code[i] = 0

# -------------------------------------------------
# 3-PHASE RHYTHM
# 0 = intake
# 1 = hold
# 2 = release
# -------------------------------------------------
rhythm_phase = np.mod(np.arange(len(phi)), 3)

# -------------------------------------------------
# 3x3 STATE CODE
# -------------------------------------------------
state_code = level_code * 3 + rhythm_phase

state_labels = [
    "local-intake", "local-hold", "local-release",
    "ring-intake", "ring-hold", "ring-release",
    "gate-intake", "gate-hold", "gate-release"
]

# -------------------------------------------------
# ACTIVE OPERATOR TRIGGERS
# -------------------------------------------------
engage_mask = np.zeros(len(phi), dtype=bool)
lock_mask = np.zeros(len(phi), dtype=bool)
release_mask = np.zeros(len(phi), dtype=bool)
nexit_mask = np.zeros(len(phi), dtype=bool)

for i in range(len(phi)):
    # engage = entering ring/gateway with low instability
    if level_code[i] >= 1 and rhythm_phase[i] == 0 and feedback_instability[i] < np.median(feedback_instability):
        engage_mask[i] = True

    # lock = hold phase near upper band, moderate stability
    if rhythm_phase[i] == 1 and radius[i] > 0.96 and radius[i] < 1.08:
        lock_mask[i] = True

    # release = release phase with outward tendency
    if rhythm_phase[i] == 2 and phi_rel_norm[i] > 0:
        release_mask[i] = True

    # nexit = gate release with low instability and strong outer radius
    if level_code[i] == 2 and rhythm_phase[i] == 2 and radius[i] > 1.02 and feedback_instability[i] < np.percentile(feedback_instability, 40):
        nexit_mask[i] = True

# -------------------------------------------------
# CONTROL SIGNAL
# -1 = damp
#  0 = neutral
# +1 = push / exit
# -------------------------------------------------
control_signal = np.zeros(len(phi))

for i in range(len(phi)):
    if engage_mask[i]:
        control_signal[i] += 0.5
    if lock_mask[i]:
        control_signal[i] += 0.25
    if release_mask[i]:
        control_signal[i] -= 0.25
    if nexit_mask[i]:
        control_signal[i] += 1.0

# smooth control
control_signal = np.convolve(control_signal, np.ones(5)/5, mode="same")

# -------------------------------------------------
# CONTROLLED PHASE
# -------------------------------------------------
phi_controlled = phi + 0.05 * control_signal
theta_controlled = np.mod(phi_controlled - carrier, 2 * np.pi)

# -------------------------------------------------
# GEOMETRY
# -------------------------------------------------
x = radius * np.cos(theta_controlled)
y = radius * np.sin(theta_controlled)

# ANU / OKO kernel
anu_x, anu_y = 0.0, 0.0

# NEXIT gateway = mean position of nexit points if present
if np.any(nexit_mask):
    nexit_x = np.mean(x[nexit_mask])
    nexit_y = np.mean(y[nexit_mask])
else:
    nexit_x, nexit_y = 1.05, 0.0

# -------------------------------------------------
# TRANSITION MATRIX
# -------------------------------------------------
num_states = 9
transition_matrix = np.zeros((num_states, num_states))

for i in range(len(state_code) - 1):
    a = state_code[i]
    b = state_code[i + 1]
    transition_matrix[a, b] += 1

row_sums = transition_matrix.sum(axis=1, keepdims=True)
transition_matrix_norm = np.divide(
    transition_matrix,
    row_sums,
    out=np.zeros_like(transition_matrix),
    where=row_sums != 0
)

# -------------------------------------------------
# SAVE ARRAYS
# -------------------------------------------------
np.save(os.path.join(OUT_PATH, "field_navigation_v28.npy"), np.vstack([x, y]).T)
np.save(os.path.join(OUT_PATH, "v28_theta_flow.npy"), theta_controlled)
np.save(os.path.join(OUT_PATH, "v28_radius.npy"), radius)
np.save(os.path.join(OUT_PATH, "v28_state_code.npy"), state_code)
np.save(os.path.join(OUT_PATH, "v28_control_signal.npy"), control_signal)
np.save(os.path.join(OUT_PATH, "v28_transition_matrix.npy"), transition_matrix_norm)

print(f"Saved -> {os.path.join(OUT_PATH, 'field_navigation_v28.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v28_theta_flow.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v28_radius.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v28_state_code.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v28_control_signal.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v28_transition_matrix.npy')}")

# -------------------------------------------------
# PLOT 1 — ACTIVE OPERATOR GEOMETRY
# -------------------------------------------------
plt.figure(figsize=(8, 8))

plt.scatter(x, y, c=t, cmap="viridis", s=45, alpha=0.85, label="trajectory")
plt.scatter(x[engage_mask], y[engage_mask], color="limegreen", s=70, label="engage")
plt.scatter(x[lock_mask], y[lock_mask], color="deepskyblue", s=70, label="lock")
plt.scatter(x[release_mask], y[release_mask], color="orange", s=70, label="release")
plt.scatter(x[nexit_mask], y[nexit_mask], color="red", s=100, marker="x", linewidths=3, label="nexit")

plt.scatter([anu_x], [anu_y], color="black", s=420, label="ANU / OKO kernel")
plt.scatter([nexit_x], [nexit_y], color="darkred", s=220, marker="X", label="NEXIT gateway")

for rr in [0.3, 0.6, 0.9, 1.2]:
    circle = plt.Circle((0, 0), rr, color="gray", fill=False, linestyle="--", alpha=0.35)
    plt.gca().add_patch(circle)

plt.axhline(0, color="gray", linestyle=":", alpha=0.6)
plt.axvline(0, color="gray", linestyle=":", alpha=0.6)

plt.gca().set_aspect("equal")
plt.title("V28 Active Operator Geometry — Engage / Lock / Release / NEXIT")
plt.legend(loc="lower left")
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT_PATH, "v28_active_operator_geometry.png"), dpi=160)
plt.close()

print(f"Saved -> {os.path.join(OUT_PATH, 'v28_active_operator_geometry.png')}")

# -------------------------------------------------
# PLOT 2 — CONTROL TIMELINE
# -------------------------------------------------
plt.figure(figsize=(14, 8))

plt.subplot(4, 1, 1)
plt.plot(t, phi, color="royalblue", label="phi")
plt.plot(t, carrier, color="darkorange", label="carrier")
plt.set_title("V28 Phase vs Carrier")
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(t, phi_rel, color="purple", label="relative phase")
plt.axhline(0, color="gray", linestyle="--", alpha=0.6)
plt.scatter(t[engage_mask], phi_rel[engage_mask], color="limegreen", s=28, label="engage")
plt.scatter(t[lock_mask], phi_rel[lock_mask], color="deepskyblue", s=28, label="lock")
plt.scatter(t[release_mask], phi_rel[release_mask], color="orange", s=28, label="release")
plt.scatter(t[nexit_mask], phi_rel[nexit_mask], color="red", s=35, label="nexit")
plt.set_title("V28 Relative Phase + Active Triggers")
plt.legend(ncol=5, fontsize=9)

plt.subplot(4, 1, 3)
plt.plot(t, control_signal, color="black", label="control signal")
plt.axhline(0, color="gray", linestyle="--", alpha=0.6)
plt.set_title("V28 Control Signal")
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(t, feedback_instability, color="darkred", label="feedback instability")
plt.scatter(t[nexit_mask], feedback_instability[nexit_mask], color="red", s=35, label="nexit")
plt.set_title("V28 Feedback Instability")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(OUT_PATH, "v28_control_timeline.png"), dpi=160)
plt.close()

print(f"Saved -> {os.path.join(OUT_PATH, 'v28_control_timeline.png')}")

# -------------------------------------------------
# PLOT 3 — 3x3 ACTIVE MATRIX
# -------------------------------------------------
plt.figure(figsize=(9, 8))
plt.imshow(transition_matrix_norm, cmap="magma", vmin=0, vmax=np.max(transition_matrix_norm) if np.max(transition_matrix_norm) > 0 else 1)

for i in range(num_states):
    for j in range(num_states):
        if transition_matrix_norm[i, j] > 0:
            plt.text(j, i, f"{transition_matrix_norm[i, j]:.2f}", ha="center", va="center", color="white", fontsize=10)

plt.xticks(range(num_states), state_labels, rotation=45, ha="right")
plt.yticks(range(num_states), state_labels)
plt.xlabel("to")
plt.ylabel("from")
plt.title("V28 Active 3x3 Transition Matrix")
plt.colorbar(label="transition probability")
plt.tight_layout()
plt.savefig(os.path.join(OUT_PATH, "v28_active_transition_matrix.png"), dpi=160)
plt.close()

print(f"Saved -> {os.path.join(OUT_PATH, 'v28_active_transition_matrix.png')}")

# -------------------------------------------------
# PLOT 4 — STATE TIMELINE
# -------------------------------------------------
plt.figure(figsize=(16, 6))
plt.plot(t, state_code, color="black", linewidth=2, label="state code")
plt.scatter(t[engage_mask], state_code[engage_mask], color="limegreen", s=35, label="engage")
plt.scatter(t[lock_mask], state_code[lock_mask], color="deepskyblue", s=35, label="lock")
plt.scatter(t[release_mask], state_code[release_mask], color="orange", s=35, label="release")
plt.scatter(t[nexit_mask], state_code[nexit_mask], color="red", s=40, label="nexit")

plt.yticks(range(num_states), state_labels)
plt.title("V28 Active Operator State Timeline")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT_PATH, "v28_state_timeline.png"), dpi=160)
plt.close()

print(f"Saved -> {os.path.join(OUT_PATH, 'v28_state_timeline.png')}")

print("V28 ACTIVE OPERATOR / CONTROL LAYER DONE")
