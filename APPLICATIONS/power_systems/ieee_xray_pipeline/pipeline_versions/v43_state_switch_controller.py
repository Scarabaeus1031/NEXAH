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

REPORT_PATH = OUTDIR / "v43_state_switch_report.txt"
TS_PATH     = OUTDIR / "v43_state_switch_timeseries.png"
POLAR_PATH  = OUTDIR / "v43_state_switch_polar.png"
CUBE_PATH   = OUTDIR / "v43_state_switch_3d.png"

print(f"\n📁 v43 running → {OUTDIR.resolve()}\n")

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

def crossed_reference(prev_theta, theta, theta_ref, eps=0.02):
    a = wrap_angle(prev_theta - theta_ref)
    b = wrap_angle(theta - theta_ref)
    if abs(a) < eps or abs(b) < eps:
        return True
    return (a * b) < 0

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
    "target_shell_index": [],
    "theta_ref": [],
    "theta_branch_target": [],
    "phase_error": [],
    "cross_event": [],
    "switch_event": [],
    "branch_sign": [],
    "mode": [],
    "u_radial": [],
    "u_theta": [],
    "u_lock": [],
    "u_hold": [],
    "u_switch": [],
    "u_shell_reentry": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

# reference line
theta_ref = -np.pi / 2

# branch corridor
branch_offset = 0.09         # target lanes around reference
hold_width = 0.06

# radius targets
r_inner = 0.035
r_outer = 0.060
breath_amp = 0.006
breath_w = 0.12

# gains
k_radial = 0.22
k_theta = 0.10
k_hold = 0.08
k_lock = 0.06
k_shell_reentry = 0.14
k_switch = 0.06

# crossing logic
cross_eps = 0.02
cooldown_steps = 10
prox_threshold = 0.30

# control clipping
u_clip = 0.08

# ============================================================
# INTERNAL STATE
# ============================================================
prev_theta = None
cooldown = 0
branch_sign = 1.0
active_shell_idx = 1      # start in transition shell as experimental target
mode = "init"

escape_count = 0
cross_count = 0
switch_count = 0
lock_count = 0

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
    # geometric state
    # --------------------------------------------------------
    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = wrap_angle(np.arctan2(sw - 0.000076, coh - 0.942913))
    dist_elastic = abs(theta - np.pi / 4)

    # --------------------------------------------------------
    # OLGO mapping
    # --------------------------------------------------------
    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo, sharpness=80.0)
    nearest_shell_value, nearest_shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # crossing / state-switch logic
    # --------------------------------------------------------
    cross_event = 0
    switch_event = 0

    if prev_theta is not None and cooldown == 0:
        if crossed_reference(prev_theta, theta, theta_ref, eps=cross_eps):
            cross_event = 1
            cross_count += 1
            cooldown = cooldown_steps

            # flip branch
            branch_sign *= -1.0

            # rotate shell target cyclically:
            # Expansion -> Transition -> Core -> Transition -> Expansion ...
            if active_shell_idx == 2:
                active_shell_idx = 1
            elif active_shell_idx == 1:
                active_shell_idx = 0
            else:
                active_shell_idx = 1

            switch_event = 1
            switch_count += 1
            mode = "switch"

    if cooldown > 0:
        cooldown -= 1

    # --------------------------------------------------------
    # switched targets
    # --------------------------------------------------------
    theta_branch_target = wrap_angle(theta_ref + branch_sign * branch_offset)

    # alternate radius track with branch
    r_target_base = r_outer if branch_sign > 0 else r_inner
    r_target = r_target_base + breath_amp * np.sin(breath_w * t)

    shell_target = shells[active_shell_idx]

    # --------------------------------------------------------
    # controller terms
    # --------------------------------------------------------
    phase_error = wrap_angle(theta - theta_branch_target)

    # radial term
    u_radial = -k_radial * (r - r_target)

    # switched theta guidance
    u_theta = -k_theta * np.sin(phase_error)

    # hold corridor near target branch lane
    u_hold = 0.0
    if abs(phase_error) < hold_width:
        u_hold = -k_hold * phase_error

    # shell attraction to chosen shell, not nearest shell
    u_lock = -k_lock * (z_olgo - shell_target)

    # stronger re-entry term if system sits too high in expansion
    shell_error = z_olgo - shell_target
    u_shell_reentry = -k_shell_reentry * shell_error

    # switch impulse: brief geometry change after crossing
    u_switch = 0.0
    if switch_event == 1:
        u_switch = k_switch * branch_sign

    # combine
    u = (
        u_radial
        + u_theta
        + u_hold
        + u_lock
        + u_shell_reentry
        + u_switch
    )

    # resonance hold
    if prox > prox_threshold:
        mode = "lock_hold"
        lock_count += 1
        u *= 0.65
    elif switch_event == 1:
        mode = "switch"
    else:
        mode = "track"

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
    controlled["dist_elastic"].append(dist_elastic)
    controlled["u"].append(u)
    controlled["z_olgo"].append(z_olgo)
    controlled["olgo_prox"].append(prox)
    controlled["shell_target"].append(shell_target)
    controlled["shell_index"].append(nearest_shell_idx)
    controlled["target_shell_index"].append(active_shell_idx)
    controlled["theta_ref"].append(theta_ref)
    controlled["theta_branch_target"].append(theta_branch_target)
    controlled["phase_error"].append(phase_error)
    controlled["cross_event"].append(cross_event)
    controlled["switch_event"].append(switch_event)
    controlled["branch_sign"].append(branch_sign)
    controlled["mode"].append(mode)
    controlled["u_radial"].append(u_radial)
    controlled["u_theta"].append(u_theta)
    controlled["u_lock"].append(u_lock)
    controlled["u_hold"].append(u_hold)
    controlled["u_switch"].append(u_switch)
    controlled["u_shell_reentry"].append(u_shell_reentry)

    if r > 0.055:
        escape_count += 1

    prev_theta = theta

# ============================================================
# REPORT
# ============================================================
observed_shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["shell_index"]) == i))
    for i in range(len(shells))
}

target_shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["target_shell_index"]) == i))
    for i in range(len(shells))
}

report = f"""NEXAH v43 – State Switch Controller

Escape count: {escape_count}
Cross count: {cross_count}
Switch count: {switch_count}
Lock count (prox > {prox_threshold}): {lock_count}

Mean voltage: {np.mean(controlled['voltage']):.4f}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean radius: {np.mean(controlled['radius']):.4f}
Mean dist to elastic axis: {np.mean(controlled['dist_elastic']):.4f}

Mean OLGO proximity: {np.mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {np.max(controlled['olgo_prox']):.4f}

Mean control signal: {np.mean(controlled['u']):.4f}
Mean radial term: {np.mean(controlled['u_radial']):.4f}
Mean theta term: {np.mean(controlled['u_theta']):.4f}
Mean lock term: {np.mean(controlled['u_lock']):.4f}
Mean shell reentry term: {np.mean(controlled['u_shell_reentry']):.4f}
Mean switch term: {np.mean(controlled['u_switch']):.4f}

Observed shell occupancy:
  Core: {observed_shell_hits['Core']}
  Transition: {observed_shell_hits['Transition']}
  Expansion: {observed_shell_hits['Expansion']}

Target shell occupancy:
  Core: {target_shell_hits['Core']}
  Transition: {target_shell_hits['Transition']}
  Expansion: {target_shell_hits['Expansion']}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print(report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(8, 1, figsize=(14, 20), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v43 State Switch Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple", label="radius")
axs[2].axhline(r_inner, color="green", linestyle="--", alpha=0.7, label="r_inner")
axs[2].axhline(r_outer, color="darkgreen", linestyle="--", alpha=0.7, label="r_outer")
axs[2].set_ylabel("Radius")
axs[2].legend()

axs[3].plot(controlled["theta"], color="teal", label="theta")
axs[3].plot(controlled["theta_ref"], color="gold", linestyle="--", label="theta_ref")
axs[3].plot(controlled["theta_branch_target"], color="hotpink", linestyle=":", label="branch target")
axs[3].set_ylabel("Theta")
axs[3].legend()

axs[4].plot(controlled["z_olgo"], color="slateblue", label="z_olgo")
for s in shells:
    axs[4].axhline(s, color="gray", linestyle="--", alpha=0.5)
axs[4].set_ylabel("OLGO Z")
axs[4].legend()

axs[5].plot(controlled["olgo_prox"], color="magenta", label="OLGO prox")
axs[5].axhline(prox_threshold, color="gray", linestyle="--", label="lock threshold")
axs[5].set_ylabel("OLGO prox")
axs[5].legend()

axs[6].plot(controlled["u"], color="black", label="u")
axs[6].plot(controlled["u_radial"], color="purple", alpha=0.7, label="radial")
axs[6].plot(controlled["u_theta"], color="cyan", alpha=0.7, label="theta")
axs[6].plot(controlled["u_lock"], color="red", alpha=0.7, label="lock")
axs[6].plot(controlled["u_shell_reentry"], color="orange", alpha=0.7, label="shell reentry")
axs[6].plot(controlled["u_switch"], color="hotpink", alpha=0.9, label="switch")
axs[6].set_ylabel("Control")
axs[6].legend(ncol=3)

axs[7].plot(controlled["cross_event"], color="hotpink", label="cross")
axs[7].plot(controlled["switch_event"], color="darkviolet", alpha=0.8, label="switch")
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
cross_vals = np.array(controlled["cross_event"])
switch_vals = np.array(controlled["switch_event"])

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="trajectory")
sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

cross_idx = np.where(cross_vals > 0)[0]
switch_idx = np.where(switch_vals > 0)[0]

if len(cross_idx) > 0:
    ax.scatter(theta_vals[cross_idx], r_vals[cross_idx], color="hotpink", s=40, label="cross")
if len(switch_idx) > 0:
    ax.scatter(theta_vals[switch_idx], r_vals[switch_idx], color="darkviolet", s=20, label="switch")

ax.set_title("v43 State Switch Polar")
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
ax.set_xlabel("Radius")
ax.set_ylabel("Theta")
ax.set_zlabel("OLGO Z")
ax.set_title("v43 State Switch 3D")

for s in shells:
    ax.plot([x.min(), x.max()], [theta_ref, theta_ref], [s, s], linestyle="--", alpha=0.35)

if len(cross_idx) > 0:
    ax.scatter(x[cross_idx], y[cross_idx], z[cross_idx], color="hotpink", s=35)
if len(switch_idx) > 0:
    ax.scatter(x[switch_idx], y[switch_idx], z[switch_idx], color="darkviolet", s=18)

fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📊 Saved: {POLAR_PATH.name}")
print(f"📊 Saved: {CUBE_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
