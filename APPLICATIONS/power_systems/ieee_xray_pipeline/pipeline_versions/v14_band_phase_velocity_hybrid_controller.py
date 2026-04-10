"""
v14_band_phase_velocity_hybrid_controller.py
============================================

Goal:
- first practical NEXAH hybrid controller
- regulate the system toward a *stable band* instead of a fixed point
- combine:
    1. radial band control
    2. phase control
    3. phase-velocity control
- compare baseline vs controlled dynamics

Core idea:
- stability is not a point, but a ring / band
- the controller acts only when the orbit leaves the stable band
  or when phase / phase velocity drift too strongly

Chosen first target band:
    r* ≈ 0.587  (inspired by 37/63 ≈ 0.587)

Outputs:
- ieee57_v14_hybrid_timeseries.png
- ieee57_v14_hybrid_phase.png
- ieee57_v14_hybrid_polar.png
- ieee57_v14_hybrid_report.txt
"""

from pathlib import Path
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
import pandapower.networks as pn


# ============================================================
# 1. Paths
# ============================================================

BASE_DIR = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
BASE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. Configuration
# ============================================================

TIME_STEPS = 300
SEED = 42

# External excitation
LOAD_FACTOR = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, TIME_STEPS))
NOISE = np.random.default_rng(SEED).normal(0.0, 0.02, TIME_STEPS)

# Classical threshold
V_CLASSICAL = 0.90

# Learned / chosen stability center (from prior runs)
COH_CENTER = 0.917
SW_CENTER = 0.0

# Stable band in radius around the NEXAH center
R_TARGET = 0.587
R_BAND_HALF_WIDTH = 0.035
R_MIN = R_TARGET - R_BAND_HALF_WIDTH
R_MAX = R_TARGET + R_BAND_HALF_WIDTH

# Reference angle and velocity
THETA_REF = -np.pi / 2           # around lower arc / 270 deg
PHASE_TOL = 0.22                # phase tolerance
OMEGA_REF = 0.0                 # simple first version: prefer low net angular drift
OMEGA_TOL = 0.06

# Controller gains
K_R = 0.10
K_THETA = 0.035
K_OMEGA = 0.025

# Saturation
U_MAX = 0.08

# Only apply control when needed
USE_DEAD_ZONE = True


# ============================================================
# 3. Utilities
# ============================================================

def wrap_angle(angle: float) -> float:
    """Wrap angle to (-pi, pi]."""
    return (angle + np.pi) % (2 * np.pi) - np.pi


def clamp(value: float, vmin: float, vmax: float) -> float:
    return max(vmin, min(vmax, value))


def smooth(x: np.ndarray, win: int = 5) -> np.ndarray:
    if win <= 1 or len(x) < win:
        return x.copy()
    kernel = np.ones(win) / win
    pad_left = win // 2
    pad_right = win - 1 - pad_left
    xp = np.pad(x, (pad_left, pad_right), mode="edge")
    return np.convolve(xp, kernel, mode="valid")


def build_case57() -> pp.pandapowerNet:
    return pn.case57()


def compute_state_from_net(net: pp.pandapowerNet) -> tuple[float, float, float]:
    """
    Return:
        v_mean,
        coherence = 1 - std(vm_pu),
        switch signal ~ local gradient of v_mean is handled outside
    """
    try:
        pp.runpp(net, enforce_q_lims=True, init="auto")
        voltages = net.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net.bus)) * 0.95

    v_mean = float(np.mean(voltages))
    v_std = float(np.std(voltages))
    coherence = 1.0 - v_std
    return v_mean, coherence, v_std


def radial_phase_features(coh: float, sw: float, coh_center: float, sw_center: float) -> tuple[float, float]:
    """
    Convert (coherence, switch) to centered polar coordinates.
    Radius is normalized relative to available scale in this local state-space.
    """
    dx = coh - coh_center
    dy = sw - sw_center
    theta = np.arctan2(dy, dx)

    # Local normalization chosen so radii land in a useful ~[0,1] scale.
    # Coherence variations are much smaller numerically than switch variations,
    # so we scale x and y separately.
    x_scaled = dx / 0.03
    y_scaled = dy / 0.12
    r = float(np.sqrt(x_scaled ** 2 + y_scaled ** 2))
    return r, theta


# ============================================================
# 4. Baseline / controlled simulation
# ============================================================

def run_simulation(controlled: bool = False) -> dict:
    net = build_case57()

    # Preserve nominal loads
    base_p = net.load["p_mw"].to_numpy().copy()

    v_hist = []
    coh_hist = []
    sw_hist = []
    vstd_hist = []

    r_hist = []
    theta_hist = []
    omega_hist = []
    u_hist = []

    classical_event = None

    prev_theta = None

    for t in range(TIME_STEPS):
        # Baseline exogenous drive
        factor = LOAD_FACTOR[t] + NOISE[t]

        # Default no control
        u_t = 0.0

        # Use previous state to generate control for this time step
        if controlled and t > 3:
            coh_prev = coh_hist[-1]
            sw_prev = sw_hist[-1]
            r_prev = r_hist[-1]
            theta_prev = theta_hist[-1]
            omega_prev = omega_hist[-1]

            # --- 1) Radial band control ---
            radial_term = 0.0
            if r_prev < R_MIN:
                radial_term = K_R * (R_MIN - r_prev)
            elif r_prev > R_MAX:
                radial_term = -K_R * (r_prev - R_MAX)

            # --- 2) Phase control ---
            e_theta = wrap_angle(theta_prev - THETA_REF)
            phase_term = 0.0
            if abs(e_theta) > PHASE_TOL:
                phase_term = -K_THETA * e_theta

            # --- 3) Phase velocity control ---
            e_omega = omega_prev - OMEGA_REF
            omega_term = 0.0
            if abs(e_omega) > OMEGA_TOL:
                omega_term = -K_OMEGA * e_omega

            u_t = radial_term + phase_term + omega_term

            # Dead zone: no control if already well-centered
            if USE_DEAD_ZONE:
                in_radial_band = (R_MIN <= r_prev <= R_MAX)
                small_phase_err = abs(e_theta) <= PHASE_TOL
                small_omega_err = abs(e_omega) <= OMEGA_TOL
                if in_radial_band and small_phase_err and small_omega_err:
                    u_t = 0.0

            u_t = clamp(u_t, -U_MAX, U_MAX)

        # Apply exogenous factor + control to loads
        total_factor = factor + u_t
        total_factor = max(0.65, total_factor)  # protect against negative / unrealistic scaling

        net.load["p_mw"] = base_p * total_factor

        # Simulate
        v_mean, coherence, v_std = compute_state_from_net(net)

        v_hist.append(v_mean)
        coh_hist.append(coherence)
        vstd_hist.append(v_std)

        # Switch signal = local slope of v_mean
        if len(v_hist) > 2:
            sw = float(np.gradient(v_hist)[-1])
        else:
            sw = 0.0
        sw_hist.append(sw)

        # Polar features
        r_t, theta_t = radial_phase_features(coherence, sw, COH_CENTER, SW_CENTER)
        r_hist.append(r_t)
        theta_hist.append(theta_t)

        # Angular velocity
        if prev_theta is None:
            omega_t = 0.0
        else:
            omega_t = wrap_angle(theta_t - prev_theta)
        omega_hist.append(omega_t)
        prev_theta = theta_t

        u_hist.append(u_t)

        # Classical collapse event
        if classical_event is None and v_mean < V_CLASSICAL:
            classical_event = t

    return {
        "v": np.array(v_hist),
        "coh": np.array(coh_hist),
        "sw": np.array(sw_hist),
        "vstd": np.array(vstd_hist),
        "r": np.array(r_hist),
        "theta": np.array(theta_hist),
        "omega": np.array(omega_hist),
        "u": np.array(u_hist),
        "classical_event": classical_event,
    }


# ============================================================
# 5. Run experiments
# ============================================================

baseline = run_simulation(controlled=False)
controlled = run_simulation(controlled=True)

t = np.arange(TIME_STEPS)


# ============================================================
# 6. Reporting
# ============================================================

baseline_mean_r = float(np.mean(baseline["r"]))
controlled_mean_r = float(np.mean(controlled["r"]))

baseline_max_r = float(np.max(baseline["r"]))
controlled_max_r = float(np.max(controlled["r"]))

baseline_mean_coh = float(np.mean(baseline["coh"]))
controlled_mean_coh = float(np.mean(controlled["coh"]))

baseline_escape_count = int(np.sum((baseline["r"] < R_MIN) | (baseline["r"] > R_MAX)))
controlled_escape_count = int(np.sum((controlled["r"] < R_MIN) | (controlled["r"] > R_MAX)))

control_activation_count = int(np.sum(np.abs(controlled["u"]) > 1e-9))
mean_control = float(np.mean(controlled["u"]))
max_control = float(np.max(np.abs(controlled["u"])))


report_lines = [
    "===== NEXAH V14 HYBRID CONTROLLER REPORT =====",
    "",
    f"Band target radius: {R_TARGET:.6f}",
    f"Band interval: [{R_MIN:.6f}, {R_MAX:.6f}]",
    f"Theta reference: {THETA_REF:.6f} rad",
    f"Phase tolerance: {PHASE_TOL:.6f} rad",
    f"Omega reference: {OMEGA_REF:.6f}",
    f"Omega tolerance: {OMEGA_TOL:.6f}",
    "",
    f"Baseline mean radius: {baseline_mean_r:.6f}",
    f"Controlled mean radius: {controlled_mean_r:.6f}",
    "",
    f"Baseline max radius: {baseline_max_r:.6f}",
    f"Controlled max radius: {controlled_max_r:.6f}",
    "",
    f"Baseline mean coherence: {baseline_mean_coh:.6f}",
    f"Controlled mean coherence: {controlled_mean_coh:.6f}",
    "",
    f"Baseline first classical event: {baseline['classical_event']}",
    f"Controlled first classical event: {controlled['classical_event']}",
    "",
    f"Baseline escape count: {baseline_escape_count}",
    f"Controlled escape count: {controlled_escape_count}",
    "",
    f"Control activation count: {control_activation_count}",
    f"Mean control signal: {mean_control:.6f}",
    f"Max |control signal|: {max_control:.6f}",
    "",
]

# Simple interpretation
if controlled_mean_coh > baseline_mean_coh:
    report_lines.append("Mean coherence improved.")
else:
    report_lines.append("Mean coherence did not improve.")

if controlled_max_r < baseline_max_r:
    report_lines.append("Maximum orbit excursion improved.")
else:
    report_lines.append("Maximum orbit excursion did not improve.")

if controlled_escape_count < baseline_escape_count:
    report_lines.append("Escape count reduced.")
else:
    report_lines.append("Escape count did not reduce.")

if (
    controlled_mean_coh > baseline_mean_coh
    and controlled_max_r < baseline_max_r
    and controlled_escape_count < baseline_escape_count
):
    report_lines.append("→ Hybrid band-phase-velocity control shows net improvement.")
else:
    report_lines.append("→ Hybrid controller is informative, but needs further tuning.")

report_text = "\n".join(report_lines)
print(report_text)

(BASE_DIR / "ieee57_v14_hybrid_report.txt").write_text(report_text, encoding="utf-8")


# ============================================================
# 7. Plot: time series
# ============================================================

fig, ax = plt.subplots(5, 1, figsize=(14, 16), sharex=True)

ax[0].plot(t, baseline["v"], label="Baseline", alpha=0.45)
ax[0].plot(t, controlled["v"], label="Controlled")
ax[0].axhline(V_CLASSICAL, ls="--", color="gray", alpha=0.8, label="Classical threshold")
ax[0].set_ylabel("Voltage mean")
ax[0].set_title("NEXAH v14 — Hybrid Band + Phase + Velocity Control (Time Series)")
ax[0].legend(loc="best")
ax[0].grid(True, alpha=0.3)

ax[1].plot(t, baseline["coh"], label="Baseline", alpha=0.45)
ax[1].plot(t, controlled["coh"], label="Controlled")
ax[1].set_ylabel("Coherence")
ax[1].grid(True, alpha=0.3)

ax[2].plot(t, baseline["sw"], label="Baseline", alpha=0.45)
ax[2].plot(t, controlled["sw"], label="Controlled")
ax[2].axhline(SW_CENTER, ls="--", color="gray", alpha=0.6)
ax[2].set_ylabel("Switch")
ax[2].grid(True, alpha=0.3)

ax[3].plot(t, controlled["r"], color="purple", label="Controlled radius")
ax[3].axhline(R_MIN, ls="--", color="gray", alpha=0.7, label="Band min/max")
ax[3].axhline(R_MAX, ls="--", color="gray", alpha=0.7)
ax[3].axhline(R_TARGET, ls=":", color="black", alpha=0.8, label="Target radius")
ax[3].set_ylabel("Radius")
ax[3].legend(loc="best")
ax[3].grid(True, alpha=0.3)

ax[4].plot(t, controlled["u"], color="black", label="Control signal")
ax[4].fill_between(t, controlled["u"], 0, where=np.abs(controlled["u"]) > 1e-9, alpha=0.2, color="gray", label="Active control")
ax[4].set_ylabel("u(t)")
ax[4].set_xlabel("Time step")
ax[4].legend(loc="best")
ax[4].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(BASE_DIR / "ieee57_v14_hybrid_timeseries.png", dpi=200)
plt.close(fig)


# ============================================================
# 8. Plot: phase space
# ============================================================

fig, ax = plt.subplots(figsize=(12, 9))

ax.plot(baseline["coh"], baseline["sw"], alpha=0.35, lw=2, label="Baseline trajectory")
ax.plot(controlled["coh"], controlled["sw"], lw=2.2, label="Controlled trajectory")

# Escape markers
baseline_escape = (baseline["r"] < R_MIN) | (baseline["r"] > R_MAX)
controlled_escape = (controlled["r"] < R_MIN) | (controlled["r"] > R_MAX)

ax.scatter(
    baseline["coh"][baseline_escape],
    baseline["sw"][baseline_escape],
    s=80,
    facecolors="none",
    edgecolors="C0",
    linewidths=1.8,
    label="Baseline escape region",
)
ax.scatter(
    controlled["coh"][controlled_escape],
    controlled["sw"][controlled_escape],
    s=80,
    facecolors="none",
    edgecolors="C1",
    linewidths=1.8,
    label="Controlled escape region",
)

# Stability center
ax.scatter([COH_CENTER], [SW_CENTER], s=320, marker="*", color="gold", label="Stability center")

# Start / end
ax.scatter([baseline["coh"][0]], [baseline["sw"][0]], s=160, color="green", label="Start")
ax.scatter([baseline["coh"][-1]], [baseline["sw"][-1]], s=160, color="red", label="Baseline end")
ax.scatter([controlled["coh"][-1]], [controlled["sw"][-1]], s=160, color="purple", label="Controlled end")

ax.axhline(SW_CENTER, color="gray", alpha=0.35, ls="--")
ax.axvline(COH_CENTER, color="gray", alpha=0.35, ls="--")

ax.set_xlabel("Coherence")
ax.set_ylabel("Switch signal")
ax.set_title("NEXAH v14 — Hybrid Controller (Phase Space)")
ax.legend(loc="best")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(BASE_DIR / "ieee57_v14_hybrid_phase.png", dpi=200)
plt.close(fig)


# ============================================================
# 9. Plot: polar
# ============================================================

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection="polar")

ax.plot(baseline["theta"], baseline["r"], alpha=0.30, lw=2.0, label="Baseline")
ax.plot(controlled["theta"], controlled["r"], lw=2.2, label="Controlled")

# Ring targets
theta_full = np.linspace(0, 2 * np.pi, 600)
ax.plot(theta_full, np.full_like(theta_full, R_TARGET), ls=":", lw=2, color="black", label="Target ring")
ax.plot(theta_full, np.full_like(theta_full, R_MIN), ls="--", lw=1.4, color="gray", alpha=0.8, label="Band")
ax.plot(theta_full, np.full_like(theta_full, R_MAX), ls="--", lw=1.4, color="gray", alpha=0.8)

# Escape markers
ax.scatter(
    baseline["theta"][baseline_escape],
    baseline["r"][baseline_escape],
    s=120,
    facecolors="none",
    edgecolors="C0",
    linewidths=1.6,
)
ax.scatter(
    controlled["theta"][controlled_escape],
    controlled["r"][controlled_escape],
    s=120,
    facecolors="none",
    edgecolors="C1",
    linewidths=1.6,
)

# Start / end
ax.scatter([baseline["theta"][0]], [baseline["r"][0]], s=160, color="green", label="Start")
ax.scatter([baseline["theta"][-1]], [baseline["r"][-1]], s=160, color="red", label="Baseline end")
ax.scatter([controlled["theta"][-1]], [controlled["r"][-1]], s=160, color="purple", label="Controlled end")

# Reference angle
ax.plot([THETA_REF, THETA_REF], [0, max(np.max(baseline["r"]), np.max(controlled["r"]))], ls="--", color="black", alpha=0.7, label="Theta ref")

ax.set_title("NEXAH v14 — Hybrid Controller (Polar)", pad=24)
ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.10))

plt.tight_layout()
plt.savefig(BASE_DIR / "ieee57_v14_hybrid_polar.png", dpi=200)
plt.close(fig)
