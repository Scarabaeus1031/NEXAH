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

REPORT_PATH = OUTDIR / "v47_master_slave_closure_report.txt"
TS_PATH     = OUTDIR / "v47_master_slave_closure_timeseries.png"
POLAR_PATH  = OUTDIR / "v47_master_slave_closure_polar.png"
CUBE_PATH   = OUTDIR / "v47_master_slave_closure_3d.png"
FIELD_PATH  = OUTDIR / "v47_master_slave_closure_topology.png"

print(f"\n📁 v47 running → {OUTDIR.resolve()}\n")

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

def smooth_step(x, x0, k=20.0):
    return 1.0 / (1.0 + np.exp(-k * (x - x0)))

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
    "u_gap": [],
    "u_closure": [],
    "psi_m": [],
    "psi_s": [],
    "r_m": [],
    "r_s": [],
    "node_m": [],
    "node_s": [],
    "switch_m": [],
    "switch_s": [],
    "gap_event": [],
    "closure_event": [],
    "algo_event": [],
    "olgo_event": [],
    "oko_event": [],
    "mx": [], "my": [],
    "sx": [], "sy": [],
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

# shell / closure gains
k_lock = 0.05
k_gap = 0.045
k_closure = 0.065

# master/slave field
master_drive = 0.055
slave_follow = 0.050
slave_counter = 0.030
res_drive = 0.18

breath_base = 0.55
breath_amp_m = 0.18
breath_amp_s = 0.10
breath_freq = 0.05

# topology
jump_gain = 0.045
u_clip = 0.08
prox_threshold = 0.30

# gap / closure
gap_angle_tol = 0.22
gap_radius_tol = 0.12
closure_tol = 0.10

# ============================================================
# INTERNAL FIELD STATE
# ============================================================
psi_m = theta_ref
psi_s = wrap_angle(theta_ref + np.pi / 3)

node_m = 4
node_s = 1

dir_m = 1
dir_s = -1

prev_theta = None

escape_count = 0
switch_m_count = 0
switch_s_count = 0
gap_count = 0
closure_count = 0
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
    # crossing estimate
    # --------------------------------------------------------
    crossing_event = 0
    if prev_theta is not None:
        prev_err = wrap_angle(prev_theta - theta_ref)
        curr_err = wrap_angle(theta - theta_ref)
        if prev_err * curr_err < 0:
            crossing_event = 1

    # --------------------------------------------------------
    # regime logic
    # --------------------------------------------------------
    algo_event = 0
    olgo_event = 0
    oko_event = 0

    if prox < 0.15:
        mode = "algo"
        algo_event = 1
        algo_count += 1
    elif prox < 0.60:
        mode = "olgo"
        olgo_event = 1
        olgo_count += 1
    else:
        mode = "oko"
        oko_event = 1
        oko_count += 1

    # --------------------------------------------------------
    # master/slave phase dynamics
    # --------------------------------------------------------
    # master aligns with IEEE + resonance
    psi_m_dot = 0.0
    psi_m_dot += master_drive * np.sin(theta - psi_m)
    psi_m_dot += res_drive * prox * np.sin(theta_ref - psi_m)

    # slave partly follows master, partly counter-rotates
    psi_s_dot = 0.0
    psi_s_dot += slave_follow * np.sin(psi_m - psi_s)
    psi_s_dot += slave_counter * np.sin(-(theta - psi_s))

    if mode == "algo":
        psi_m_dot += 0.018 * dir_m
        psi_s_dot += -0.012 * dir_s
    elif mode == "olgo":
        psi_m_dot += -0.010 * dir_m
        psi_s_dot += 0.010 * dir_s
    elif mode == "oko":
        psi_m_dot += 0.008 * np.sin(theta_ref - psi_m)
        psi_s_dot += 0.008 * np.sin(psi_m - psi_s)

    psi_m = wrap_angle(psi_m + psi_m_dot)
    psi_s = wrap_angle(psi_s + psi_s_dot)

    # --------------------------------------------------------
    # radii
    # --------------------------------------------------------
    r_m = breath_base + breath_amp_m * np.sin(breath_freq * t + psi_m)
    r_s = (breath_base - 0.08) + breath_amp_s * np.sin(breath_freq * t - psi_s)

    # --------------------------------------------------------
    # nodes from phase
    # --------------------------------------------------------
    def phase_to_sector(phase):
        a = (phase + 2*np.pi) % (2*np.pi)
        return int(np.floor(a / (2*np.pi / N_SECTORS))) % N_SECTORS

    old_m = node_m
    old_s = node_s

    node_m = phase_to_sector(psi_m)
    node_s = phase_to_sector(psi_s)

    switch_m = 1 if node_m != old_m else 0
    switch_s = 1 if node_s != old_s else 0

    if switch_m:
        switch_m_count += 1
    if switch_s:
        switch_s_count += 1

    # --------------------------------------------------------
    # gap / white gas windows
    # --------------------------------------------------------
    phase_gap = abs(wrap_angle(psi_m - psi_s))
    radius_gap = abs(r_m - r_s)

    gap_event = 1 if (phase_gap < gap_angle_tol and radius_gap < gap_radius_tol) else 0
    if gap_event:
        gap_count += 1

    # --------------------------------------------------------
    # closure / OKO event
    # stronger than prox alone:
    # closure = resonance + gap + relation to theta_ref
    # --------------------------------------------------------
    closure_metric = (
        0.5 * prox
        + 0.25 * np.exp(-8.0 * phase_gap)
        + 0.25 * np.exp(-10.0 * abs(wrap_angle(psi_m - theta_ref)))
    )

    closure_event = 1 if closure_metric > 0.72 else 0
    if closure_event:
        closure_count += 1
        mode = "oko"

    # --------------------------------------------------------
    # topology coordinates
    # --------------------------------------------------------
    mx = r_m * np.cos(sector_angles[node_m])
    my = r_m * np.sin(sector_angles[node_m])

    sx = r_s * np.cos(sector_angles[node_s])
    sy = r_s * np.sin(sector_angles[node_s])

    # --------------------------------------------------------
    # topology jump rules
    # --------------------------------------------------------
    u_jump = 0.0
    if crossing_event:
        dir_m *= -1

    if gap_event:
        dir_s *= -1
        u_jump += jump_gain * 0.5

    if closure_event:
        # pull master/slave into partial synchronization
        psi_s = wrap_angle(0.6 * psi_s + 0.4 * psi_m)
        u_jump += jump_gain

    # --------------------------------------------------------
    # controller composition
    # --------------------------------------------------------
    # IEEE layer
    u_ieee = 0.0
    u_ieee += -k_r * (r - target_radius)
    u_ieee += -k_theta * np.sin(wrap_angle(theta - theta_ref))

    # field guidance = master + slave
    u_field = 0.0
    u_field += 0.022 * np.cos(theta - psi_m)
    u_field += 0.018 * np.cos(theta - psi_s)

    # lock toward different shells by regime
    if mode == "algo":
        shell_target = shells[2]
    elif mode == "olgo":
        shell_target = shells[1]
    else:
        shell_target = shells[0]

    u_lock = -k_lock * (z_olgo - shell_target)

    # gap term
    u_gap = 0.0
    if gap_event:
        u_gap += k_gap * np.cos(theta - psi_m)
        u_gap += k_gap * np.cos(theta - psi_s)

    # closure term
    u_closure = 0.0
    if closure_event:
        u_closure += k_closure * np.cos(theta_ref - theta)
        u_closure += 0.03 * np.cos(psi_m - psi_s)

    u = u_ieee + u_field + u_lock + u_gap + u_closure + u_jump

    if prox > prox_threshold:
        lock_count += 1
        u *= 0.75

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
    controlled["u_gap"].append(u_gap)
    controlled["u_closure"].append(u_closure)
    controlled["psi_m"].append(psi_m)
    controlled["psi_s"].append(psi_s)
    controlled["r_m"].append(r_m)
    controlled["r_s"].append(r_s)
    controlled["node_m"].append(node_m)
    controlled["node_s"].append(node_s)
    controlled["switch_m"].append(switch_m)
    controlled["switch_s"].append(switch_s)
    controlled["gap_event"].append(gap_event)
    controlled["closure_event"].append(closure_event)
    controlled["algo_event"].append(algo_event)
    controlled["olgo_event"].append(olgo_event)
    controlled["oko_event"].append(oko_event)
    controlled["mx"].append(mx)
    controlled["my"].append(my)
    controlled["sx"].append(sx)
    controlled["sy"].append(sy)
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

node_m_counts = {f"node_{i}": int(np.sum(np.array(controlled["node_m"]) == i)) for i in range(N_SECTORS)}
node_s_counts = {f"node_{i}": int(np.sum(np.array(controlled["node_s"]) == i)) for i in range(N_SECTORS)}

report = f"""NEXAH v47 – Master Slave Closure Controller

Escape count: {escape_count}
Master switch count: {switch_m_count}
Slave switch count: {switch_s_count}
Gap count: {gap_count}
Closure count: {closure_count}
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

Master node occupancy:
  node_0: {node_m_counts['node_0']}
  node_1: {node_m_counts['node_1']}
  node_2: {node_m_counts['node_2']}
  node_3: {node_m_counts['node_3']}
  node_4: {node_m_counts['node_4']}
  node_5: {node_m_counts['node_5']}

Slave node occupancy:
  node_0: {node_s_counts['node_0']}
  node_1: {node_s_counts['node_1']}
  node_2: {node_s_counts['node_2']}
  node_3: {node_s_counts['node_3']}
  node_4: {node_s_counts['node_4']}
  node_5: {node_s_counts['node_5']}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print(report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(10, 1, figsize=(14, 24), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v47 Master Slave Closure Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple", label="IEEE radius")
axs[2].plot(controlled["r_m"], color="hotpink", alpha=0.8, label="master radius")
axs[2].plot(controlled["r_s"], color="cyan", alpha=0.8, label="slave radius")
axs[2].axhline(target_radius, color="green", linestyle="--", alpha=0.7)
axs[2].legend()
axs[2].set_ylabel("Radius")

axs[3].plot(controlled["theta"], color="teal", label="theta")
axs[3].plot(controlled["psi_m"], color="magenta", alpha=0.8, label="psi master")
axs[3].plot(controlled["psi_s"], color="cyan", alpha=0.8, label="psi slave")
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
axs[5].plot(controlled["u_gap"], color="hotpink", alpha=0.8, label="gap")
axs[5].plot(controlled["u_closure"], color="green", alpha=0.8, label="closure")
axs[5].legend(ncol=6)
axs[5].set_ylabel("Control")

axs[6].plot(controlled["node_m"], color="magenta", label="master node")
axs[6].plot(controlled["node_s"], color="cyan", alpha=0.8, label="slave node")
axs[6].legend()
axs[6].set_ylabel("Nodes")

axs[7].plot(controlled["switch_m"], color="magenta", label="m switch")
axs[7].plot(controlled["switch_s"], color="cyan", label="s switch")
axs[7].plot(controlled["gap_event"], color="hotpink", label="gap")
axs[7].plot(controlled["closure_event"], color="green", label="closure")
axs[7].legend()
axs[7].set_ylabel("Events")

axs[8].plot(controlled["algo_event"], color="gold", label="ALGO")
axs[8].plot(controlled["olgo_event"], color="magenta", label="OLGO")
axs[8].plot(controlled["oko_event"], color="green", label="OKO")
axs[8].legend()
axs[8].set_ylabel("Modes")

axs[9].plot(controlled["olgo_prox"], color="darkviolet")
axs[9].axhline(prox_threshold, color="gray", linestyle="--", alpha=0.6)
axs[9].set_ylabel("prox")
axs[9].set_xlabel("Time step")

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
psi_m_vals = np.array(controlled["psi_m"])
psi_s_vals = np.array(controlled["psi_s"])
rm_vals = np.array(controlled["r_m"])
rs_vals = np.array(controlled["r_s"])
prox_vals = np.array(controlled["olgo_prox"])

gap_idx = np.where(np.array(controlled["gap_event"]) > 0)[0]
closure_idx = np.where(np.array(controlled["closure_event"]) > 0)[0]

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="IEEE")
ax.plot(psi_m_vals, rm_vals, color="magenta", alpha=0.75, label="Master")
ax.plot(psi_s_vals, rs_vals, color="cyan", alpha=0.75, label="Slave")

sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

if len(gap_idx) > 0:
    ax.scatter(psi_m_vals[gap_idx], rm_vals[gap_idx], color="hotpink", s=20, label="gaps")
if len(closure_idx) > 0:
    ax.scatter(psi_m_vals[closure_idx], rm_vals[closure_idx], color="green", s=26, label="closure")

ax.set_title("v47 Master Slave Closure Polar")
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
ax.plot(controlled["mx"], controlled["my"], controlled["r_m"], color="magenta", linewidth=1.6, alpha=0.8)
ax.plot(controlled["sx"], controlled["sy"], controlled["r_s"], color="cyan", linewidth=1.4, alpha=0.8)

ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("OLGO Z / Field R")
ax.set_title("v47 Master Slave Closure 3D")
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

ax.plot(controlled["mx"], controlled["my"], color="magenta", linewidth=1.5, alpha=0.85, label="master")
ax.plot(controlled["sx"], controlled["sy"], color="cyan", linewidth=1.5, alpha=0.85, label="slave")

ax.set_title("v47 Master Slave Closure Field")
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
