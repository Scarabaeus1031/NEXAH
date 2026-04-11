import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp

# ============================================================
# PATHS
# ============================================================
OUTDIR = Path("/Users/tho2020/Documents/GitHub/NEXAH/APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = OUTDIR / "v49_controlled_closure_engine_report.txt"
TS_PATH     = OUTDIR / "v49_controlled_closure_engine_timeseries.png"
POLAR_PATH  = OUTDIR / "v49_controlled_closure_engine_polar.png"

print(f"\n📁 v49 running → {OUTDIR.resolve()}\n")

# ============================================================
# HELPERS
# ============================================================
N_SECTORS = 6
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

def phase_to_sector(phase, n=6):
    a = (phase + 2*np.pi) % (2*np.pi)
    return int(np.floor(a / (2*np.pi / n))) % n

def safe_mean(x):
    return float(np.mean(x)) if len(x) else 0.0

def safe_max(x):
    return float(np.max(x)) if len(x) else 0.0

# ============================================================
# GRID SETUP
# ============================================================
np.random.seed(42)
net = pp.networks.case57()

net.load.p_mw *= 0.95
net.load.q_mvar *= 0.95

base_p = net.load.p_mw.copy()
base_q = net.load.q_mvar.copy()

# ============================================================
# STORAGE
# ============================================================
controlled = {k: [] for k in [
    "voltage","coherence","radius","theta","z_olgo","olgo_prox","shell_index",
    "u","u_ieee","u_field","u_lock","u_gap","u_closure","u_couple",
    "psi_m","psi_s","r_m","r_s",
    "node_m","node_s","switch_m","switch_s",
    "gap_event","closure_event",
    "algo_event","olgo_event","oko_event",
    "closure_metric","closure_bias","mode"
]}

# ============================================================
# SETTINGS
# ============================================================
T = 400
theta_ref = -np.pi / 2
target_radius = 0.26

# IEEE
k_r = 0.12
k_theta = 0.05

# field
master_drive = 0.16
slave_follow = 0.14
slave_counter = 0.04
res_drive = 0.26

# breathing
breath_base = 0.48
breath_amp_m = 0.14
breath_amp_s = 0.08
breath_freq = 0.06

# control
k_lock = 0.12
k_gap = 0.06
k_closure = 0.10
k_couple = 0.12

# thresholds
prox_threshold = 0.22
gap_angle_tol = 0.32
gap_radius_tol = 0.14
closure_metric_threshold = 0.52
closure_bias_on = 0.58
closure_bias_off = 0.42

u_clip = 0.10
load_scale_gain = 0.06

# latch
oko_hold_steps = 18

# ============================================================
# INTERNAL STATE
# ============================================================
psi_m = theta_ref
psi_s = wrap_angle(theta_ref + np.pi/3)

dir_m = 1
dir_s = -1

closure_bias = 0.0
oko_hold = 0

prev_theta = None
prev_node_m = phase_to_sector(psi_m)
prev_node_s = phase_to_sector(psi_s)

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
    print(f"step {t}")

    try:
        pp.runpp(net, enforce_q_lims=True, max_iteration=20)
    except:
        print(f"⚠️ PF failed at step {t}, damping...")
        net.load.p_mw = base_p * 0.99
        net.load.q_mvar = base_q * 0.99
        continue

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

    crossing_event = 0
    if prev_theta is not None:
        prev_err = wrap_angle(prev_theta - theta_ref)
        curr_err = wrap_angle(theta - theta_ref)
        if prev_err * curr_err < 0:
            crossing_event = 1

    # --------------------------------------------------------
    # FIELD PHASES
    # --------------------------------------------------------
    psi_m_dot = master_drive * np.sin(theta - psi_m) + res_drive * prox * np.sin(theta_ref - psi_m)
    psi_s_dot = slave_follow * np.sin(psi_m - psi_s) + slave_counter * np.sin(-(theta - psi_s))

    # light directionality
    psi_m_dot += 0.012 * dir_m
    psi_s_dot += -0.008 * dir_s

    psi_m = wrap_angle(psi_m + psi_m_dot)
    psi_s = wrap_angle(psi_s + psi_s_dot)

    r_m = breath_base + breath_amp_m * np.sin(breath_freq * t + psi_m)
    r_s = (breath_base - 0.06) + breath_amp_s * np.sin(breath_freq * t - psi_s)

    node_m = phase_to_sector(psi_m)
    node_s = phase_to_sector(psi_s)

    switch_m = int(node_m != prev_node_m)
    switch_s = int(node_s != prev_node_s)

    if switch_m:
        switch_m_count += 1
    if switch_s:
        switch_s_count += 1

    # --------------------------------------------------------
    # GAP / ÖSE
    # --------------------------------------------------------
    phase_gap = abs(wrap_angle(psi_m - psi_s))
    radius_gap = abs(r_m - r_s)

    gap_event = int(phase_gap < gap_angle_tol and radius_gap < gap_radius_tol)
    if gap_event:
        gap_count += 1

    # --------------------------------------------------------
    # CLOSURE METRIC
    # --------------------------------------------------------
    closure_metric = (
        0.32 * prox
        + 0.24 * np.exp(-5.0 * phase_gap)
        + 0.20 * np.exp(-6.0 * abs(r - target_radius))
        + 0.14 * np.exp(-6.0 * abs(wrap_angle(theta - psi_m)))
        + 0.10 * gap_event
    )

    # bias integrates memory of near-closure
    closure_bias = 0.94 * closure_bias + 0.18 * closure_metric

    closure_event = 0
    if closure_bias > closure_bias_on or closure_metric > closure_metric_threshold:
        oko_hold = oko_hold_steps

    if oko_hold > 0:
        closure_event = 1
        oko_hold -= 1
        closure_count += 1

    # --------------------------------------------------------
    # MODE
    # --------------------------------------------------------
    algo_event = 0
    olgo_event = 0
    oko_event = 0

    if closure_event:
        mode = "oko"
        oko_event = 1
        oko_count += 1
    elif prox >= 0.18:
        mode = "olgo"
        olgo_event = 1
        olgo_count += 1
    else:
        mode = "algo"
        algo_event = 1
        algo_count += 1

    # --------------------------------------------------------
    # REGIME EFFECTS
    # --------------------------------------------------------
    if mode == "algo":
        dir_m = 1
    elif mode == "olgo":
        if crossing_event:
            dir_m *= -1
        if gap_event:
            dir_s *= -1
    elif mode == "oko":
        # force convergence
        psi_s = wrap_angle(0.65 * psi_s + 0.35 * psi_m)
        r_s = 0.75 * r_s + 0.25 * r_m

    # --------------------------------------------------------
    # CONTROL TERMS
    # --------------------------------------------------------
    u_ieee = -k_r * (r - target_radius) - k_theta * np.sin(wrap_angle(theta - theta_ref))

    u_field = (
        0.034 * np.cos(theta - psi_m)
        + 0.026 * np.cos(theta - psi_s)
    )

    if mode == "algo":
        shell_target = shells[2]
    elif mode == "olgo":
        shell_target = shells[1]
    else:
        shell_target = shells[0]

    u_lock = -k_lock * (z_olgo - shell_target)

    u_gap = 0.0
    if gap_event:
        u_gap += k_gap * np.cos(theta - psi_m)
        u_gap += k_gap * np.cos(theta - psi_s)

    u_closure = 0.0
    if closure_event:
        u_closure += k_closure * np.cos(theta_ref - theta)
        u_closure += 0.05 * np.cos(psi_m - psi_s)
        u_closure += 0.04 * prox

    u_couple = (
        k_couple * np.cos(theta - psi_m)
        + 0.08 * np.exp(-3.5 * abs(r - r_m))
    )

    u = u_ieee + u_field + u_lock + u_gap + u_closure + u_couple

    # warmup
    if t < 10:
        u = 0.0

    if prox > prox_threshold:
        lock_count += 1
        u *= 0.82

    u = np.clip(u, -u_clip, u_clip)

    # --------------------------------------------------------
    # APPLY SAFELY
    # --------------------------------------------------------
    factor = 1.0 + load_scale_gain * u
    factor = np.clip(factor, 0.94, 1.06)

    net.load.p_mw = base_p * factor
    net.load.q_mvar = base_q * factor

    # --------------------------------------------------------
    # STORE
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

    controlled["closure_metric"].append(closure_metric)
    controlled["closure_bias"].append(closure_bias)
    controlled["mode"].append(mode)

    if r > 0.055:
        escape_count += 1

    prev_theta = theta
    prev_node_m = node_m
    prev_node_s = node_s

# ============================================================
# REPORT
# ============================================================
shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["shell_index"]) == i))
    for i in range(len(shells))
}

node_m_counts = {f"node_{i}": int(np.sum(np.array(controlled["node_m"]) == i)) for i in range(N_SECTORS)}
node_s_counts = {f"node_{i}": int(np.sum(np.array(controlled["node_s"]) == i)) for i in range(N_SECTORS)}

report = f"""NEXAH v49 – Controlled Closure Engine

Escape count: {escape_count}
Master switch count: {switch_m_count}
Slave switch count: {switch_s_count}
Gap count: {gap_count}
Closure count: {closure_count}
Lock count (prox > {prox_threshold}): {lock_count}

ALGO count: {algo_count}
OLGO count: {olgo_count}
OKO count: {oko_count}

Mean voltage: {safe_mean(controlled['voltage']):.4f}
Mean coherence: {safe_mean(controlled['coherence']):.4f}
Mean radius: {safe_mean(controlled['radius']):.4f}

Mean OLGO proximity: {safe_mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {safe_max(controlled['olgo_prox']):.4f}
Mean control signal: {safe_mean(controlled['u']):.4f}

Mean closure metric: {safe_mean(controlled['closure_metric']):.4f}
Max closure metric: {safe_max(controlled['closure_metric']):.4f}
Mean closure bias: {safe_mean(controlled['closure_bias']):.4f}
Max closure bias: {safe_max(controlled['closure_bias']):.4f}

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
fig, axs = plt.subplots(5, 1, figsize=(12, 16), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v49 Controlled Closure Engine")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple", label="IEEE r")
axs[2].plot(controlled["r_m"], color="magenta", alpha=0.8, label="master r")
axs[2].plot(controlled["r_s"], color="cyan", alpha=0.8, label="slave r")
axs[2].axhline(target_radius, color="green", linestyle="--", alpha=0.7)
axs[2].legend()
axs[2].set_ylabel("Radius")

axs[3].plot(controlled["closure_metric"], color="darkviolet", label="closure metric")
axs[3].plot(controlled["closure_bias"], color="black", alpha=0.8, label="closure bias")
axs[3].axhline(closure_metric_threshold, color="gray", linestyle="--", alpha=0.6)
axs[3].axhline(closure_bias_on, color="red", linestyle="--", alpha=0.6)
axs[3].legend()
axs[3].set_ylabel("Closure")

axs[4].plot(controlled["algo_event"], color="gold", label="ALGO")
axs[4].plot(controlled["olgo_event"], color="magenta", label="OLGO")
axs[4].plot(controlled["oko_event"], color="green", label="OKO")
axs[4].plot(controlled["closure_event"], color="black", alpha=0.6, label="closure on")
axs[4].legend()
axs[4].set_ylabel("Modes")
axs[4].set_xlabel("Time step")

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

closure_idx = np.where(np.array(controlled["closure_event"]) > 0)[0]

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="IEEE")
ax.plot(psi_m_vals, rm_vals, color="magenta", alpha=0.75, label="Master")
ax.plot(psi_s_vals, rs_vals, color="cyan", alpha=0.75, label="Slave")

sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

if len(closure_idx) > 0:
    ax.scatter(psi_m_vals[closure_idx], rm_vals[closure_idx], color="green", s=26, label="closure")

ax.set_title("v49 Controlled Closure Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📊 Saved: {POLAR_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
