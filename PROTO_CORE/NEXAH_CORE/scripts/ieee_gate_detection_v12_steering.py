# NEXAH_CORE/scripts/ieee_gate_detection_v12_control_steering.py
#
# v12: Simple Control / Steering Layer
#
# Goal:
# Use the v10/v11 idea operationally:
#
#   1. Build a gate-risk field in (r, theta)
#   2. Detect when the system enters a high-risk region
#   3. Apply a small steering / damping control
#   4. Compare uncontrolled vs controlled dynamics
#
# This is NOT a validated controller.
# It is a prototype showing how NEXAH can move from:
#
#   detection -> field map -> steering attempt

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import entropy

np.random.seed(42)

OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v12_control_steering.png"


# --------------------------------------------------
# 1. SIGNAL GENERATION
# --------------------------------------------------
def generate_uncontrolled_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            x[i] = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            x[i] = np.random.normal(0, 1.0)

    return x


# --------------------------------------------------
# 2. COHERENCE
# --------------------------------------------------
def compute_coherence(x, window=20, max_lag=5):
    C = np.zeros(len(x))

    for i in range(window, len(x)):
        seg = x[i - window:i]
        vals = []

        for lag in range(1, max_lag + 1):
            a = seg[:-lag]
            b = seg[lag:]

            if np.std(a) > 1e-12 and np.std(b) > 1e-12:
                vals.append(abs(np.corrcoef(a, b)[0, 1]))

        C[i] = np.mean(vals) if vals else 0.0

    return C


# --------------------------------------------------
# 3. ENTROPY
# --------------------------------------------------
def compute_entropy(x, window=40):
    S = np.zeros(len(x))

    for i in range(window, len(x)):
        seg = x[i - window:i]
        _, pxx = welch(seg, nperseg=len(seg))

        pxx = pxx + 1e-12
        pxx = pxx / np.sum(pxx)

        S[i] = entropy(pxx)

    return S


# --------------------------------------------------
# 4. GEOMETRY
# --------------------------------------------------
def compute_geometry(t, x, window=30):
    dx = np.gradient(x, t)
    G = np.zeros(len(x))

    for i in range(window, len(x)):
        X = np.column_stack((x[i - window:i], dx[i - window:i]))
        cov = np.cov(X.T)

        eigvals = np.maximum(np.linalg.eigvalsh(cov), 1e-12)
        G[i] = np.sqrt(np.prod(eigvals))

    return dx, G


# --------------------------------------------------
# 5. GATE MASK
# --------------------------------------------------
def compute_gate_mask(C, S, G):
    C_thr = np.percentile(C[C > 0], 15)
    S_thr = np.percentile(S[S > 0], 80)
    G_thr = np.percentile(G[G > 0], 80)

    mask = (C < C_thr) & (S > S_thr) & (G > G_thr)

    return mask, C_thr, S_thr, G_thr


# --------------------------------------------------
# 6. PHASE + RADIUS
# --------------------------------------------------
def compute_phase_radius(t, x):
    dx = np.gradient(x, t)
    theta = np.arctan2(dx, x)
    r = np.sqrt(x**2 + dx**2)
    return dx, theta, r


# --------------------------------------------------
# 7. BUILD RISK FIELD
# --------------------------------------------------
def build_risk_field(theta, r, gate_mask, bins_theta=60, bins_r=40):
    valid = (~np.isnan(theta)) & (~np.isnan(r))

    theta_all = theta[valid]
    r_all = r[valid]

    theta_g = theta[valid & gate_mask]
    r_g = r[valid & gate_mask]

    theta_range = [-np.pi, np.pi]
    r_range = [0, np.max(r_all)]

    H_all, theta_edges, r_edges = np.histogram2d(
        theta_all,
        r_all,
        bins=[bins_theta, bins_r],
        range=[theta_range, r_range],
        density=False,
    )

    H_gates, _, _ = np.histogram2d(
        theta_g,
        r_g,
        bins=[bins_theta, bins_r],
        range=[theta_range, r_range],
        density=False,
    )

    risk = H_gates / (H_all + 1e-8)

    return risk, theta_edges, r_edges


# --------------------------------------------------
# 8. RISK LOOKUP
# --------------------------------------------------
def lookup_risk(theta_value, r_value, risk, theta_edges, r_edges):
    ti = np.searchsorted(theta_edges, theta_value, side="right") - 1
    ri = np.searchsorted(r_edges, r_value, side="right") - 1

    ti = np.clip(ti, 0, risk.shape[0] - 1)
    ri = np.clip(ri, 0, risk.shape[1] - 1)

    return risk[ti, ri]


# --------------------------------------------------
# 9. CONTROLLED SIGNAL
# --------------------------------------------------
def generate_controlled_signal(t, risk, theta_edges, r_edges, risk_threshold=0.35, damping=0.45):
    x = np.zeros_like(t)
    control = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            raw = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            raw = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            raw = np.random.normal(0, 1.0)

        if i < 3:
            x[i] = raw
            continue

        local_dx = (x[i - 1] - x[i - 2]) / (t[i - 1] - t[i - 2])
        local_theta = np.arctan2(local_dx, x[i - 1])
        local_r = np.sqrt(x[i - 1] ** 2 + local_dx**2)

        local_risk = lookup_risk(local_theta, local_r, risk, theta_edges, r_edges)

        if local_risk > risk_threshold:
            control[i] = damping
            x[i] = (1.0 - damping) * raw + damping * x[i - 1]
        else:
            x[i] = raw

    return x, control


# --------------------------------------------------
# 10. CLUSTER GATES
# --------------------------------------------------
def cluster_gates(mask, min_length=10, max_gap=8):
    clusters = []
    start = None
    gap_count = 0

    for i, val in enumerate(mask):
        if val:
            if start is None:
                start = i
            gap_count = 0
        else:
            if start is not None:
                gap_count += 1

                if gap_count > max_gap:
                    end = i - gap_count
                    if end - start >= min_length:
                        clusters.append((start, end))
                    start = None
                    gap_count = 0

    if start is not None:
        clusters.append((start, len(mask) - 1))

    return clusters


# --------------------------------------------------
# 11. PIPELINE
# --------------------------------------------------
t = np.linspace(0, 100, 1000)

x_un = generate_uncontrolled_signal(t)
dx_un, theta_un, r_un = compute_phase_radius(t, x_un)

C_un = compute_coherence(x_un)
S_un = compute_entropy(x_un)
_, G_un = compute_geometry(t, x_un)

gate_un, C_thr_un, S_thr_un, G_thr_un = compute_gate_mask(C_un, S_un, G_un)
zones_un = cluster_gates(gate_un)

risk, theta_edges, r_edges = build_risk_field(theta_un, r_un, gate_un)

np.random.seed(42)
x_ctrl, control = generate_controlled_signal(t, risk, theta_edges, r_edges)

dx_ctrl, theta_ctrl, r_ctrl = compute_phase_radius(t, x_ctrl)

C_ctrl = compute_coherence(x_ctrl)
S_ctrl = compute_entropy(x_ctrl)
_, G_ctrl = compute_geometry(t, x_ctrl)

gate_ctrl, C_thr_ctrl, S_thr_ctrl, G_thr_ctrl = compute_gate_mask(C_ctrl, S_ctrl, G_ctrl)
zones_ctrl = cluster_gates(gate_ctrl)


# --------------------------------------------------
# 12. SUMMARY METRICS
# --------------------------------------------------
def summarize(label, x, C, S, G, gate_mask, zones):
    gate_count = int(np.sum(gate_mask))
    zone_count = len(zones)
    mean_C = float(np.mean(C[C > 0]))
    mean_S = float(np.mean(S[S > 0]))
    mean_G = float(np.mean(G[G > 0]))
    max_amp = float(np.max(np.abs(x)))

    print(f"\n--- {label} ---")
    print(f"Gate samples: {gate_count}")
    print(f"Gate zones:   {zone_count}")
    print(f"Mean C:       {mean_C:.3f}")
    print(f"Mean S:       {mean_S:.3f}")
    print(f"Mean G:       {mean_G:.3f}")
    print(f"Max |x|:      {max_amp:.3f}")


# --------------------------------------------------
# 13. VISUALIZATION
# --------------------------------------------------
fig, axs = plt.subplots(5, 1, figsize=(14, 14), sharex=True)

axs[0].plot(t, x_un, label="uncontrolled")
axs[0].plot(t, x_ctrl, label="controlled", alpha=0.8)
axs[0].set_title("System Dynamics: uncontrolled vs controlled")
axs[0].legend()

axs[1].plot(t, C_un, label="C uncontrolled")
axs[1].plot(t, C_ctrl, label="C controlled", alpha=0.8)
axs[1].axhline(C_thr_un, linestyle="--", label="C threshold")
axs[1].set_title("Coherence")
axs[1].legend()

axs[2].plot(t, S_un, label="S uncontrolled")
axs[2].plot(t, S_ctrl, label="S controlled", alpha=0.8)
axs[2].axhline(S_thr_un, linestyle="--", label="S threshold")
axs[2].set_title("Spectral Entropy")
axs[2].legend()

axs[3].plot(t, G_un, label="G uncontrolled")
axs[3].plot(t, G_ctrl, label="G controlled", alpha=0.8)
axs[3].axhline(G_thr_un, linestyle="--", label="G threshold")
axs[3].set_title("Phase-Space Dispersion")
axs[3].legend()

axs[4].plot(t, control, label="control activation")
axs[4].set_title("Control Activation")
axs[4].set_ylim(-0.05, 1.05)
axs[4].legend()

for s, e in zones_un:
    s = min(s, len(t) - 1)
    e = min(e, len(t) - 1)
    for ax in axs:
        ax.axvspan(t[s], t[e], alpha=0.10)

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)


# --------------------------------------------------
# 14. RISK FIELD VISUAL
# --------------------------------------------------
RISK_OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v12_risk_field.png"

fig2, ax = plt.subplots(figsize=(8, 6))

im = ax.imshow(
    risk.T,
    origin="lower",
    aspect="auto",
    extent=[-np.pi, np.pi, r_edges[0], r_edges[-1]],
)

ax.set_title("Risk Field P(gate | r, theta)")
ax.set_xlabel("theta")
ax.set_ylabel("r")

plt.colorbar(im, ax=ax)
plt.tight_layout()
plt.savefig(RISK_OUTPUT_PATH, dpi=150)


# --------------------------------------------------
# 15. LOGGING
# --------------------------------------------------
print("\n--- NEXAH IEEE Gate Detection v12 ---")
summarize("Uncontrolled", x_un, C_un, S_un, G_un, gate_un, zones_un)
summarize("Controlled", x_ctrl, C_ctrl, S_ctrl, G_ctrl, gate_ctrl, zones_ctrl)

print(f"\nControl activations: {int(np.sum(control > 0))}")
print(f"Saved comparison to: {OUTPUT_PATH}")
print(f"Saved risk field to: {RISK_OUTPUT_PATH}")

plt.show()
