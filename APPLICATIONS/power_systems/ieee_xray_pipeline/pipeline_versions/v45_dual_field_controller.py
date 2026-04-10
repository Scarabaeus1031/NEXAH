import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# PATHS
# ============================================================
OUTDIR = Path("/Users/tho2020/Documents/GitHub/NEXAH/APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = OUTDIR / "v45_dual_field_report.txt"
TS_PATH     = OUTDIR / "v45_dual_field_timeseries.png"
POLAR_PATH  = OUTDIR / "v45_dual_field_polar.png"
CUBE_PATH   = OUTDIR / "v45_dual_field_3d.png"
FIELD_PATH  = OUTDIR / "v45_dual_field_topology.png"

print(f"\n📁 v45 running → {OUTDIR.resolve()}\n")

# ============================================================
# OLGO LAYER
# ============================================================
phi = (1 + np.sqrt(5)) / 2
pi = np.pi

f0 = (phi ** 3) / (pi ** 2)
epsilon = 0.029
shells = np.array([f0, f0 + epsilon, f0 + 2 * epsilon])
shell_names = ["Core", "Transition", "Expansion"]

def olgo_proximity(z, sharpness=80.0):
    d = np.min(np.abs(shells - z))
    return np.exp(-sharpness * d)

def nearest_shell(z):
    idx = np.argmin(np.abs(shells - z))
    return shells[idx], idx

# ============================================================
# HELPERS
# ============================================================
def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

def phase_to_sector(angle, n=6):
    a = (angle + 2 * np.pi) % (2 * np.pi)
    return int(np.floor(a / (2 * np.pi / n))) % n

def smooth_step(x, x0, k=20.0):
    return 1.0 / (1.0 + np.exp(-k * (x - x0)))

# ============================================================
# HEX FIELD GEOMETRY
# ============================================================
hex_angles = np.linspace(0, 2*np.pi, 7)[:-1]
hex_nodes = np.array([(np.cos(a), np.sin(a)) for a in hex_angles])
center_node = np.array([[0.0, 0.0]])

# ============================================================
# GRID SETUP
# ============================================================
np.random.seed(42)
net = pp.networks.case57()
net.load.p_mw *= 0.85
net.load.q_mvar *= 0.85

# ============================================================
# STORAGE
# ============================================================
controlled = {
    "voltage": [],
    "coherence": [],
    "radius": [],
    "theta": [],
    "z_olgo": [],
    "olgo_prox": [],
    "shell_index": [],
    "u": [],
    "u_ieee": [],
    "u_field": [],
    "u_lock": [],
    "u_reentry": [],
    "psi": [],
    "field_radius": [],
    "field_node": [],
    "field_switch": [],
    "loop_event": [],
    "field_x": [],
    "field_y": [],
    "mode": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2
target_radius = 0.045

# IEEE controller gains
k_r = 0.08
k_theta = 0.04
k_lock = 0.035

# synthetic field gains
psi_drive_gain = 0.08
psi_res_gain = 0.18
psi_cross_gain = 0.12

field_breath_base = 0.55
field_breath_amp = 0.18
field_breath_freq = 0.045

reentry_gain = 0.05
field_align_gain = 0.04

prox_threshold = 0.30
u_clip = 0.08

# ============================================================
# INTERNAL FIELD STATE
# ============================================================
psi = -np.pi / 2
prev_theta = None
prev_field_node = None

escape_count = 0
lock_count = 0
field_switch_count = 0
loop_count = 0

# ============================================================
# MAIN LOOP
# ============================================================
for t in range(T):
    pp.runpp(net, enforce_q_lims=True)

    vm = net.res_bus.vm_pu.values
    v_mean = np.mean(vm)

    coh = 1.0 - np.std(vm)
    sw = (v_mean - 1.0) * 10.0

    # --------------------------------------------------------
    # real IEEE state
    # --------------------------------------------------------
    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = wrap_angle(np.arctan2(sw - 0.000076, coh - 0.942913))

    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo)
    _, shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # event estimate from IEEE
    # --------------------------------------------------------
    crossing_signal = 0.0
    if prev_theta is not None:
        prev_err = wrap_angle(prev_theta - theta_ref)
        curr_err = wrap_angle(theta - theta_ref)
        if prev_err * curr_err < 0:
            crossing_signal = 1.0

    # --------------------------------------------------------
    # dynamic synthetic field
    # psi is not theta. psi is driven by theta, resonance, and history.
    # --------------------------------------------------------
    psi_dot = 0.0
    psi_dot += psi_drive_gain * np.sin(theta - psi)
    psi_dot += psi_res_gain * prox * np.sin(theta_ref - psi)
    psi_dot += psi_cross_gain * crossing_signal * np.sign(np.sin(theta - theta_ref) + 1e-6)

    psi = wrap_angle(psi + psi_dot)

    # breathing field radius
    field_radius = field_breath_base + field_breath_amp * np.sin(field_breath_freq * t + psi)

    # field node comes from psi, not theta
    field_node = phase_to_sector(psi, n=6)

    field_switch = 0
    if prev_field_node is not None and field_node != prev_field_node:
        field_switch = 1
        field_switch_count += 1

    # --------------------------------------------------------
    # loop logic
    # loop is activated when field radius contracts and prox is not too low
    # --------------------------------------------------------
    loop_gate = smooth_step(field_breath_base - field_radius, 0.02, k=20.0)
    loop_event = 1 if (loop_gate > 0.5 and prox > 0.02) else 0
    if loop_event:
        loop_count += 1

    # --------------------------------------------------------
    # topology coordinates
    # --------------------------------------------------------
    sector_angle = hex_angles[field_node]
    fx = field_radius * np.cos(sector_angle)
    fy = field_radius * np.sin(sector_angle)

    # --------------------------------------------------------
    # control composition
    # --------------------------------------------------------
    # A) IEEE layer
    phase_err_ieee = wrap_angle(theta - theta_ref)
    u_ieee = 0.0
    u_ieee += -k_r * (r - target_radius)
    u_ieee += -k_theta * np.sin(phase_err_ieee)

    # B) OLGO shell pull
    shell_target = shells[1] if loop_event else shells[2]
    u_lock = -k_lock * (z_olgo - shell_target)

    # C) Synthetic field alignment
    # forward = sector-alignment
    # feedback = field-to-reference correction
    u_field = 0.0
    u_field += field_align_gain * np.cos(theta - sector_angle)
    u_field += 0.03 * np.cos(theta - psi)

    # D) loop reentry
    u_reentry = 0.0
    if loop_event:
        u_reentry += reentry_gain * np.cos(theta - sector_angle)
        u_reentry += 0.04 * np.cos(theta_ref - theta)

    u = u_ieee + u_lock + u_field + u_reentry

    if prox > prox_threshold:
        lock_count += 1
        u *= 0.70

    u = np.clip(u, -u_clip, u_clip)

    # --------------------------------------------------------
    # apply
    # --------------------------------------------------------
    factor = 1.0 + u * 0.08
    net.load.p_mw *= factor
    net.load.q_mvar *= factor

    # --------------------------------------------------------
    # store
    # --------------------------------------------------------
    controlled["voltage"].append(v_mean)
    controlled["coherence"].append(coh)
    controlled["radius"].append(r)
    controlled["theta"].append(theta)
    controlled["z_olgo"].append(z_olgo)
    controlled["olgo_prox"].append(prox)
    controlled["shell_index"].append(shell_idx)
    controlled["u"].append(u)
    controlled["u_ieee"].append(u_ieee)
    controlled["u_field"].append(u_field)
    controlled["u_lock"].append(u_lock)
    controlled["u_reentry"].append(u_reentry)
    controlled["psi"].append(psi)
    controlled["field_radius"].append(field_radius)
    controlled["field_node"].append(field_node)
    controlled["field_switch"].append(field_switch)
    controlled["loop_event"].append(loop_event)
    controlled["field_x"].append(fx)
    controlled["field_y"].append(fy)
    controlled["mode"].append("loop" if loop_event else "field")

    if r > 0.055:
        escape_count += 1

    prev_theta = theta
    prev_field_node = field_node

# ============================================================
# REPORT
# ============================================================
shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["shell_index"]) == i))
    for i in range(len(shells))
}

field_node_counts = {
    f"node_{i}": int(np.sum(np.array(controlled["field_node"]) == i))
    for i in range(6)
}

report = f"""NEXAH v45 – Dual Field Controller

Escape count: {escape_count}
Field switch count: {field_switch_count}
Loop count: {loop_count}
Lock count (prox > {prox_threshold}): {lock_count}

Mean voltage: {np.mean(controlled['voltage']):.4f}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean radius: {np.mean(controlled['radius']):.4f}

Mean OLGO proximity: {np.mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {np.max(controlled['olgo_prox']):.4f}
Mean control signal: {np.mean(controlled['u']):.4f}

Observed shell occupancy:
  Core: {shell_hits['Core']}
  Transition: {shell_hits['Transition']}
  Expansion: {shell_hits['Expansion']}

Field node occupancy:
  node_0: {field_node_counts['node_0']}
  node_1: {field_node_counts['node_1']}
  node_2: {field_node_counts['node_2']}
  node_3: {field_node_counts['node_3']}
  node_4: {field_node_counts['node_4']}
  node_5: {field_node_counts['node_5']}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print(report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(8, 1, figsize=(14, 20), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v45 Dual Field Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple", label="IEEE radius")
axs[2].plot(controlled["field_radius"], color="hotpink", alpha=0.8, label="field radius")
axs[2].axhline(target_radius, color="green", linestyle="--", alpha=0.7)
axs[2].set_ylabel("Radius")
axs[2].legend()

axs[3].plot(controlled["theta"], color="teal", label="theta")
axs[3].plot(controlled["psi"], color="darkviolet", alpha=0.8, label="psi (field phase)")
axs[3].axhline(theta_ref, color="gold", linestyle="--", alpha=0.7, label="theta_ref")
axs[3].set_ylabel("Phase")
axs[3].legend()

axs[4].plot(controlled["z_olgo"], color="slateblue")
for s in shells:
    axs[4].axhline(s, color="gray", linestyle="--", alpha=0.5)
axs[4].set_ylabel("OLGO Z")

axs[5].plot(controlled["u"], color="black", label="u")
axs[5].plot(controlled["u_ieee"], color="gray", alpha=0.8, label="ieee")
axs[5].plot(controlled["u_field"], color="gold", alpha=0.8, label="field")
axs[5].plot(controlled["u_lock"], color="red", alpha=0.8, label="lock")
axs[5].plot(controlled["u_reentry"], color="cyan", alpha=0.8, label="reentry")
axs[5].set_ylabel("Control")
axs[5].legend(ncol=5)

axs[6].plot(controlled["field_node"], color="darkviolet")
axs[6].set_ylabel("Field node")

axs[7].plot(controlled["field_switch"], color="purple", label="field switch")
axs[7].plot(controlled["loop_event"], color="hotpink", label="loop")
axs[7].set_ylabel("Events")
axs[7].set_xlabel("Time step")
axs[7].legend()

fig.tight_layout()
fig.savefig(TS_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# POLAR
# ============================================================
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="polar")

theta_vals = np.array(controlled["theta"])
r_vals = np.array(controlled["radius"])
prox_vals = np.array(controlled["olgo_prox"])

psi_vals = np.array(controlled["psi"])
fr_vals = np.array(controlled["field_radius"])
loop_vals = np.array(controlled["loop_event"])

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="IEEE trajectory")
ax.plot(psi_vals, fr_vals, color="hotpink", alpha=0.7, label="Field trajectory")
sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

loop_idx = np.where(loop_vals > 0)[0]
if len(loop_idx) > 0:
    ax.scatter(psi_vals[loop_idx], fr_vals[loop_idx], color="hotpink", s=20, label="loop events")

ax.set_title("v45 Dual Field Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# 3D
# ============================================================
fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(projection="3d")

x = np.array(controlled["radius"])
y = np.array(controlled["theta"])
z = np.array(controlled["z_olgo"])
c = np.array(controlled["olgo_prox"])

sc = ax.scatter(x, y, z, c=c, cmap="plasma", s=14, label="IEEE")

# overlay field as synthetic topological path
fx = np.array(controlled["field_x"])
fy = np.array(controlled["field_y"])
fz = np.array(controlled["field_radius"])
ax.plot(fx, fy, fz, color="hotpink", linewidth=1.6, alpha=0.8)

ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("OLGO Z / Field R")
ax.set_title("v45 Dual Field 3D")

for s in shells:
    ax.plot([x.min(), x.max()], [theta_ref, theta_ref], [s, s], linestyle="--", alpha=0.35)

fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# FIELD TOPOLOGY VIEW
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

# draw hexagon
for i in range(6):
    x1, y1 = hex_nodes[i]
    x2, y2 = hex_nodes[(i + 1) % 6]
    ax.plot([x1, x2], [y1, y2], color="gray", alpha=0.8)

# spokes
for i in range(6):
    x1, y1 = hex_nodes[i]
    ax.plot([0, x1], [0, y1], color="lightgray", alpha=0.6)

# node points
ax.scatter(hex_nodes[:, 0], hex_nodes[:, 1], s=180, c="skyblue")
ax.scatter(center_node[:, 0], center_node[:, 1], s=220, c="hotpink")

for i, (xn, yn) in enumerate(hex_nodes):
    ax.text(xn * 1.08, yn * 1.08, f"{i}", ha="center", va="center", fontsize=12)
ax.text(0, 0, "loop", ha="center", va="center", fontsize=12, color="white")

# overlay field trajectory
ax.plot(controlled["field_x"], controlled["field_y"], color="hotpink", linewidth=1.5, alpha=0.8)

node_occ = np.array([field_node_counts[f"node_{i}"] for i in range(6)], dtype=float)
if node_occ.max() > 0:
    node_occ = node_occ / node_occ.max()
    for i, (xn, yn) in enumerate(hex_nodes):
        ax.scatter([xn], [yn], s=400 * node_occ[i] + 40, alpha=0.25, c="navy")

ax.set_title("v45 Dynamic Field Topology")
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(FIELD_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📊 Saved: {POLAR_PATH.name}")
print(f"📊 Saved: {CUBE_PATH.name}")
print(f"📊 Saved: {FIELD_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
