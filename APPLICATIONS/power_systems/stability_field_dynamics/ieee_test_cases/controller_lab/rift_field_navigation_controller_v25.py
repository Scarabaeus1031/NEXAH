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
# PHASE / CARRIER / RELATIVE PHASE
# -------------------------------------------------
carrier = np.linspace(0.0, 1.0, len(phi))
phi_norm = (phi - phi.min()) / (phi.max() - phi.min() + 1e-12)
phi_rel = phi_norm - carrier

# wrapped flow
theta_flow = np.mod(phi_rel, 2 * np.pi)
theta_vis = np.interp(
    phi_rel,
    (phi_rel.min(), phi_rel.max()),
    (-0.45, 1.05)
)

# -------------------------------------------------
# SMOOTH INSTABILITY
# -------------------------------------------------
win = 7
kernel = np.ones(win) / win
instability = np.convolve(instability_raw, kernel, mode="same")

# normalize instability
inst_norm = (instability - instability.min()) / (instability.max() - instability.min() + 1e-12)

# -------------------------------------------------
# FEEDBACK FIELD
# -------------------------------------------------
# core idea:
# lock reduces effective instability
# transfer increases it
# engage compresses drift before lock

feedback_seed = np.zeros(len(phi))

# pre-feedback geometric seed from relative phase
feedback_seed += 0.12 * np.cos(theta_flow)
feedback_seed += 0.08 * np.sin(2 * theta_flow)

# add weak rift contribution if present
if len(rift) == len(phi):
    rift_norm = (rift - np.min(rift)) / (np.max(rift) - np.min(rift) + 1e-12)
    feedback_seed += 0.06 * (rift_norm - 0.5)
else:
    rift_norm = np.zeros(len(phi))

# blended feedback instability
inst_feedback = 0.72 * inst_norm + 0.28 * (0.5 + feedback_seed)

# smooth again
inst_feedback = np.convolve(inst_feedback, kernel, mode="same")
inst_feedback = np.clip(inst_feedback, 0.0, 1.0)

# -------------------------------------------------
# BREATHING RADIUS
# -------------------------------------------------
# higher radius outside, lower radius near lock
radius = 1.16 - 0.36 * inst_feedback

# add subtle breathing
radius += 0.035 * np.cos(theta_flow)
radius += 0.02 * np.sin(3 * theta_flow)

# gentle re-smooth
radius = np.convolve(radius, kernel, mode="same")

# guides
base_ring = 1.00
upper_ring = 1.16
lower_ring = 0.84

# -------------------------------------------------
# OPERATOR STATE DETECTION
# -------------------------------------------------
# logic:
# - lock: near relative-phase crossing and low feedback instability
# - engage: around lock, slightly higher radius / just before lock
# - release: after lock while moving away
# - transfer: outer high-radius + unstable zones

dphi_rel = np.gradient(phi_rel)
dradius = np.gradient(radius)

portal_mask = np.abs(phi_rel) < 0.035

lock_mask = (np.abs(phi_rel) < 0.09) & (inst_feedback < 0.36) & (radius < 0.96)
engage_mask = (np.abs(phi_rel) < 0.16) & (inst_feedback < 0.48) & (radius < 1.02) & (~lock_mask)
release_mask = (np.abs(phi_rel) < 0.22) & (dradius > 0.001) & (~lock_mask) & (~engage_mask)
transfer_mask = (radius > 1.08) | ((inst_feedback > 0.62) & (np.abs(phi_rel) > 0.28))

# strengthen state continuity
def dilate(mask, k=2):
    out = mask.copy()
    idx = np.where(mask)[0]
    for i in idx:
        lo = max(0, i-k)
        hi = min(len(mask), i+k+1)
        out[lo:hi] = True
    return out

lock_mask = dilate(lock_mask, 1)
engage_mask = dilate(engage_mask, 1) & (~lock_mask)
release_mask = dilate(release_mask, 1) & (~lock_mask) & (~engage_mask)
transfer_mask = dilate(transfer_mask, 0) & (~lock_mask)

# exit / entry from sign change of relative phase
sign_change = np.where(np.diff(np.sign(phi_rel)) != 0)[0]
entry_exit_mask = np.zeros(len(phi), dtype=bool)
entry_exit_mask[sign_change] = True

# -------------------------------------------------
# TIMELINE STATES
# 0 none, 1 portal, 2 engage, 3 lock, 4 release, 5 transfer, 6 exit
# -------------------------------------------------
state_code = np.zeros(len(phi), dtype=int)
state_code[portal_mask] = 1
state_code[engage_mask] = 2
state_code[lock_mask] = 3
state_code[release_mask] = 4
state_code[transfer_mask] = 5
state_code[entry_exit_mask] = 6

# -------------------------------------------------
# GEOMETRY
# -------------------------------------------------
x = radius * np.cos(theta_vis)
y = radius * np.sin(theta_vis)

# OKO kernel
oko_x, oko_y = 0.0, 0.0

# -------------------------------------------------
# SAVE ARRAYS
# -------------------------------------------------
np.save(os.path.join(OUT_PATH, "field_navigation_v25.npy"), np.vstack([x, y]).T)
np.save(os.path.join(OUT_PATH, "v25_theta_flow.npy"), theta_flow)
np.save(os.path.join(OUT_PATH, "v25_radius.npy"), radius)
np.save(os.path.join(OUT_PATH, "v25_state_code.npy"), state_code)
np.save(os.path.join(OUT_PATH, "v25_instability_feedback.npy"), inst_feedback)

print(f"Saved -> {os.path.join(OUT_PATH, 'field_navigation_v25.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v25_theta_flow.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v25_radius.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v25_state_code.npy')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v25_instability_feedback.npy')}")

# -------------------------------------------------
# PLOT 1 — PHASE + STATES
# -------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

axs[0].plot(t, phi_norm, color="royalblue", label="phi")
axs[0].plot(t, carrier, color="orange", label="carrier")
axs[0].set_title("V25 Phase vs Carrier")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, phi_rel, color="purple", label="relative phase")
axs[1].scatter(t[portal_mask], phi_rel[portal_mask], color="gold", s=28, label="portal", zorder=3)
axs[1].scatter(t[engage_mask], phi_rel[engage_mask], color="limegreen", s=20, label="engage", zorder=3)
axs[1].scatter(t[lock_mask], phi_rel[lock_mask], color="deepskyblue", s=20, label="lock", zorder=3)
axs[1].scatter(t[release_mask], phi_rel[release_mask], color="orange", s=20, label="release", zorder=3)
axs[1].scatter(t[entry_exit_mask], phi_rel[entry_exit_mask], color="red", s=24, label="exit/entry", zorder=3)
axs[1].axhline(0, color="gray", linestyle="--", alpha=0.6)
axs[1].set_title("V25 Relative Phase + Stable States")
axs[1].legend(loc="upper right")
axs[1].grid(True, alpha=0.3)

axs[2].plot(t, inst_feedback, color="darkred", label="feedback instability")
axs[2].scatter(t[transfer_mask], inst_feedback[transfer_mask], color="red", marker="x", s=70, label="transfer")
axs[2].set_title("V25 Feedback Instability + Transfer Events")
axs[2].legend()
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
p1 = os.path.join(OUT_PATH, "v25_phase_states.png")
plt.savefig(p1, dpi=150)
plt.close()
print(f"Saved -> {p1}")

# -------------------------------------------------
# PLOT 2 — STABLE LOCK RING
# -------------------------------------------------
plt.figure(figsize=(8, 8))
plt.scatter(x, y, c=t, cmap="viridis", s=36, edgecolors="none", label="trajectory")
plt.scatter(x[portal_mask], y[portal_mask], color="gold", edgecolor="black", s=120, label="portal", zorder=5)
plt.scatter(x[engage_mask], y[engage_mask], color="limegreen", s=40, label="engage", zorder=4)
plt.scatter(x[lock_mask], y[lock_mask], color="deepskyblue", s=40, label="lock", zorder=4)
plt.scatter(x[release_mask], y[release_mask], color="orange", s=40, label="release", zorder=4)
plt.scatter(x[transfer_mask], y[transfer_mask], color="red", marker="x", s=90, label="transfer", zorder=6)
plt.scatter([oko_x], [oko_y], color="black", s=180, label="OKO kernel", zorder=7)

for rr in [lower_ring, base_ring, upper_ring]:
    circle = plt.Circle((0, 0), rr, fill=False, linestyle="--", color="gray", alpha=0.5)
    plt.gca().add_patch(circle)

plt.axhline(0, color="gray", linestyle=":", alpha=0.7)
plt.axvline(0, color="gray", linestyle=":", alpha=0.7)
plt.gca().set_aspect("equal")
plt.title("V25 Stable Lock / Engage / Release Ring Geometry")
plt.legend(loc="lower left")
plt.grid(True, alpha=0.2)

p2 = os.path.join(OUT_PATH, "v25_stable_lock_ring.png")
plt.savefig(p2, dpi=150)
plt.close()
print(f"Saved -> {p2}")

# -------------------------------------------------
# PLOT 3 — TIMELINE
# -------------------------------------------------
plt.figure(figsize=(14, 4))
plt.plot(t, state_code, color="black", linewidth=2)

plt.scatter(t[portal_mask], state_code[portal_mask], color="gold", s=30, label="portal")
plt.scatter(t[engage_mask], state_code[engage_mask], color="limegreen", s=24, label="engage")
plt.scatter(t[lock_mask], state_code[lock_mask], color="deepskyblue", s=24, label="lock")
plt.scatter(t[release_mask], state_code[release_mask], color="orange", s=24, label="release")
plt.scatter(t[transfer_mask], state_code[transfer_mask], color="red", marker="x", s=60, label="transfer")
plt.scatter(t[entry_exit_mask], state_code[entry_exit_mask], color="darkred", s=28, label="exit/entry")

plt.yticks(
    [0, 1, 2, 3, 4, 5, 6],
    ["none", "portal", "engage", "lock", "release", "transfer", "exit"]
)
plt.title("V25 Operator Timeline")
plt.grid(True, alpha=0.3)
plt.legend(loc="upper left")

p3 = os.path.join(OUT_PATH, "v25_operator_timeline.png")
plt.savefig(p3, dpi=150)
plt.close()
print(f"Saved -> {p3}")

# -------------------------------------------------
# PLOT 4 — FEEDBACK BREATHING
# -------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

axs[0].plot(t, instability_raw, color="firebrick", alpha=0.35, label="raw instability")
axs[0].plot(t, inst_feedback, color="darkred", linewidth=2, label="feedback instability")
axs[0].legend()
axs[0].set_title("V25 Raw vs Feedback Instability")
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, radius, color="teal", linewidth=2, label="radius")
axs[1].axhline(base_ring, color="magenta", linestyle="--", label="base")
axs[1].axhline(upper_ring, color="orange", linestyle="--", label="upper")
axs[1].axhline(lower_ring, color="purple", linestyle="--", label="lower")
axs[1].legend()
axs[1].set_title("V25 Breathing Radius")
axs[1].grid(True, alpha=0.3)

axs[2].plot(t, dphi_rel, color="slateblue", label="d(relative phase)/dt")
axs[2].plot(t, dradius, color="gray", label="d(radius)/dt")
axs[2].legend()
axs[2].set_title("V25 Dynamic Derivatives")
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
p4 = os.path.join(OUT_PATH, "v25_feedback_breathing.png")
plt.savefig(p4, dpi=150)
plt.close()
print(f"Saved -> {p4}")

print("V25 CLOSED FEEDBACK + STABLE LOCK DONE")
