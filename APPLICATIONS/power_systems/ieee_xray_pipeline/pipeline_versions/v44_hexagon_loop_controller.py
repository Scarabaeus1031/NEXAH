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

REPORT_PATH = OUTDIR / "v44_hexagon_loop_report.txt"
TS_PATH     = OUTDIR / "v44_hexagon_loop_timeseries.png"
POLAR_PATH  = OUTDIR / "v44_hexagon_loop_polar.png"
CUBE_PATH   = OUTDIR / "v44_hexagon_loop_3d.png"
GRAPH_PATH  = OUTDIR / "v44_hexagon_loop_graph.png"

print(f"\n📁 v44 running → {OUTDIR.resolve()}\n")

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

def angle_to_hex_sector(theta):
    """
    Map angle to one of 6 hex sectors.
    Uses [0, 2pi) representation.
    """
    a = (theta + 2 * np.pi) % (2 * np.pi)
    sector = int(np.floor(a / (np.pi / 3.0))) % 6
    return sector

def crossed_sector(prev_sector, current_sector):
    return prev_sector != current_sector

# ============================================================
# HEXAGON GRAPH
# ============================================================
# 6 outer nodes + center loop node
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
    "dist_elastic": [],
    "u": [],
    "z_olgo": [],
    "olgo_prox": [],
    "shell_index": [],
    "node_id": [],
    "node_switch": [],
    "loop_event": [],
    "u_forward": [],
    "u_feedback": [],
    "u_lock": [],
    "u_reentry": [],
    "mode": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2
target_radius = 0.045
target_radius_outer = 0.060

# loop / reentry
inner_loop_radius = 0.42      # experimental: below this, treat as loop reentry zone
node_hold_gain = 0.035
reentry_gain = 0.065

# gains
k_radial = 0.11
k_theta = 0.05
k_lock = 0.045
k_forward = 0.030
k_feedback = 0.040

u_clip = 0.08
prox_threshold = 0.30

# ============================================================
# INTERNAL STATE
# ============================================================
prev_sector = None
current_target_sector = None

escape_count = 0
node_switch_count = 0
loop_count = 0
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
    # olgo mapping
    # --------------------------------------------------------
    z_olgo = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z_olgo)
    _, shell_idx = nearest_shell(z_olgo)

    # --------------------------------------------------------
    # topological mapping
    # --------------------------------------------------------
    node_id = angle_to_hex_sector(theta)
    node_switch = 0
    loop_event = 0

    if prev_sector is None:
        current_target_sector = node_id
    else:
        if crossed_sector(prev_sector, node_id):
            node_switch = 1
            node_switch_count += 1
            current_target_sector = node_id

    # --------------------------------------------------------
    # loop / eyelet logic
    # "0 are loops, not voids"
    # --------------------------------------------------------
    if r < inner_loop_radius:
        loop_event = 1
        loop_count += 1

    # --------------------------------------------------------
    # target geometry from sector
    # --------------------------------------------------------
    sector_angle = hex_angles[current_target_sector]
    sector_angle = wrap_angle(sector_angle)

    # --------------------------------------------------------
    # controller terms
    # --------------------------------------------------------
    # 1. radial regulation
    radial_target = target_radius_outer if node_id in [0, 1, 5] else target_radius
    u_radial = -k_radial * (r - radial_target)

    # 2. forward propagation (Leo / yellow)
    phase_error_forward = wrap_angle(theta - sector_angle)
    u_forward = -k_forward * np.sin(phase_error_forward)

    # 3. feedback / reflection (Lilith / pink)
    phase_error_feedback = wrap_angle(theta - theta_ref)
    u_feedback = -k_feedback * np.sin(phase_error_feedback)

    # 4. shell lock
    shell_target = shells[1] if loop_event else shells[2]
    u_lock = -k_lock * (z_olgo - shell_target)

    # 5. reentry through loop node
    u_reentry = 0.0
    if loop_event:
        # if in inner loop zone, bias toward current sector and keep it from falling through
        u_reentry += reentry_gain * np.cos(theta - sector_angle)
        u_reentry += node_hold_gain * np.cos(theta - theta_ref)

    # combine
    u = u_radial + u_forward + u_feedback + u_lock + u_reentry

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
    controlled["dist_elastic"].append(dist_elastic)
    controlled["u"].append(u)
    controlled["z_olgo"].append(z_olgo)
    controlled["olgo_prox"].append(prox)
    controlled["shell_index"].append(shell_idx)
    controlled["node_id"].append(node_id)
    controlled["node_switch"].append(node_switch)
    controlled["loop_event"].append(loop_event)
    controlled["u_forward"].append(u_forward)
    controlled["u_feedback"].append(u_feedback)
    controlled["u_lock"].append(u_lock)
    controlled["u_reentry"].append(u_reentry)
    controlled["mode"].append("loop" if loop_event else "sector")

    if r > 0.055:
        escape_count += 1

    prev_sector = node_id

# ============================================================
# REPORT
# ============================================================
shell_hits = {
    shell_names[i]: int(np.sum(np.array(controlled["shell_index"]) == i))
    for i in range(len(shells))
}

node_counts = {
    f"node_{i}": int(np.sum(np.array(controlled["node_id"]) == i))
    for i in range(6)
}

report = f"""NEXAH v44 – Hexagon Loop Controller

Escape count: {escape_count}
Node switch count: {node_switch_count}
Loop count: {loop_count}
Lock count (prox > {prox_threshold}): {lock_count}

Mean voltage: {np.mean(controlled['voltage']):.4f}
Mean coherence: {np.mean(controlled['coherence']):.4f}
Mean radius: {np.mean(controlled['radius']):.4f}
Mean dist to elastic axis: {np.mean(controlled['dist_elastic']):.4f}

Mean OLGO proximity: {np.mean(controlled['olgo_prox']):.4f}
Max OLGO proximity: {np.max(controlled['olgo_prox']):.4f}
Mean control signal: {np.mean(controlled['u']):.4f}

Observed shell occupancy:
  Core: {shell_hits['Core']}
  Transition: {shell_hits['Transition']}
  Expansion: {shell_hits['Expansion']}

Node occupancy:
  node_0: {node_counts['node_0']}
  node_1: {node_counts['node_1']}
  node_2: {node_counts['node_2']}
  node_3: {node_counts['node_3']}
  node_4: {node_counts['node_4']}
  node_5: {node_counts['node_5']}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print(report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(8, 1, figsize=(14, 20), sharex=True)

axs[0].plot(controlled["voltage"], color="orange")
axs[0].set_ylabel("Voltage")
axs[0].set_title("v44 Hexagon Loop Controller")

axs[1].plot(controlled["coherence"], color="blue")
axs[1].set_ylabel("Coherence")

axs[2].plot(controlled["radius"], color="purple")
axs[2].axhline(inner_loop_radius, color="hotpink", linestyle="--", label="loop threshold")
axs[2].axhline(target_radius, color="green", linestyle="--", alpha=0.7, label="target r")
axs[2].axhline(target_radius_outer, color="darkgreen", linestyle="--", alpha=0.7, label="outer r")
axs[2].set_ylabel("Radius")
axs[2].legend()

axs[3].plot(controlled["theta"], color="teal")
axs[3].axhline(theta_ref, color="gold", linestyle="--", label="theta ref")
axs[3].set_ylabel("Theta")
axs[3].legend()

axs[4].plot(controlled["z_olgo"], color="slateblue")
for s in shells:
    axs[4].axhline(s, color="gray", linestyle="--", alpha=0.5)
axs[4].set_ylabel("OLGO Z")

axs[5].plot(controlled["u"], color="black", label="u")
axs[5].plot(controlled["u_forward"], color="gold", alpha=0.8, label="forward")
axs[5].plot(controlled["u_feedback"], color="hotpink", alpha=0.8, label="feedback")
axs[5].plot(controlled["u_lock"], color="red", alpha=0.8, label="lock")
axs[5].plot(controlled["u_reentry"], color="cyan", alpha=0.8, label="reentry")
axs[5].set_ylabel("Control")
axs[5].legend(ncol=4)

axs[6].plot(controlled["node_id"], color="darkviolet")
axs[6].set_ylabel("Hex node")

axs[7].plot(controlled["node_switch"], color="purple", label="switch")
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
node_switch_vals = np.array(controlled["node_switch"])
loop_vals = np.array(controlled["loop_event"])

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.7, label="trajectory")
sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

switch_idx = np.where(node_switch_vals > 0)[0]
loop_idx = np.where(loop_vals > 0)[0]

if len(switch_idx) > 0:
    ax.scatter(theta_vals[switch_idx], r_vals[switch_idx], color="purple", s=38, label="node switch")
if len(loop_idx) > 0:
    ax.scatter(theta_vals[loop_idx], r_vals[loop_idx], color="hotpink", s=14, label="loop")

ax.set_title("v44 Hexagon Loop Polar")
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
ax.set_title("v44 Hexagon Loop 3D")

for s in shells:
    ax.plot([x.min(), x.max()], [theta_ref, theta_ref], [s, s], linestyle="--", alpha=0.35)

if len(switch_idx) > 0:
    ax.scatter(x[switch_idx], y[switch_idx], z[switch_idx], color="purple", s=32)
if len(loop_idx) > 0:
    ax.scatter(x[loop_idx], y[loop_idx], z[loop_idx], color="hotpink", s=14)

fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

# ============================================================
# HEXAGON GRAPH VISUAL
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

# outer ring
for i in range(6):
    x1, y1 = hex_nodes[i]
    x2, y2 = hex_nodes[(i + 1) % 6]
    ax.plot([x1, x2], [y1, y2], color="gray", alpha=0.8)

# center spokes
for i in range(6):
    x1, y1 = hex_nodes[i]
    ax.plot([0, x1], [0, y1], color="lightgray", alpha=0.6)

# nodes
ax.scatter(hex_nodes[:, 0], hex_nodes[:, 1], s=180, c="skyblue")
ax.scatter(center_node[:, 0], center_node[:, 1], s=220, c="hotpink")

# labels
for i, (xn, yn) in enumerate(hex_nodes):
    ax.text(xn * 1.08, yn * 1.08, f"{i}", ha="center", va="center", fontsize=12)
ax.text(0, 0, "loop", ha="center", va="center", fontsize=12, color="white")

# occupancy overlay
node_occ = np.array([node_counts[f"node_{i}"] for i in range(6)], dtype=float)
if node_occ.max() > 0:
    node_occ = node_occ / node_occ.max()
    for i, (xn, yn) in enumerate(hex_nodes):
        ax.scatter([xn], [yn], s=400 * node_occ[i] + 40, alpha=0.25, c="navy")

ax.set_title("v44 Hexagon Loop Topology")
ax.set_aspect("equal")
ax.axis("off")
fig.tight_layout()
fig.savefig(GRAPH_PATH, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"📊 Saved: {TS_PATH.name}")
print(f"📊 Saved: {POLAR_PATH.name}")
print(f"📊 Saved: {CUBE_PATH.name}")
print(f"📊 Saved: {GRAPH_PATH.name}")
print(f"📄 Saved: {REPORT_PATH.name}")
