import os
import numpy as np
import matplotlib.pyplot as plt

# =================================================
# V27 — TRIPLE RHYTHM / 3x3 CLOSURE CONTROLLER
# =================================================
# Idea:
# - build a 3-phase rhythm (intake / hold / release)
# - across 3 structural levels (local / ring / gateway)
# - yielding a 3x3 state lattice
#
# Outputs:
# 1. v27_triple_rhythm_timeline.png
# 2. v27_3x3_state_lattice.png
# 3. v27_waltz_phase_map.png
# 4. v27_gateway_breath_cycle.png
# 5. v27_closure_resonance.png
#
# Saved arrays:
# - field_navigation_v27.npy
# - v27_theta_flow.npy
# - v27_radius.npy
# - v27_state_code.npy
# - v27_rhythm_phase.npy
# - v27_gateway_strength.npy
# =================================================

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
rift_path = os.path.join(BASE_PATH, "rift.npy")

states = np.load(states_path)
print("Loaded states.npy")

if os.path.exists(rift_path):
    rift = np.load(rift_path)
    print("Loaded rift.npy")
else:
    print("rift.npy not found -> using zeros")
    rift = np.zeros(len(states))

phi = states[:, 0]
instability = states[:, 1]
t = np.arange(len(phi))
n = len(phi)

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
# PHASE / CARRIER / RELATIVE PHASE
# -------------------------------------------------
carrier = np.linspace(0.0, 1.0, n)
phi_norm = (phi - phi.min()) / (phi.max() - phi.min() + 1e-12)
phi_rel = phi_norm - carrier

# wrapped flow phase
theta_flow = np.angle(np.exp(1j * 2 * np.pi * phi_rel))

# -------------------------------------------------
# FEEDBACK INSTABILITY
# -------------------------------------------------
# smooth but still local enough to keep structure
kernel = np.array([1, 2, 3, 2, 1], dtype=float)
kernel = kernel / kernel.sum()
instability_fb = np.convolve(instability, kernel, mode="same")

# -------------------------------------------------
# V27 RHYTHM DRIVER (3-PHASE WALZER)
# -------------------------------------------------
# 0 = intake
# 1 = hold
# 2 = release
#
# Driven by modulo-3 segmentation of time plus local phase sign
rhythm_phase = np.mod(t, 3)

# slightly deform rhythm by sign of phase drift
drift_sign = np.sign(phi_rel)
rhythm_driver = (rhythm_phase + (drift_sign > 0).astype(int)) % 3

# -------------------------------------------------
# STRUCTURAL LEVELS (3 layers)
# -------------------------------------------------
# 0 = local
# 1 = ring
# 2 = gateway
#
# local: near raw flow
# ring: stable shell motion
# gateway: near zero crossing / threshold corridor
gateway_mask = np.abs(phi_rel) < 0.04
ring_mask = (np.abs(phi_rel) >= 0.04) & (np.abs(phi_rel) < 0.20)
local_mask = np.abs(phi_rel) >= 0.20

level_code = np.zeros(n, dtype=int)
level_code[ring_mask] = 1
level_code[gateway_mask] = 2

# -------------------------------------------------
# 3x3 STATE LATTICE
# -------------------------------------------------
# state_code = 3 * level + phase
#
# local   -> 0,1,2
# ring    -> 3,4,5
# gateway -> 6,7,8
state_code = 3 * level_code + rhythm_driver

state_names = {
    0: "local-intake",
    1: "local-hold",
    2: "local-release",
    3: "ring-intake",
    4: "ring-hold",
    5: "ring-release",
    6: "gate-intake",
    7: "gate-hold",
    8: "gate-release",
}

# -------------------------------------------------
# GATEWAY STRENGTH
# -------------------------------------------------
# strongest near phi_rel ~ 0 and moderate instability
gateway_strength = np.exp(-(phi_rel / 0.06) ** 2) * (0.5 + 0.5 * (1 - phi_norm))

# -------------------------------------------------
# BREATHING RADIUS
# -------------------------------------------------
# base ring + rhythm-dependent breathing + gateway compression
radius = (
    1.0
    + 0.12 * np.sin(2 * np.pi * t / max(3, n / 9))
    + 0.05 * np.cos(2 * np.pi * t / max(3, n / 27))
    - 0.18 * gateway_strength
)

# add mild dependence on structural level
radius = radius + 0.06 * (level_code - 1)

# -------------------------------------------------
# POLAR PROJECTION
# -------------------------------------------------
x = radius * np.cos(theta_flow)
y = radius * np.sin(theta_flow)

# -------------------------------------------------
# TRANSITION MATRIX FOR 3x3 LATTICE
# -------------------------------------------------
num_states = 9
transition_matrix = np.zeros((num_states, num_states), dtype=float)

for i in range(n - 1):
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
# SAVE ARRAYS
# -------------------------------------------------
np.save(os.path.join(OUT_PATH, "field_navigation_v27.npy"), np.vstack([x, y]).T)
np.save(os.path.join(OUT_PATH, "v27_theta_flow.npy"), theta_flow)
np.save(os.path.join(OUT_PATH, "v27_radius.npy"), radius)
np.save(os.path.join(OUT_PATH, "v27_state_code.npy"), state_code)
np.save(os.path.join(OUT_PATH, "v27_rhythm_phase.npy"), rhythm_driver)
np.save(os.path.join(OUT_PATH, "v27_gateway_strength.npy"), gateway_strength)
np.save(os.path.join(OUT_PATH, "v27_transition_matrix.npy"), transition_matrix_norm)

print(f"Saved -> {os.path.join(OUT_PATH, 'field_navigation_v27.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v27_theta_flow.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v27_radius.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v27_state_code.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v27_rhythm_phase.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v27_gateway_strength.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v27_transition_matrix.npy')}")

# =================================================
# VISUAL 1 — TRIPLE RHYTHM TIMELINE
# =================================================
plt.figure(figsize=(14, 7))

plt.subplot(3, 1, 1)
plt.plot(t, phi_rel, color="purple", label="relative phase")
plt.axhline(0, color="gray", linestyle="--", alpha=0.7)
plt.title("V27 Triple Rhythm — Relative Phase")
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, level_code, color="darkgreen", label="level code")
plt.yticks([0, 1, 2], ["local", "ring", "gateway"])
plt.title("V27 Structural Level")
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, state_code, color="black", linewidth=1.6, label="3x3 state code")

colors_phase = {0: "gold", 1: "deepskyblue", 2: "tomato"}
labels_phase = {0: "intake", 1: "hold", 2: "release"}

for rp in [0, 1, 2]:
    mask = rhythm_driver == rp
    plt.scatter(
        t[mask],
        state_code[mask],
        s=20,
        color=colors_phase[rp],
        label=labels_phase[rp]
    )

plt.yticks(range(9), [state_names[i] for i in range(9)])
plt.title("V27 Triple Rhythm State Timeline")
plt.legend(ncol=3, fontsize=9)
plt.grid(alpha=0.3)

plt.tight_layout()
path_1 = os.path.join(OUT_PATH, "v27_triple_rhythm_timeline.png")
plt.savefig(path_1, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved -> {path_1}")

# =================================================
# VISUAL 2 — 3x3 STATE LATTICE
# =================================================
plt.figure(figsize=(8, 7))
plt.imshow(transition_matrix_norm, cmap="magma", vmin=0, vmax=np.max(transition_matrix_norm) if np.max(transition_matrix_norm) > 0 else 1)

for i in range(num_states):
    for j in range(num_states):
        val = transition_matrix_norm[i, j]
        if val > 0:
            plt.text(j, i, f"{val:.2f}", ha="center", va="center", color="white", fontsize=9)

plt.xticks(range(9), [state_names[i] for i in range(9)], rotation=45, ha="right")
plt.yticks(range(9), [state_names[i] for i in range(9)])
plt.title("V27 3x3 State Lattice — Transition Matrix")
plt.xlabel("to")
plt.ylabel("from")
plt.colorbar(label="transition probability")
plt.tight_layout()

path_2 = os.path.join(OUT_PATH, "v27_3x3_state_lattice.png")
plt.savefig(path_2, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved -> {path_2}")

# =================================================
# VISUAL 3 — WALTZ PHASE MAP
# =================================================
plt.figure(figsize=(9, 9))

# guide rings
for rr in [0.8, 1.0, 1.2]:
    circle = plt.Circle((0, 0), rr, color="gray", fill=False, linestyle="--", alpha=0.4)
    plt.gca().add_patch(circle)

# 3 main rhythm rays
angles = [0, 2 * np.pi / 3, 4 * np.pi / 3]
for a in angles:
    plt.plot([0, 1.25 * np.cos(a)], [0, 1.25 * np.sin(a)], linestyle=":", color="gray", alpha=0.7)

phase_colors = np.array([colors_phase[r] for r in rhythm_driver])

plt.scatter(x, y, c=phase_colors, s=35, alpha=0.9)
plt.scatter(
    x[gateway_mask],
    y[gateway_mask],
    s=80,
    facecolors="none",
    edgecolors="black",
    linewidths=1.2,
    label="gateway corridor"
)

plt.scatter(0, 0, s=180, color="black", label="closure center")

plt.gca().set_aspect("equal")
plt.title("V27 Waltz Phase Map — 3 Rhythm Sectors")
plt.grid(alpha=0.3)
plt.legend()
plt.xlim(-1.35, 1.35)
plt.ylim(-1.35, 1.35)

path_3 = os.path.join(OUT_PATH, "v27_waltz_phase_map.png")
plt.savefig(path_3, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved -> {path_3}")

# =================================================
# VISUAL 4 — GATEWAY BREATH CYCLE
# =================================================
plt.figure(figsize=(14, 8))

plt.subplot(3, 1, 1)
plt.plot(t, radius, color="teal", label="breathing radius")
plt.axhline(1.0, color="magenta", linestyle="--", label="base")
plt.axhline(1.15, color="orange", linestyle="--", label="upper")
plt.axhline(0.85, color="purple", linestyle="--", label="lower")
plt.title("V27 Gateway Breath Cycle — Radius")
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(3, 1, 2)
plt.plot(t, gateway_strength, color="darkorange", label="gateway strength")
plt.fill_between(t, 0, gateway_strength, color="gold", alpha=0.25)
plt.title("V27 Gateway Strength")
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(3, 1, 3)
plt.plot(t, instability, color="lightcoral", alpha=0.5, label="raw instability")
plt.plot(t, instability_fb, color="darkred", linewidth=2, label="feedback instability")
plt.title("V27 Raw vs Feedback Instability")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
path_4 = os.path.join(OUT_PATH, "v27_gateway_breath_cycle.png")
plt.savefig(path_4, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved -> {path_4}")

# =================================================
# VISUAL 5 — CLOSURE RESONANCE
# =================================================
plt.figure(figsize=(10, 10))

# soft guide structure
for rr in np.linspace(0.3, 1.2, 4):
    circle = plt.Circle((0, 0), rr, color="gray", fill=False, linestyle="--", alpha=0.25)
    plt.gca().add_patch(circle)

# connect points softly
for i in range(n - 1):
    plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color="black", alpha=0.08)

# scatter by state family
family_colors = {
    0: "gold",         # local-intake
    1: "deepskyblue",  # local-hold
    2: "tomato",       # local-release
    3: "yellowgreen",  # ring-intake
    4: "cyan",         # ring-hold
    5: "orange",       # ring-release
    6: "khaki",        # gate-intake
    7: "dodgerblue",   # gate-hold
    8: "red",          # gate-release
}

for s in range(9):
    mask = state_code == s
    if np.any(mask):
        plt.scatter(
            x[mask],
            y[mask],
            s=28,
            color=family_colors[s],
            alpha=0.85,
            label=state_names[s]
        )

# central closure / oko-like kernel
plt.scatter(0, 0, s=250, color="black", label="closure / OKO kernel")

plt.gca().set_aspect("equal")
plt.title("V27 Closure Resonance — 3x3 Phase-Layer Field")
plt.grid(alpha=0.25)
plt.xlim(-1.35, 1.35)
plt.ylim(-1.35, 1.35)

# smaller legend
handles, labels = plt.gca().get_legend_handles_labels()
# avoid duplicates while preserving order
seen = set()
h2, l2 = [], []
for h, l in zip(handles, labels):
    if l not in seen:
        h2.append(h)
        l2.append(l)
        seen.add(l)
plt.legend(h2, l2, fontsize=8, ncol=2, loc="upper right")

path_5 = os.path.join(OUT_PATH, "v27_closure_resonance.png")
plt.savefig(path_5, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved -> {path_5}")

print("V27 TRIPLE RHYTHM / 3x3 CLOSURE DONE")
