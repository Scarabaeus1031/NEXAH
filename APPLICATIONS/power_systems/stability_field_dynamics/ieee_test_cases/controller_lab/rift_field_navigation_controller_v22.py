import os
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
OUT_DIR = os.path.join(BASE_PATH, "rift_extraction")
os.makedirs(OUT_DIR, exist_ok=True)

states_path = os.path.join(BASE_PATH, "states.npy")
rift_path = os.path.join(BASE_PATH, "rift.npy")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
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
# V22 — RELATIVE PHASE (remove linear carrier, keep structure)
# -------------------------------------------------
phi_rel = phi - (base_freq * t)

# symmetric wrapped phase in [-pi, pi]
theta = (phi_rel + np.pi) % (2 * np.pi) - np.pi

# -------------------------------------------------
# V22 — FLOW FEEDBACK (OKO-style internal coupling)
# -------------------------------------------------
rift_norm = np.zeros_like(rift, dtype=float)
if np.max(np.abs(rift)) > 1e-12:
    rift_norm = rift / np.max(np.abs(rift))

inst_norm = np.zeros_like(instability, dtype=float)
if np.max(np.abs(instability)) > 1e-12:
    inst_norm = instability / np.max(np.abs(instability))

feedback = 0.18 * inst_norm + 0.08 * rift_norm

theta_flow = theta + feedback
theta_flow = (theta_flow + np.pi) % (2 * np.pi) - np.pi

# -------------------------------------------------
# CONTINUOUS RING EMBEDDING (no hard channel clipping)
# -------------------------------------------------
radial = (phi - base) / (std + 1e-12)
r = 1.0 + 0.18 * np.tanh(radial)

x = r * np.cos(theta_flow)
y = r * np.sin(theta_flow)

# -------------------------------------------------
# PORTAL / ENTRY / EXIT DETECTION
# -------------------------------------------------
phase_error = phi - (base_freq * t)
portal_mask = np.abs(phase_error - np.mean(phase_error)) < 0.03

# entry/exit = zero crossings of theta_flow
zero_cross = np.where(np.diff(np.sign(theta_flow)) != 0)[0]

# high-instability transfer points
thr = np.percentile(instability, 85)
transfer_mask = instability >= thr

# -------------------------------------------------
# SAVE ARRAYS
# -------------------------------------------------
np.save(os.path.join(OUT_DIR, "field_navigation_v22.npy"), np.vstack([x, y]).T)
np.save(os.path.join(OUT_DIR, "v22_theta_flow.npy"), theta_flow)
np.save(os.path.join(OUT_DIR, "v22_radius.npy"), r)

print("Saved -> field_navigation_v22.npy")
print("Saved -> v22_theta_flow.npy")
print("Saved -> v22_radius.npy")

# -------------------------------------------------
# PLOT 1 — RELATIVE PHASE / FLOW / FEEDBACK
# -------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

axs[0].plot(t, phi, color="blue", label="phi")
axs[0].plot(t, base_freq * t, color="orange", label="carrier")
axs[0].set_title("V22 Absolute Phase vs Carrier")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, phi_rel, color="purple", label="phi_rel")
axs[1].axhline(0, color="gray", linestyle="--", alpha=0.7)
axs[1].set_title("V22 Relative Phase")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

axs[2].plot(t, theta_flow, color="green", label="theta_flow")
axs[2].scatter(t[transfer_mask], theta_flow[transfer_mask], color="red", s=18, label="transfer")
axs[2].axhline(0, color="gray", linestyle="--", alpha=0.7)
axs[2].set_title("V22 Wrapped Flow Phase")
axs[2].legend()
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
p1 = os.path.join(OUT_DIR, "v22_phase_flow.png")
plt.savefig(p1, dpi=160)
plt.close()
print(f"Saved -> {p1}")

# -------------------------------------------------
# PLOT 2 — TORUS / RING MANIFOLD PROJECTION
# -------------------------------------------------
plt.figure(figsize=(9, 9))

# guide rings
for rr in [0.82, 1.0, 1.18]:
    ang = np.linspace(0, 2*np.pi, 400)
    plt.plot(rr * np.cos(ang), rr * np.sin(ang), linestyle="--", color="gray", alpha=0.5)

# trajectory
plt.plot(x, y, color="black", alpha=0.25, linewidth=1.0)
plt.scatter(x, y, c=t, cmap="viridis", s=26, edgecolors="none", label="trajectory")

# portal points
plt.scatter(x[portal_mask], y[portal_mask], color="gold", s=42, label="portal")

# transfer points
plt.scatter(x[transfer_mask], y[transfer_mask], color="red", marker="x", s=90, label="transfer")

# zero crossings
if len(zero_cross) > 0:
    plt.scatter(x[zero_cross], y[zero_cross], color="cyan", s=28, label="entry/exit")

plt.axhline(0, color="gray", linestyle=":", alpha=0.7)
plt.axvline(0, color="gray", linestyle=":", alpha=0.7)
plt.gca().set_aspect("equal")
plt.title("V22 Open-Closed Ring Flow")
plt.legend()
plt.grid(True, alpha=0.3)

p2 = os.path.join(OUT_DIR, "v22_torus_open_closed.png")
plt.savefig(p2, dpi=160)
plt.close()
print(f"Saved -> {p2}")

# -------------------------------------------------
# PLOT 3 — ENTRY / EXIT MAP
# -------------------------------------------------
plt.figure(figsize=(12, 4))
plt.plot(t, theta_flow, color="darkgreen", label="theta_flow")
plt.axhline(0, color="gray", linestyle="--", alpha=0.7)

if len(zero_cross) > 0:
    plt.scatter(zero_cross, theta_flow[zero_cross], color="cyan", s=35, label="entry/exit")

plt.scatter(t[transfer_mask], theta_flow[transfer_mask], color="red", s=18, label="transfer")
plt.title("V22 Entry / Exit / Transfer Events")
plt.legend()
plt.grid(True, alpha=0.3)

p3 = os.path.join(OUT_DIR, "v22_entry_exit_map.png")
plt.savefig(p3, dpi=160)
plt.close()
print(f"Saved -> {p3}")

# -------------------------------------------------
# PLOT 4 — CONTINUOUS RADIAL BREATHING
# -------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

axs[0].plot(t, instability, color="darkred", label="instability")
axs[0].set_title("V22 Local Instability")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

axs[1].plot(t, r, color="teal", label="continuous radius")
axs[1].axhline(1.0, color="magenta", linestyle="--", label="base")
axs[1].axhline(1.18, color="orange", linestyle="--", label="upper guide")
axs[1].axhline(0.82, color="purple", linestyle="--", label="lower guide")
axs[1].set_title("V22 Continuous Ring Breathing")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

axs[2].plot(t, feedback, color="black", label="feedback")
axs[2].set_title("V22 Flow Feedback")
axs[2].legend()
axs[2].grid(True, alpha=0.3)

plt.tight_layout()
p4 = os.path.join(OUT_DIR, "v22_breathing_layers.png")
plt.savefig(p4, dpi=160)
plt.close()
print(f"Saved -> {p4}")

# -------------------------------------------------
# PLOT 5 — HIGHLIGHT VISUAL
# -------------------------------------------------
plt.figure(figsize=(10, 10))

# faint spiral-style connective trace
plt.plot(x, y, color="#444444", linewidth=1.2, alpha=0.35)

# color by radius
sc = plt.scatter(x, y, c=r, cmap="plasma", s=42, edgecolors="none")

# emphasize portal and transfer
plt.scatter(x[portal_mask], y[portal_mask], s=80, color="gold", edgecolors="black", linewidths=0.5, label="portal")
plt.scatter(x[transfer_mask], y[transfer_mask], s=90, color="red", marker="x", linewidths=2.0, label="transfer")

# center
plt.scatter([0], [0], s=120, color="white", edgecolors="black", linewidths=1.0)

for rr in [0.82, 1.0, 1.18]:
    ang = np.linspace(0, 2*np.pi, 400)
    plt.plot(rr * np.cos(ang), rr * np.sin(ang), linestyle="--", color="white", alpha=0.18)

plt.gca().set_aspect("equal")
plt.title("V22 Highlight — Inside-Out Ring Geometry")
plt.legend()
plt.grid(True, alpha=0.15)
plt.colorbar(sc, label="radius / layer intensity")

p5 = os.path.join(OUT_DIR, "v22_highlight_geometry.png")
plt.savefig(p5, dpi=180)
plt.close()
print(f"Saved -> {p5}")

print("V22 Open-Closed / Inside-Out Navigation DONE")
