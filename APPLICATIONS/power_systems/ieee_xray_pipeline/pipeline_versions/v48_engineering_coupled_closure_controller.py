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

REPORT_PATH = OUTDIR / "v48_engineering_coupled_closure_report.txt"
TS_PATH     = OUTDIR / "v48_engineering_coupled_closure_timeseries.png"
POLAR_PATH  = OUTDIR / "v48_engineering_coupled_closure_polar.png"
CUBE_PATH   = OUTDIR / "v48_engineering_coupled_closure_3d.png"
FIELD_PATH  = OUTDIR / "v48_engineering_coupled_closure_topology.png"

print(f"\n📁 v48 running → {OUTDIR.resolve()}\n")

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
# FIELD TOPOLOGY
# ============================================================
N_SECTORS = 6
sector_angles = np.linspace(0, 2*np.pi, N_SECTORS, endpoint=False)
hex_nodes = np.array([(np.cos(a), np.sin(a)) for a in sector_angles])

def phase_to_sector(phase):
    a = (phase + 2*np.pi) % (2*np.pi)
    return int(np.floor(a / (2*np.pi / N_SECTORS))) % N_SECTORS

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
    "u_couple": [],
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
    "closure_metric": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2

# practical engineering target: closer than before, but not unrealistically tiny
target_radius = 0.22

# IEEE gains
k_r = 0.16
k_theta = 0.050

# shell / lock gains
k_lock = 0.11
k_gap = 0.06
k_closure = 0.08
k_couple = 0.10

# field dynamics
master_drive = 0.15
slave_follow = 0.12
slave_counter = 0.05
res_drive = 0.24

breath_base = 0.52
breath_amp_m = 0.16
breath_amp_s = 0.10
breath_freq = 0.055

# thresholds
prox_threshold = 0.20
gap_angle_tol = 0.28
gap_radius_tol = 0.14
closure_tol = 0.58

u_clip = 0.10

# ============================================================
# INTERNAL FIELD STATE
# ============================================================
psi_m = theta_ref
psi_s = wrap_angle(theta_ref + np.pi / 3)

node_m = 4
node_s = 5

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

    # crossing estimate
    crossing_event = 0
    if prev_theta is not None:
        prev_err = wrap_angle(prev_theta - theta_ref)
        curr_err = wrap_angle(theta - theta_ref)
        if prev_err * curr_err < 0:
            crossing_event = 1

    # --------------------------------------------------------
    # mode logic
    # --------------------------------------------------------
    algo_event = 0
    olgo_event = 0
    oko_event = 0

    if prox < 0.18:
        mode = "algo"
        algo_event = 1
        algo_count += 1
    elif prox < 0.50:
        mode = "olgo"
        olgo_event = 1
        olgo_count += 1
    else:
        mode = "oko"
        oko_event = 1
        oko_count += 1

    # --------------------------------------------------------
    # master / slave phase dynamics
    # stronger coupling to IEEE
    # --------------------------------------------------------
    psi_m_dot = 0.0
    psi_m_dot += master_drive * np.sin(theta - psi_m)
    psi_m_dot += res_drive * prox * np.sin(theta_ref - psi_m)

    psi_s_dot = 0.0
    psi_s_dot += slave_follow * np.sin(psi_m - psi_s)
    psi_s_dot += slave_counter * np.sin(-(theta - psi_s))

    if mode == "algo":
        psi_m_dot += 0.020 * dir_m
        psi_s_dot += -0.010 * dir_s
    elif mode == "olgo":
        psi_m_dot += -0.015 * dir_m
        psi_s_dot += 0.012 * dir_s
    elif mode == "oko":
        psi_m_dot += 0.012 * np.sin(theta_ref - psi_m)
        psi_s_dot += 0.010 * np.sin(psi_m - psi_s)

    psi_m = wrap_angle(psi_m + psi_m_dot)
    psi_s = wrap_angle(psi_s + psi_s_dot)

    # --------------------------------------------------------
    # radii for master/slave
    # --------------------------------------------------------
    r_m = breath_base + breath_amp_m * np.sin(breath_freq * t + psi_m)
    r_s = (breath_base - 0.08) + breath_amp_s * np.sin(breath_freq * t - psi_s)

    # --------------------------------------------------------
    # nodes
    # --------------------------------------------------------
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
    # gap windows
    # --------------------------------------------------------
    phase_gap = abs(wrap_angle(psi_m - psi_s))
    radius_gap = abs(r_m - r_s)
    gap_event = 1 if (phase_gap < gap_angle_tol and radius_gap < gap_radius_tol) else 0
    if gap_event:
        gap_count += 1

    # --------------------------------------------------------
    # closure metric
    # more engineering-friendly, less strict
    # --------------------------------------------------------
    closure_metric = (
        0.35 * prox
        + 0.25 * np.exp(-6.0 * phase_gap)
        + 0.20 * np.exp(-8.0 * abs(r - target_radius))
        + 0.20 * np.exp(-8.0 * abs(wrap_angle(theta - psi_m)))
    )
    closure_event = 1 if closure_metric > closure_tol else 0
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
    # switching / knot logic
    # --------------------------------------------------------
    if crossing_event:
        dir_m *= -1

    if gap_event:
        dir_s *= -1

    if closure_event:
        # pull slave toward master
        psi_s = wrap_angle(0.5 * psi_s + 0.5 * psi_m)

    # --------------------------------------------------------
    # controller terms
    # --------------------------------------------------------
    # 1. IEEE contraction into practical band
    u_ieee = 0.0
    u_ieee += -k_r * (r - target_radius)
    u_ieee += -k_theta * np.sin(wrap_angle(theta - theta_ref))

    # 2. field guidance from both tracks
    u_field = 0.0
    u_field += 0.030 * np.cos(theta - psi_m)
    u_field += 0.022 * np.cos(theta - psi_s)

    # 3. shell pull depends on mode
    if mode == "algo":
        shell_target = shells[2]
    elif mode == "olgo":
        shell_target = shells[1]
    else:
        shell_target = shells[0]

    u_lock = -k_lock * (z_olgo - shell_target)

    # 4. gap force
    u_gap = 0.0
    if gap_event:
        u_gap += k_gap * np.cos(theta - psi_m)
        u_gap += k_gap * np.cos(theta - psi_s)

    # 5. closure force
    u_closure = 0.0
    if closure_event:
        u_closure += k_closure * np.cos(theta_ref - theta)
        u_closure += 0.04 * np.cos(psi_m - psi_s)

    # 6. explicit coupling of IEEE to master/slave field
    u_couple = 0.0
    u_couple += k_couple * np.cos(theta - psi_m)
    u_couple += 0.06 * np.exp(-4.0 * abs(r - r_m))

    u = u_ieee + u_field + u_lock + u_gap + u_closure + u_couple

    if prox > prox_threshold:
        lock_count += 1
        u *= 0.78

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
    controlled["u"].append(u)
    controlled["u_ieee"].append(u_ieee)
    controlled["u_field"].append(u_field)
    controlled["u_lock"].append(u_lock)
    controlled["u_gap"].append(u_gap)
    controlled["u_closure"].append(u_closure)
    controlled["u_couple"].append(u_couple)

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
    controlled["closure_metric"].append(closure_metric)

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

report = f"""NEXAH v48 – Engineering Coupled Closure Controller

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
Mean closure metric: {np.mean(controlled['closure_metric']):.4f}

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
axs[0].set_title("v48 Engineering Coupled Closure Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple", label="IEEE radius")
axs[2].plot(controlled["r_m"], color="magenta", alpha=0.8, label="master radius")
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
axs[5].plot(controlled["u_couple"], color="blue", alpha=0.8, label="couple")
axs[5].legend(ncol=7)
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

axs[9].plot(controlled["closure_metric"], color="darkviolet")
axs[9].axhline(closure_tol, color="gray", linestyle="--", alpha=0.6)
axs[9].set_ylabel("Closure")
axs[9].set_xlabel("Time step")

fig.tight_layout()
fig.savefig(TS_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
