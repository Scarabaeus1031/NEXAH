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

rift_path = os.path.join(BASE_PATH, "rift.npy")
if os.path.exists(rift_path):
    rift = np.load(rift_path)
    print("Loaded rift.npy")
else:
    print("rift.npy not found -> using zeros")
    rift = np.zeros(len(states))

print("Loaded states.npy")

phi = states[:, 0]
instability = states[:, 1]
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
# RELATIVE / WRAPPED PHASE
# -------------------------------------------------
carrier = base_freq * t
phi_rel = phi - carrier
theta_flow = phi_rel.copy()

# normalize to ring-like angular interval
theta_min = np.min(theta_flow)
theta_max = np.max(theta_flow)
theta_norm = (theta_flow - theta_min) / (theta_max - theta_min + 1e-12)

# map to angular arc
theta = np.pi * (1.05 - 1.35 * theta_norm)

# -------------------------------------------------
# CONTINUOUS RADIUS FIELD
# -------------------------------------------------
inst_norm = (instability - instability.min()) / (instability.max() - instability.min() + 1e-12)

radius = 1.15 - 0.32 * theta_norm + 0.03 * (0.5 - inst_norm)

# guides
r_upper = np.max(radius)
r_lower = np.min(radius)
r_base  = np.mean(radius)

# -------------------------------------------------
# EVENT DETECTION
# -------------------------------------------------
# portal = near structural center band
portal_mask = np.abs(phi_rel) < 0.03

# transfer = high local curvature / slope jumps
dtheta = np.gradient(theta_flow)
transfer_mask = np.abs(np.gradient(dtheta)) > np.percentile(np.abs(np.gradient(dtheta)), 82)

# engage = first entering stable corridor
engage_mask = (phi_rel > 0.02) & (phi_rel < 0.10) & (t < 25)

# lock = low instability + near base ring
lock_mask = (instability < np.percentile(instability, 35)) & (np.abs(radius - r_base) < 0.02)

# release = leaving lock region
lock_shift = np.roll(lock_mask, 1)
release_mask = (lock_shift == True) & (lock_mask == False)

# exit = crossing through central phase axis toward open side
exit_mask = (np.abs(theta_flow) < 0.05) & (t > int(0.65 * len(t)))

# -------------------------------------------------
# TORUS / RING PROJECTION
# -------------------------------------------------
x = radius * np.cos(theta)
y = radius * np.sin(theta)

np.save(os.path.join(OUT_PATH, "field_navigation_v23.npy"), np.vstack([x, y]).T)
np.save(os.path.join(OUT_PATH, "v23_theta_flow.npy"), theta_flow)
np.save(os.path.join(OUT_PATH, "v23_radius.npy"), radius)

print("Saved -> field_navigation_v23.npy")
print("Saved -> v23_theta_flow.npy")
print("Saved -> v23_radius.npy")

# -------------------------------------------------
# PLOT 1 — PHASE / FLOW / EVENTS
# -------------------------------------------------
plt.figure(figsize=(14, 10))

plt.subplot(3, 1, 1)
plt.plot(t, phi, color="blue", label="phi")
plt.plot(t, carrier, color="orange", label="carrier")
plt.legend()
plt.grid(alpha=0.3)
plt.title("V23 Phase vs Carrier")

plt.subplot(3, 1, 2)
plt.plot(t, phi_rel, color="purple", label="relative phase")
plt.axhline(0, color="gray", linestyle="--")
plt.scatter(t[portal_mask], phi_rel[portal_mask], color="gold", s=30, label="portal")
plt.scatter(t[engage_mask], phi_rel[engage_mask], color="limegreen", s=20, label="engage")
plt.scatter(t[lock_mask], phi_rel[lock_mask], color="deepskyblue", s=14, label="lock")
plt.scatter(t[release_mask], phi_rel[release_mask], color="orange", s=36, label="release")
plt.scatter(t[exit_mask], phi_rel[exit_mask], color="red", s=30, label="exit")
plt.legend()
plt.grid(alpha=0.3)
plt.title("V23 Relative Phase + Operator States")

plt.subplot(3, 1, 3)
plt.plot(t, instability, color="darkred", label="instability")
plt.scatter(t[transfer_mask], instability[transfer_mask], color="red", marker="x", s=60, label="transfer")
plt.legend()
plt.grid(alpha=0.3)
plt.title("V23 Instability + Transfer Events")

plt.tight_layout()
plt.savefig(os.path.join(OUT_PATH, "v23_phase_operator_states.png"), dpi=160)
plt.close()

# -------------------------------------------------
# PLOT 2 — OPEN-CLOSED RING FLOW
# -------------------------------------------------
plt.figure(figsize=(10, 10))

sc = plt.scatter(x, y, c=t, cmap="viridis", s=28, label="trajectory")
plt.colorbar(sc, label="time index")

plt.scatter(x[portal_mask], y[portal_mask], color="gold", edgecolor="black", s=90, label="portal")
plt.scatter(x[engage_mask], y[engage_mask], color="limegreen", s=45, label="engage")
plt.scatter(x[lock_mask], y[lock_mask], color="deepskyblue", s=25, label="lock")
plt.scatter(x[release_mask], y[release_mask], color="orange", s=70, label="release")
plt.scatter(x[exit_mask], y[exit_mask], color="red", s=55, label="exit")
plt.scatter(x[transfer_mask], y[transfer_mask], color="red", marker="x", s=90, label="transfer")

# guide rings
for rr in [r_lower, r_base, r_upper]:
    circ = plt.Circle((0, 0), rr, fill=False, linestyle="--", color="gray", alpha=0.5)
    plt.gca().add_patch(circ)

# Oko kernel
plt.scatter([0], [0], color="black", s=180, label="Oko kernel")

plt.axhline(0, color="gray", linestyle=":")
plt.axvline(0, color="gray", linestyle=":")

plt.gca().set_aspect("equal")
plt.title("V23 Engage / Lock / Release Ring Geometry")
plt.legend()
plt.grid(alpha=0.2)
plt.savefig(os.path.join(OUT_PATH, "v23_ring_operator_map.png"), dpi=160)
plt.close()

# -------------------------------------------------
# PLOT 3 — 10-GON / 2x5 FOLD FIELD
# -------------------------------------------------
plt.figure(figsize=(10, 10))

plt.scatter(x, y, c="lightgray", s=10)

# outer decagon
N = 10
angles = np.linspace(0, 2*np.pi, N, endpoint=False) + np.pi/10
R = r_base * 0.98
dx = R * np.cos(angles)
dy = R * np.sin(angles)

for i in range(N):
    j = (i + 1) % N
    plt.plot([dx[i], dx[j]], [dy[i], dy[j]], color="black", alpha=0.35)

# two shifted pentagon folds
P = 5
angles_a = np.linspace(0, 2*np.pi, P, endpoint=False) + np.pi/2
angles_b = angles_a + np.pi/5

Ra = r_base * 0.78
Rb = r_base * 0.78

axp = Ra * np.cos(angles_a)
ayp = Ra * np.sin(angles_a)
bxp = Rb * np.cos(angles_b)
byp = Rb * np.sin(angles_b)

for i in range(P):
    j = (i + 1) % P
    plt.plot([axp[i], axp[j]], [ayp[i], ayp[j]], color="magenta", linewidth=2, alpha=0.75)
    plt.plot([bxp[i], bxp[j]], [byp[i], byp[j]], color="cyan", linewidth=2, alpha=0.75)

# X-star
plt.plot([-r_base*0.85, r_base*0.85], [-r_base*0.85, r_base*0.85], color="red", linestyle="--", alpha=0.5)
plt.plot([-r_base*0.85, r_base*0.85], [r_base*0.85, -r_base*0.85], color="red", linestyle="--", alpha=0.5)

plt.scatter([0], [0], color="black", s=160)
plt.gca().set_aspect("equal")
plt.title("V23 Decagon + 2x5 Fold Geometry")
plt.grid(alpha=0.2)
plt.savefig(os.path.join(OUT_PATH, "v23_fold_geometry.png"), dpi=160)
plt.close()

# -------------------------------------------------
# PLOT 4 — STATE TIMELINE
# -------------------------------------------------
state_code = np.zeros(len(t))
state_code[portal_mask] = 1
state_code[engage_mask] = 2
state_code[lock_mask] = 3
state_code[transfer_mask] = 4
state_code[release_mask] = 5
state_code[exit_mask] = 6

plt.figure(figsize=(14, 4))
plt.plot(t, state_code, color="black", linewidth=1.2)
plt.scatter(t[portal_mask], state_code[portal_mask], color="gold", label="portal")
plt.scatter(t[engage_mask], state_code[engage_mask], color="limegreen", label="engage")
plt.scatter(t[lock_mask], state_code[lock_mask], color="deepskyblue", label="lock")
plt.scatter(t[transfer_mask], state_code[transfer_mask], color="red", marker="x", label="transfer")
plt.scatter(t[release_mask], state_code[release_mask], color="orange", label="release")
plt.scatter(t[exit_mask], state_code[exit_mask], color="red", label="exit")

plt.yticks([0,1,2,3,4,5,6], ["none","portal","engage","lock","transfer","release","exit"])
plt.grid(alpha=0.3)
plt.legend()
plt.title("V23 Operator State Timeline")
plt.savefig(os.path.join(OUT_PATH, "v23_state_timeline.png"), dpi=160)
plt.close()

print(f"Saved -> {os.path.join(OUT_PATH, 'v23_phase_operator_states.png')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v23_ring_operator_map.png')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v23_fold_geometry.png')}")
print(f"Saved -> {os.path.join(OUT_PATH, 'v23_state_timeline.png')}")

print("V23 Engage / Lock / Release Navigation DONE")
