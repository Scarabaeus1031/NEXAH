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

REPORT_PATH = OUTDIR / "v48_engineering_coupled_closure_report.txt"
TS_PATH     = OUTDIR / "v48_engineering_coupled_closure_timeseries.png"

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

def phase_to_sector(phase):
    a = (phase + 2*np.pi) % (2*np.pi)
    return int(np.floor(a / (2*np.pi / N_SECTORS))) % N_SECTORS

# ============================================================
# GRID SETUP
# ============================================================
np.random.seed(42)
net = pp.networks.case57()

# ⚠️ weniger aggressiv starten
net.load.p_mw *= 0.95
net.load.q_mvar *= 0.95

# ✅ BASELINE (WICHTIG!)
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
    "mode","closure_metric"
]}

# ============================================================
# SETTINGS
# ============================================================
T = 400
theta_ref = -np.pi / 2
target_radius = 0.22

k_r = 0.16
k_theta = 0.050
k_lock = 0.11
k_gap = 0.06
k_closure = 0.08
k_couple = 0.10

master_drive = 0.15
slave_follow = 0.12
slave_counter = 0.05
res_drive = 0.24

breath_base = 0.52
breath_amp_m = 0.16
breath_amp_s = 0.10
breath_freq = 0.055

prox_threshold = 0.20
gap_angle_tol = 0.28
gap_radius_tol = 0.14
closure_tol = 0.58

u_clip = 0.10

# ============================================================
# INTERNAL STATE
# ============================================================
psi_m = theta_ref
psi_s = wrap_angle(theta_ref + np.pi / 3)

node_m = 4
node_s = 5

prev_theta = None

# ============================================================
# MAIN LOOP
# ============================================================
for t in range(T):

    print(f"step {t}")

    try:
        pp.runpp(net, enforce_q_lims=True, max_iteration=20)
    except:
        print(f"⚠️ PF failed at step {t}, damping...")
        net.load.p_mw = base_p * 0.98
        net.load.q_mvar = base_q * 0.98
        continue

    vm = net.res_bus.vm_pu.values
    v_mean = np.mean(vm)

    coh = 1.0 - np.std(vm)
    sw = (v_mean - 1.0) * 10.0

    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = wrap_angle(np.arctan2(sw - 0.000076, coh - 0.942913))

    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo)
    _, shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # MODE
    # --------------------------------------------------------
    if prox < 0.18:
        mode = "algo"
    elif prox < 0.50:
        mode = "olgo"
    else:
        mode = "oko"

    # --------------------------------------------------------
    # FIELD DYNAMICS
    # --------------------------------------------------------
    psi_m += master_drive * np.sin(theta - psi_m)
    psi_s += slave_follow * np.sin(psi_m - psi_s)

    psi_m = wrap_angle(psi_m)
    psi_s = wrap_angle(psi_s)

    r_m = breath_base + breath_amp_m * np.sin(breath_freq * t + psi_m)
    r_s = (breath_base - 0.08) + breath_amp_s * np.sin(breath_freq * t - psi_s)

    node_m = phase_to_sector(psi_m)
    node_s = phase_to_sector(psi_s)

    phase_gap = abs(wrap_angle(psi_m - psi_s))
    radius_gap = abs(r_m - r_s)

    gap_event = int(phase_gap < gap_angle_tol and radius_gap < gap_radius_tol)

    closure_metric = (
        0.35 * prox
        + 0.25 * np.exp(-6.0 * phase_gap)
        + 0.20 * np.exp(-8.0 * abs(r - target_radius))
        + 0.20 * np.exp(-8.0 * abs(wrap_angle(theta - psi_m)))
    )

    closure_event = int(closure_metric > closure_tol)

    # --------------------------------------------------------
    # CONTROLLER
    # --------------------------------------------------------
    u_ieee = -k_r * (r - target_radius) - k_theta * np.sin(theta - theta_ref)
    u_field = 0.03 * np.cos(theta - psi_m)
    u_lock = -k_lock * (z_olgo - shells[1])

    u = u_ieee + u_field + u_lock

    # 👇 Stabilitäts-Startphase
    if t < 10:
        u = 0.0

    u = np.clip(u, -u_clip, u_clip)

    # --------------------------------------------------------
    # APPLY (FIXED!)
    # --------------------------------------------------------
    factor = 1.0 + u * 0.08
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
    controlled["psi_m"].append(psi_m)
    controlled["psi_s"].append(psi_s)
    controlled["r_m"].append(r_m)
    controlled["r_s"].append(r_s)
    controlled["node_m"].append(node_m)
    controlled["node_s"].append(node_s)
    controlled["gap_event"].append(gap_event)
    controlled["closure_event"].append(closure_event)
    controlled["mode"].append(mode)
    controlled["closure_metric"].append(closure_metric)

    prev_theta = theta

# ============================================================
# REPORT SAFE
# ============================================================
def safe_mean(x): return np.mean(x) if len(x) else 0.0
def safe_max(x): return np.max(x) if len(x) else 0.0

report = f"""
Mean voltage: {safe_mean(controlled['voltage']):.4f}
Mean coherence: {safe_mean(controlled['coherence']):.4f}
Mean radius: {safe_mean(controlled['radius']):.4f}

Mean OLGO proximity: {safe_mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {safe_max(controlled['olgo_prox']):.4f}
"""

REPORT_PATH.write_text(report)
print(report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(3, 1, figsize=(10, 10))

axs[0].plot(controlled["voltage"])
axs[0].set_title("Voltage")

axs[1].plot(controlled["coherence"])
axs[1].set_title("Coherence")

axs[2].plot(controlled["closure_metric"])
axs[2].set_title("Closure Metric")

fig.tight_layout()
fig.savefig(TS_PATH)
plt.close()

print(f"📊 Saved: {TS_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
