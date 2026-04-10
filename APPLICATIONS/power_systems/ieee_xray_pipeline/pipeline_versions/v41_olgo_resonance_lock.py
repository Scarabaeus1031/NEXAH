import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# PATH
# ============================================================
OUTDIR = Path("/Users/tho2020/Documents/GitHub/NEXAH/APPLICATIONS/power_systems/ieee_xray_pipeline/results")
OUTDIR.mkdir(parents=True, exist_ok=True)

REPORT_PATH = OUTDIR / "v41_olgo_lock_report.txt"
CUBE_PATH   = OUTDIR / "v41_olgo_lock_3d.png"
TS_PATH     = OUTDIR / "v41_olgo_lock_timeseries.png"
POLAR_PATH  = OUTDIR / "v41_olgo_lock_polar.png"

print(f"\n📁 v41 running → {OUTDIR.resolve()}\n")

# ============================================================
# OLGO RESONANCE LAYER
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
    "dist_elastic": [],
    "u": [],
    "z_olgo": [],
    "olgo_prox": [],
    "shell_target": [],
    "shell_index": [],
    "phase_term": [],
    "lock_term": [],
    "damp_term": [],
}

escape_count = 0
lock_count = 0

# ============================================================
# CONTROLLER SETTINGS
# ============================================================
target_radius = 0.040
target_theta = -np.pi / 2   # passt zu deinem aktuellen Drift-Bereich recht gut

# gains
k_core   = 0.60
k_band   = 0.85
k_theta  = 0.12
k_lock   = 0.18
k_phase  = 0.025
k_olgo   = 0.05

# breathing
breath_amp = 0.012
breath_w   = 0.10

# damping threshold
lock_threshold = 0.30

# ============================================================
# MAIN LOOP
# ============================================================
for t in range(400):
    pp.runpp(net, enforce_q_lims=True)

    vm = net.res_bus.vm_pu.values
    v_mean = np.mean(vm)

    coh = 1.0 - np.std(vm)
    sw  = (v_mean - 1.0) * 10.0

    # geometric state space
    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = np.arctan2(sw - 0.000076, coh - 0.942913)
    dist_elastic = abs(theta - np.pi / 4)

    # --------------------------------------------------------
    # OLGO mapping
    # --------------------------------------------------------
    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo)
    shell_tgt, shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # Lissajous-like phase modulation
    # --------------------------------------------------------
    phase_mod = np.sin(3.0 * t) * np.sin(2.0 * t + np.pi / 2)

    # --------------------------------------------------------
    # base controller (v36/v40 ancestry)
    # --------------------------------------------------------
    u = 0.0
    u += k_core * max(0.0, target_radius - r)
    u += k_band * (target_radius + breath_amp * np.sin(breath_w * t) - r)
    u += k_theta * (target_theta - theta)

    # --------------------------------------------------------
    # NEW 1: resonance drive
    # --------------------------------------------------------
    u_olgo = k_olgo * prox * phase_mod
    u += u_olgo

    # --------------------------------------------------------
    # NEW 2: shell lock term
    # pulls z_olgo gently toward nearest shell
    # --------------------------------------------------------
    u_lock = -k_lock * (z_olgo - shell_tgt)
    u += u_lock

    # --------------------------------------------------------
    # NEW 3: phase stabilizer
    # stronger only near resonance
    # --------------------------------------------------------
    u_phase = -k_phase * prox * np.sin(theta - target_theta)
    u += u_phase

    # --------------------------------------------------------
    # NEW 4: damping when resonance is reached
    # avoid overshooting once shell contact happens
    # --------------------------------------------------------
    damp_factor = 1.0
    if prox > lock_threshold:
        damp_factor = 0.45
        lock_count += 1

    u *= damp_factor
    u = np.clip(u, -0.12, 0.12)

    # --------------------------------------------------------
    # apply to loads
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
    controlled["dist_elastic"].append(dist_elastic)
    controlled["u"].append(u)
    controlled["z_olgo"].append(z_olgo)
    controlled["olgo_prox"].append(prox)
    controlled["shell_target"].append(shell_tgt)
    controlled["shell_index"].append(shell_idx)
    controlled["phase_term"].append(u_phase)
    controlled["lock_term"].append(u_lock)
    controlled["damp_term"].append(damp_factor)

    if r > 0.055:
        escape_count += 1

# ============================================================
# REPORT
# ============================================================
shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["shell_index"]) == i))
    for i in range(len(shells))
}

report = f"""NEXAH v41 – OLGO Resonance Lock

Escape count: {escape_count}
Lock count (prox > {lock_threshold}): {lock_count}

Mean voltage: {np.mean(controlled['voltage']):.4f}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean radius: {np.mean(controlled['radius']):.4f}
Mean dist to elastic axis: {np.mean(controlled['dist_elastic']):.4f}

Mean OLGO proximity: {np.mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {np.max(controlled['olgo_prox']):.4f}

Mean control signal: {np.mean(controlled['u']):.4f}
Mean lock term: {np.mean(controlled['lock_term']):.4f}
Mean phase term: {np.mean(controlled['phase_term']):.4f}

Shell occupancy:
  Core: {shell_hits['Core']}
  Transition: {shell_hits['Transition']}
  Expansion: {shell_hits['Expansion']}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print(report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(6, 1, figsize=(14, 16), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v41 OLGO Resonance Lock Timeseries")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple")
axs[2].axhline(target_radius, color="green", linestyle="--")
axs[2].set_ylabel("Radius")

axs[3].plot(controlled["dist_elastic"], color="darkorange")
axs[3].set_ylabel("Dist Elastic")

axs[4].plot(controlled["olgo_prox"], color="magenta", label="OLGO proximity")
axs[4].axhline(lock_threshold, color="gray", linestyle="--", label="Lock threshold")
axs[4].set_ylabel("OLGO prox")
axs[4].legend()

axs[5].plot(controlled["u"], color="black", label="u")
axs[5].plot(controlled["lock_term"], color="red", alpha=0.7, label="lock term")
axs[5].plot(controlled["phase_term"], color="cyan", alpha=0.7, label="phase term")
axs[5].set_ylabel("Control")
axs[5].set_xlabel("Time step")
axs[5].legend()

fig.tight_layout()
fig.savefig(TS_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# POLAR
# ============================================================
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="polar")
ax.plot(controlled["theta"], controlled["radius"], color="steelblue", alpha=0.7, label="trajectory")
sc = ax.scatter(
    controlled["theta"],
    controlled["radius"],
    c=controlled["olgo_prox"],
    cmap="plasma",
    s=18,
    label="OLGO prox"
)
ax.set_title("v41 OLGO Resonance Lock Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# 3D
# ============================================================
fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(projection="3d")

x = controlled["radius"]
y = controlled["theta"]
z = controlled["z_olgo"]

sc = ax.scatter(x, y, z, c=controlled["olgo_prox"], cmap="plasma", s=14)
ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("OLGO Z")
ax.set_title("v41 OLGO Resonance Lock 3D")

# shell guide lines
for s in shells:
    ax.plot([min(x), max(x)], [target_theta, target_theta], [s, s], linestyle="--", alpha=0.35)

fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📊 Saved: {POLAR_PATH.name}")
print(f"📊 Saved: {CUBE_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
