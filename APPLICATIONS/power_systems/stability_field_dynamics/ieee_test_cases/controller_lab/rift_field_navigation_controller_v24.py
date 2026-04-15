# ============================================================
# V24 — OKO KERNEL + LOCK / ENGAGE EMERGENCE
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export/"
EXPORT_PATH = os.path.join(BASE_PATH, "rift_extraction/")
os.makedirs(EXPORT_PATH, exist_ok=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
states = np.load(os.path.join(BASE_PATH, "states.npy"))

rift_path = os.path.join(BASE_PATH, "rift.npy")
if os.path.exists(rift_path):
    rift = np.load(rift_path)
else:
    print("rift.npy not found -> using zeros")
    rift = np.zeros(len(states))

phi = states[:, 0]
instability = states[:, 1]
t = np.arange(len(phi))

print("Loaded states.npy")

# -------------------------------------------------
# BASE SYSTEM
# -------------------------------------------------
base = np.mean(phi)
spread = np.std(phi)

upper = base + spread
lower = base - spread

print(f"Base Layer:  {base:.4f} ± {spread:.4f}")
print(f"Upper Layer: {upper:.4f}")
print(f"Lower Layer: {lower:.4f}")

# carrier
carrier = np.linspace(0, 1, len(phi))

# -------------------------------------------------
# RELATIVE PHASE (WRAPPED)
# -------------------------------------------------
relative_phase = phi - carrier
relative_phase = (relative_phase + np.pi) % (2*np.pi) - np.pi

# -------------------------------------------------
# V24 — OPERATOR STATES
# -------------------------------------------------
EPS_LOCK = 0.05
EPS_ENGAGE = 0.15

lock_mask = np.abs(relative_phase) < EPS_LOCK
engage_mask = (np.abs(relative_phase) < EPS_ENGAGE) & (~lock_mask)
release_mask = (np.abs(relative_phase) >= EPS_ENGAGE) & (np.abs(relative_phase) < 0.4)
transfer_mask = np.abs(relative_phase) >= 0.4

# -------------------------------------------------
# OKO KERNEL DYNAMICS
# -------------------------------------------------
inst_norm = (instability - np.min(instability)) / (np.max(instability) - np.min(instability) + 1e-8)

radius = (
    1.0
    + 0.25 * inst_norm
    - 0.35 * np.exp(-np.abs(relative_phase))
)

radius[lock_mask] *= 0.6
radius[engage_mask] *= 0.85
radius[transfer_mask] *= 1.15

# -------------------------------------------------
# ANGLE FLOW
# -------------------------------------------------
theta = 2 * np.pi * carrier + 0.5 * relative_phase

x = radius * np.cos(theta)
y = radius * np.sin(theta)

# -------------------------------------------------
# SAVE NUMERICS
# -------------------------------------------------
np.save(os.path.join(BASE_PATH, "v24_radius.npy"), radius)
np.save(os.path.join(BASE_PATH, "v24_theta.npy"), theta)

# -------------------------------------------------
# PLOT 1 — OKO RING GEOMETRY
# -------------------------------------------------
plt.figure(figsize=(6,6))

plt.scatter(x, y, c=t, s=30)

plt.scatter(x[transfer_mask], y[transfer_mask], color="red", marker="x", label="transfer")
plt.scatter(x[lock_mask], y[lock_mask], color="cyan", label="lock")
plt.scatter(x[engage_mask], y[engage_mask], color="green", label="engage")

plt.scatter(0, 0, s=150, color="black", label="OKO kernel")

plt.title("V24 — OKO-Coupled Ring Dynamics")
plt.legend()
plt.axis("equal")

path = os.path.join(EXPORT_PATH, "v24_oko_ring.png")
plt.savefig(path)
print("Saved ->", path)
plt.close()

# -------------------------------------------------
# PLOT 2 — STATE TIMELINE
# -------------------------------------------------
plt.figure(figsize=(10,4))

state = np.zeros(len(phi))

state[engage_mask] = 1
state[lock_mask] = 2
state[release_mask] = 3
state[transfer_mask] = 4

plt.plot(state, color="black")

plt.scatter(np.where(transfer_mask), state[transfer_mask], color="red")
plt.scatter(np.where(lock_mask), state[lock_mask], color="cyan")
plt.scatter(np.where(engage_mask), state[engage_mask], color="green")

plt.yticks([0,1,2,3,4], ["none","engage","lock","release","transfer"])
plt.title("V24 Operator Timeline")

path = os.path.join(EXPORT_PATH, "v24_operator_timeline.png")
plt.savefig(path)
print("Saved ->", path)
plt.close()

# -------------------------------------------------
# PLOT 3 — PHASE + STATES
# -------------------------------------------------
plt.figure(figsize=(10,6))

plt.subplot(2,1,1)
plt.plot(phi, label="phi")
plt.plot(carrier, label="carrier")
plt.legend()
plt.title("Phase vs Carrier")

plt.subplot(2,1,2)
plt.plot(relative_phase, label="relative phase")

plt.scatter(np.where(lock_mask), relative_phase[lock_mask], color="cyan")
plt.scatter(np.where(engage_mask), relative_phase[engage_mask], color="green")
plt.scatter(np.where(transfer_mask), relative_phase[transfer_mask], color="red")

plt.legend()

path = os.path.join(EXPORT_PATH, "v24_phase_states.png")
plt.savefig(path)
print("Saved ->", path)
plt.close()

print("V24 OKO SYSTEM DONE")
