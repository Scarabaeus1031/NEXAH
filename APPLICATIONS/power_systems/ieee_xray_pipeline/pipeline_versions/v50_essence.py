import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp

# ============================================================
# PATHS
# ============================================================
OUTDIR = Path("./results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH = OUTDIR / "v50_timeseries.png"

print(f"\n📁 v50 running → {OUTDIR.resolve()}\n")

# ============================================================
# OLGO / SHELL
# ============================================================
phi = (1 + np.sqrt(5)) / 2
pi = np.pi

f0 = (phi ** 3) / (pi ** 2)
epsilon = 0.029
shells = np.array([f0, f0 + epsilon, f0 + 2 * epsilon])

def olgo_proximity(z, sharpness=80.0):
    d = np.min(np.abs(shells - z))
    return np.exp(-sharpness * d)

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

# ============================================================
# GRID
# ============================================================
np.random.seed(42)
net = pp.networks.case57()
net.load.p_mw *= 0.85
net.load.q_mvar *= 0.85

base_p = net.load.p_mw.copy()
base_q = net.load.q_mvar.copy()

# ============================================================
# STORAGE
# ============================================================
data = {
    "voltage": [],
    "coherence": [],
    "radius": [],
    "theta": [],
    "z": [],
    "prox": [],
    "u": [],
    "closure": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400
theta_ref = -np.pi / 2
target_radius = 0.22

k_r = 0.22
k_theta = 0.05
k_lock = 0.10

u_clip = 0.10

# ============================================================
# LOOP
# ============================================================
for t in range(T):
    print(f"step {t}")

    try:
        pp.runpp(net, max_iteration=20)
    except:
        print("⚠️ PF failed → reset")
        net.load.p_mw = base_p * 0.95
        net.load.q_mvar = base_q * 0.95
        continue

    vm = net.res_bus.vm_pu.values
    v_mean = np.mean(vm)

    coh = 1.0 - np.std(vm)
    sw = (v_mean - 1.0) * 10.0

    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = wrap_angle(np.arctan2(sw - 0.000076, coh - 0.942913))

    z = 0.5 * coh + 0.5 * (1 - abs(sw))
    prox = olgo_proximity(z)

    # --------------------------------------------------------
    # CONTROLLER
    # --------------------------------------------------------
    u_ieee = -k_r * (r - target_radius)
    u_theta = -k_theta * np.sin(theta - theta_ref)

    # shell lock (soft)
    shell_target = shells[0]
    u_lock = -k_lock * (z - shell_target)

    # --------------------------------------------------------
    # v50 breathing (NEW CORE)
    # --------------------------------------------------------
    u_breath = -0.02 * (r - target_radius)

    u = u_ieee + u_theta + u_lock

    if prox > 0.25:
        u += u_breath

    # soft lock (not freezing)
    if prox > 0.2:
        u *= 0.92

    u = np.clip(u, -u_clip, u_clip)

    # --------------------------------------------------------
    # APPLY
    # --------------------------------------------------------
    factor = 1.0 + u * 0.08
    net.load.p_mw *= factor
    net.load.q_mvar *= factor

    # --------------------------------------------------------
    # CLOSURE METRIC (simple + stable)
    # --------------------------------------------------------
    closure = (
        0.5 * prox
        + 0.5 * np.exp(-5.0 * abs(r - target_radius))
    )

    # --------------------------------------------------------
    # STORE
    # --------------------------------------------------------
    data["voltage"].append(v_mean)
    data["coherence"].append(coh)
    data["radius"].append(r)
    data["theta"].append(theta)
    data["z"].append(z)
    data["prox"].append(prox)
    data["u"].append(u)
    data["closure"].append(closure)

# ============================================================
# PLOTS
# ============================================================
fig, axs = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

axs[0].plot(data["voltage"])
axs[0].set_title("Voltage")

axs[1].plot(data["coherence"])
axs[1].set_title("Coherence")

axs[2].plot(data["radius"])
axs[2].axhline(target_radius, linestyle="--")
axs[2].set_title("Radius")

axs[3].plot(data["closure"])
axs[3].set_title("Closure Metric")

plt.tight_layout()
plt.savefig(TS_PATH, dpi=150)
plt.close()

print("\n✅ v50 finished")
print(f"📊 Saved: {TS_PATH}")
