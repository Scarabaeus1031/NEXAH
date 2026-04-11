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

REPORT_PATH = OUTDIR / "v46_topological_navigation_report.txt"
TS_PATH     = OUTDIR / "v46_topological_navigation_timeseries.png"
POLAR_PATH  = OUTDIR / "v46_topological_navigation_polar.png"
CUBE_PATH   = OUTDIR / "v46_topological_navigation_3d.png"
FIELD_PATH  = OUTDIR / "v46_topological_navigation_topology.png"

print(f"\n📁 v46 running → {OUTDIR.resolve()}\n")

# ============================================================
# OLGO / SHELL LAYER
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

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

# ============================================================
# HEX FIELD
# ============================================================
N_SECTORS = 6
sector_angles = np.linspace(0, 2*np.pi, N_SECTORS, endpoint=False)
hex_nodes = np.array([(np.cos(a), np.sin(a)) for a in sector_angles])

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
    "u_jump": [],
    "psi": [],
    "field_radius": [],
    "field_node": [],
    "field_switch": [],
    "loop_event": [],
    "algo_event": [],
    "olgo_event": [],
    "oko_event": [],
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

# IEEE gains
k_r = 0.07
k_theta = 0.035
k_lock = 0.03

# field gains
psi_align_gain = 0.06
psi_res_gain = 0.16
field_breath_base = 0.55
field_breath_amp = 0.18
field_breath_freq = 0.045

# topology gains
jump_gain = 0.055
field_align_gain = 0.035
reentry_gain = 0.05

prox_threshold = 0.30
u_clip = 0.08

# ============================================================
# INTERNAL STATE
# ============================================================
psi = theta_ref
field_node = 4
direction = 1
mode = "algo"

prev_theta = None

escape_count = 0
field_switch_count = 0
loop_count = 0
lock_count = 0
algo_count = 0
olgo_count = 0
oko_count = 0

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
    # IEEE state
    # --------------------------------------------------------
    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = wrap_angle(np.arctan2(sw - 0.000076, coh - 0.942913))

    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo)
    _, shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # crossings / events
    # --------------------------------------------------------
    crossing_event = 0
    if prev_theta is not None:
        prev_err = wrap_angle(prev_theta - theta_ref)
        curr_err = wrap_angle(theta - theta_ref)
        if prev_err * curr_err < 0:
            crossing_event = 1

    # --------------------------------------------------------
    # mode logic: ALGO / OLGO / OKO
    # --------------------------------------------------------
    algo_event = 0
    olgo_event = 0
    oko_event = 0

    if prox < 0.15:
        mode = "algo"
        algo_event = 1
        algo_count += 1
    elif prox < 0.55:
        mode = "olgo"
        olgo_event = 1
        olgo_count += 1
    else:
        mode = "oko"
        oko_event = 1
        oko_count += 1

    # --------------------------------------------------------
    # dynamic field phase
    # --------------------------------------------------------
    psi_dot = 0.0
    psi_dot += psi_align_gain * np.sin(theta - psi)
    psi_dot += psi_res_gain * prox * np.sin(theta_ref - psi)

    # ALGO: forward drift
    if mode == "algo":
        psi_dot += 0.020 * direction

    # OLGO: mirrored drift
    elif mode == "olgo":
        psi_dot += -0.015 * direction

    # OKO: closure / stabilize
    elif mode == "oko":
        psi_dot += 0.010 * np.sin(theta_ref - psi)

    psi = wrap_angle(psi + psi_dot)

    # --------------------------------------------------------
    # breathing field radius
    # --------------------------------------------------------
    field_radius = field_breath_base + field_breath_amp * np.sin(field_breath_freq * t + psi)

    # --------------------------------------------------------
    # loop detection
    # --------------------------------------------------------
    loop_event = 0
    if field_radius < 0.40 and prox > 0.05:
        loop_event = 1
        loop_count += 1

    # --------------------------------------------------------
    # TOPOLOGICAL JUMP
    # this is the missing piece from v45
    # --------------------------------------------------------
    field_switch = 0
    u_jump = 0.0

    if crossing_event or loop_event or mode == "oko":
        old_node = field_node

        if mode == "algo":
            field_node = (field_node + direction) % N_SECTORS
        elif mode == "olgo":
            direction *= -1
            field_node = (field_node + direction) % N_SECTORS
        elif mode == "oko":
            field_node = (field_node + 2 * direction) % N_SECTORS

        if field_node != old_node:
            field_switch = 1
            field_switch_count += 1
            psi = wrap_angle(sector_angles[field_node])
            u_jump = jump_gain * direction

    # --------------------------------------------------------
    # topology coords
    # --------------------------------------------------------
    sector_angle = sector_angles[field_node]
    fx = field_radius * np.cos(sector_angle)
    fy = field_radius * np.sin(sector_angle)

    # --------------------------------------------------------
    # controller composition
    # --------------------------------------------------------
    u_ieee = 0.0
    u_ieee += -k_r * (r - target_radius)
    u_ieee += -k_theta * np.sin(wrap_angle(theta - theta_ref))

    shell_target = shells[1] if mode == "olgo" else shells[0] if mode == "oko" else shells[2]
    u_lock = -k_lock * (z_olgo - shell_target)

    u_field = 0.0
    u_field += field_align_gain * np.cos(theta - sector_angle)
    u_field += 0.025 * np.cos(theta - psi)

    u_reentry = 0.0
    if loop_event:
        u_reentry += reentry_gain * np.cos(theta - sector_angle)
        u_reentry += 0.035 * np.cos(theta_ref - theta)

    u = u_ieee + u_lock + u_field + u_reentry + u_jump

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
    controlled["u_jump"].append(u_jump)
    controlled["psi"].append(psi)
    controlled["field_radius"].append(field_radius)
    controlled["field_node"].append(field_node)
    controlled["field_switch"].append(field_switch)
    controlled["loop_event"].append(loop_event)
    controlled["algo_event"].append(algo_event)
    controlled["olgo_event"].append(olgo_event)
    controlled["oko_event"].append(oko_event)
    controlled["field_x"].append(fx)
    controlled["field_y"].append(fy)
    controlled["mode"].append(mode)

    if r > 0.055:
        escape_count += 1

    prev_theta = theta

# ============================================================
# REPORT
# ============================================================
shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["shell_index"]) == i))
    for i in range(len(shells))
}

field_node_counts = {
    f"node_{i}": int(np.sum(np.array(controlled["field_node"]) == i))
    for i in range(N_SECTORS)
}

report = f"""NEXAH v46 – Topological Navigation Controller

Escape count: {escape_count}
Field switch count: {field_switch_count}
Loop count: {loop_count}
Lock count (prox > {prox_threshold}): {lock_count}

ALGO count: {algo_count}
OLGO count: {olgo_count}
OKO count: {oko_count}

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
fig, axs = plt.subplots(9, 1, figsize=(14, 22), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v46 Topological Navigation Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple", label="IEEE radius")
axs[2].plot(controlled["field_radius"], color="hotpink", alpha=0.8, label="field radius")
axs[2].axhline(target_radius, color="green", linestyle="--", alpha=0.7)
axs[2].legend()
axs[2].set_ylabel("Radius")

axs[3].plot(controlled["theta"], color="teal", label="theta")
axs[3].plot(controlled["psi"], color="darkviolet", alpha=0.8, label="psi")
axs[3].axhline(theta_ref, color="gold", linestyle="--", alpha=0.7, label="theta_ref")
axs[3].legend()
axs[3].set_ylabel("Phase")

axs[4].plot(controlled["z_olgo"], color="slateblue")
for s in shells:
    axs[4].axhline(s, color="gray", linestyle="--", alpha=0.5)
axs[4].set_ylabel("OLGO Z")

axs[5].plot(controlled["u"], color="black", label="u")
axs[5].plot(controlled["u_ieee"], color="gray", alpha=0.8, label="ieee")
axs[5].plot(controlled["u_field"], color="gold", alpha=0.8, label="field")
axs[5].plot(controlled["u_lock"], color="red", alpha=0.8, label="lock")
axs[5].plot(controlled["u_reentry"], color="cyan", alpha=0.8, label="reentry")
axs[5].plot(controlled["u_jump"], color="hotpink", alpha=0.8, label="jump")
axs[5].legend(ncol=6)
axs[5].set_ylabel("Control")

axs[6].plot(controlled["field_node"], color="darkviolet")
axs[6].set_ylabel("Field node")

axs[7].plot(controlled["field_switch"], color="purple", label="field switch")
axs[7].plot(controlled["loop_event"], color="hotpink", label="loop")
axs[7].legend()
axs[7].set_ylabel("Events")

axs[8].plot(controlled["algo_event"], color="gold", label="ALGO")
axs[8].plot(controlled["olgo_event"], color="magenta", label="OLGO")
axs[8].plot(controlled["oko_event"], color="green", label="OKO")
axs[8].legend()
axs[8].set_ylabel("Modes")
axs[8].set_xlabel("Time step")

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
psi_vals = np.array(controlled["psi"])
fr_vals = np.array(controlled["field_radius"])
prox_vals = np.array(controlled["olgo_prox"])
loop_vals = np.array(controlled["loop_event"])
switch_vals = np.array(controlled["field_switch"])

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="IEEE")
ax.plot(psi_vals, fr_vals, color="hotpink", alpha=0.75, label="Field")
sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

loop_idx = np.where(loop_vals > 0)[0]
switch_idx = np.where(switch_vals > 0)[0]

if len(loop_idx) > 0:
    ax.scatter(psi_vals[loop_idx], fr_vals[loop_idx], color="hotpink", s=18, label="loops")
if len(switch_idx) > 0:
    ax.scatter(psi_vals[switch_idx], fr_vals[switch_idx], color="purple", s=28, label="switches")

ax.set_title("v46 Topological Navigation Polar")
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

sc = ax.scatter(x, y, z, c=c, cmap="plasma", s=14)
ax.plot(controlled["field_x"], controlled["field_y"], controlled["field_radius"],
        color="hotpink", linewidth=1.6, alpha=0.8)

ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("OLGO Z / Field R")
ax.set_title("v46 Topological Navigation 3D")
fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# FIELD TOPOLOGY
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

for i in range(N_SECTORS):
    x1, y1 = hex_nodes[i]
    x2, y2 = hex_nodes[(i + 1) % N_SECTORS]
    ax.plot([x1, x2], [y1, y2], color="gray", alpha=0.8)

for i in range(N_SECTORS):
    x1, y1 = hex_nodes[i]
    ax.plot([0, x1], [0, y1], color="lightgray", alpha=0.6)

ax.scatter(hex_nodes[:, 0], hex_nodes[:, 1], s=180, c="skyblue")
ax.scatter([0], [0], s=220, c="hotpink")

for i, (xn, yn) in enumerate(hex_nodes):
    ax.text(xn * 1.08, yn * 1.08, f"{i}", ha="center", va="center", fontsize=12)
ax.text(0, 0, "loop", ha="center", va="center", fontsize=12, color="white")

ax.plot(controlled["field_x"], controlled["field_y"], color="hotpink", linewidth=1.5, alpha=0.85)

node_occ = np.array([field_node_counts[f"node_{i}"] for i in range(N_SECTORS)], dtype=float)
if node_occ.max() > 0:
    node_occ = node_occ / node_occ.max()
    for i, (xn, yn) in enumerate(hex_nodes):
        ax.scatter([xn], [yn], s=400 * node_occ[i] + 40, alpha=0.25, c="navy")

ax.set_title("v46 Topological Navigation Field")
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
