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

REPORT_PATH = OUTDIR / "v42_phase_crossing_report.txt"
TS_PATH     = OUTDIR / "v42_phase_crossing_timeseries.png"
POLAR_PATH  = OUTDIR / "v42_phase_crossing_polar.png"
CUBE_PATH   = OUTDIR / "v42_phase_crossing_3d.png"

print(f"\n📁 v42 running → {OUTDIR.resolve()}\n")

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

def crossed_reference(prev_theta, theta, theta_ref, eps=0.03):
    """
    Detects whether theta crossed the reference line between steps.
    """
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
    "theta_ref": [],
    "phase_error": [],
    "cross_event": [],
    "kick_term": [],
    "hold_term": [],
    "lock_term": [],
    "mode": [],
}

# ============================================================
# CONTROLLER SETTINGS
# ============================================================
T = 400

target_radius = 0.040
theta_ref = -np.pi / 2            # gold / phase line
theta_hold_width = 0.12           # hold corridor around reference
cross_eps = 0.02
cooldown_steps = 12

# continuous gains
k_core = 0.55
k_band = 0.75
k_theta = 0.10
k_lock  = 0.12
k_hold  = 0.06

# breathing / base modulation
breath_amp = 0.010
breath_w = 0.10

# event gains
kick_gain = 0.08
radial_kick_gain = 0.04
mirror_sign = 1.0

# resonance settings
lock_threshold = 0.30
prox_sharpness = 80.0

# ============================================================
# STATE
# ============================================================
escape_count = 0
cross_count = 0
lock_count = 0
prev_theta = None
cooldown = 0

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
    theta = np.arctan2(sw - 0.000076, coh - 0.942913)
    theta = wrap_angle(theta)
    dist_elastic = abs(theta - np.pi / 4)

    # --------------------------------------------------------
    # OLGO mapping
    # --------------------------------------------------------
    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo, sharpness=prox_sharpness)
    shell_tgt, shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # base controller
    # --------------------------------------------------------
    u = 0.0

    # radial breathing
    radial_target = target_radius + breath_amp * np.sin(breath_w * t)
    u += k_core * max(0.0, target_radius - r)
    u += k_band * (radial_target - r)

    # weak continuous theta guidance
    phase_error = wrap_angle(theta - theta_ref)
    u_theta = -k_theta * np.sin(phase_error)
    u += u_theta

    # shell lock
    u_lock = -k_lock * (z_olgo - shell_tgt)
    u += u_lock

    # hold near phase corridor
    in_hold_corridor = abs(phase_error) < theta_hold_width
    u_hold = 0.0
    if in_hold_corridor:
        u_hold = -k_hold * phase_error
        u += u_hold

    # --------------------------------------------------------
    # event-driven crossing logic
    # --------------------------------------------------------
    cross_event = 0
    u_kick = 0.0
    mode = "drift"

    if prev_theta is not None and cooldown == 0:
        if crossed_reference(prev_theta, theta, theta_ref, eps=cross_eps):
            cross_event = 1
            cross_count += 1
            cooldown = cooldown_steps
            mode = "phase_cross"

            # mirror flip
            mirror_sign *= -1.0

            # pink-X trigger:
            # kick depends on resonance and whether we are near hold line
            u_kick += mirror_sign * kick_gain * (0.35 + prox)

            # small radial kick: if too far out, pull inward; if too close, push outward
            radial_error = target_radius - r
            u_kick += radial_kick_gain * np.sign(radial_error)

            # if resonance is already active, soften the kick
            if prox > lock_threshold:
                u_kick *= 0.55
                lock_count += 1

            u += u_kick

    # cooldown decay
    if cooldown > 0:
        cooldown -= 1

    # --------------------------------------------------------
    # additional resonance hold
    # --------------------------------------------------------
    if prox > lock_threshold:
        mode = "lock_hold"
        lock_count += 1
        # do not let the controller overshoot too much once resonance is reached
        u *= 0.75

    # clip
    u = np.clip(u, -0.12, 0.12)

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
    controlled["shell_target"].append(shell_tgt)
    controlled["shell_index"].append(shell_idx)
    controlled["theta_ref"].append(theta_ref)
    controlled["phase_error"].append(phase_error)
    controlled["cross_event"].append(cross_event)
    controlled["kick_term"].append(u_kick)
    controlled["hold_term"].append(u_hold)
    controlled["lock_term"].append(u_lock)
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

report = f"""NEXAH v42 – Phase Crossing Controller

Escape count: {escape_count}
Cross count: {cross_count}
Lock count (prox > {lock_threshold}): {lock_count}

Mean voltage: {np.mean(controlled['voltage']):.4f}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean radius: {np.mean(controlled['radius']):.4f}
Mean dist to elastic axis: {np.mean(controlled['dist_elastic']):.4f}

Mean OLGO proximity: {np.mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {np.max(controlled['olgo_prox']):.4f}

Mean control signal: {np.mean(controlled['u']):.4f}
Mean kick term: {np.mean(controlled['kick_term']):.4f}
Mean hold term: {np.mean(controlled['hold_term']):.4f}
Mean lock term: {np.mean(controlled['lock_term']):.4f}

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
fig, axs = plt.subplots(7, 1, figsize=(14, 18), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v42 Phase Crossing Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple")
axs[2].axhline(target_radius, color="green", linestyle="--", label="target r")
axs[2].set_ylabel("Radius")
axs[2].legend()

axs[3].plot(controlled["theta"], color="darkcyan", label="theta")
axs[3].plot(controlled["theta_ref"], color="gold", linestyle="--", label="theta_ref")
axs[3].set_ylabel("Theta")
axs[3].legend()

axs[4].plot(controlled["olgo_prox"], color="magenta", label="OLGO prox")
axs[4].axhline(lock_threshold, color="gray", linestyle="--", label="lock threshold")
axs[4].set_ylabel("OLGO prox")
axs[4].legend()

axs[5].plot(controlled["u"], color="black", label="u")
axs[5].plot(controlled["kick_term"], color="hotpink", alpha=0.8, label="kick")
axs[5].plot(controlled["hold_term"], color="cyan", alpha=0.8, label="hold")
axs[5].plot(controlled["lock_term"], color="red", alpha=0.8, label="lock")
axs[5].set_ylabel("Control")
axs[5].legend()

axs[6].plot(controlled["cross_event"], color="hotpink", label="cross event")
axs[6].set_ylabel("Cross")
axs[6].set_xlabel("Time step")
axs[6].legend()

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

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="trajectory")
sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

# mark crossings
cross_idx = np.where(cross_vals > 0)[0]
if len(cross_idx) > 0:
    ax.scatter(theta_vals[cross_idx], r_vals[cross_idx], color="hotpink", s=40, label="phase crosses")

ax.set_title("v42 Phase Crossing Polar")
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
ax.set_title("v42 Phase Crossing 3D")

# shell guides
for s in shells:
    ax.plot([x.min(), x.max()], [theta_ref, theta_ref], [s, s], linestyle="--", alpha=0.35)

# crossing points
if len(cross_idx) > 0:
    ax.scatter(x[cross_idx], y[cross_idx], z[cross_idx], color="hotpink", s=35)

fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📊 Saved: {POLAR_PATH.name}")
print(f"📊 Saved: {CUBE_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
