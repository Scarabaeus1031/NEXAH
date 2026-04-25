# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v29_yugo_iota_predictor.py
#
# v29: YUGO / Greyspace IOTA Predictor
#
# Goal:
#   Detect whether IOTA events are preceded by a measurable "Greyspace" condition:
#
#   - high YUGO angular instability
#   - high switching density
#   - rising radial derivative pressure
#
# This is NOT yet control.
# This is a pre-IOTA warning layer.

import os
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

np.random.seed(42)

N = 1000
TRANSITION_POINT = 600

OUTPUT_DIR = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUT_SCORE_TIME = os.path.join(OUTPUT_DIR, "v29_greyspace_iota_score_time.png")
OUT_PHASE_MAP = os.path.join(OUTPUT_DIR, "v29_greyspace_phase_map.png")
OUT_WARNING_WINDOWS = os.path.join(OUTPUT_DIR, "v29_pre_iota_warning_windows.png")

SPIKE_THRESHOLD = 10.0
WINDOW_SWITCH = 20
WINDOW_SCORE = 25

STATE_THETA = 0
STATE_TAO = 1
STATE_DAO = 2
STATE_IOTA = 3

# --------------------------------------------------
# SIGNAL
# --------------------------------------------------

t = np.arange(N)

signal = np.sin(0.2 * t)
noise = np.random.normal(0, 0.8, size=N)
signal[TRANSITION_POINT:] = np.sin(0.2 * t[TRANSITION_POINT:]) + noise[TRANSITION_POINT:]

# --------------------------------------------------
# PHASE SPACE
# --------------------------------------------------

theta = np.unwrap(np.angle(signal + 1j * np.roll(signal, 1)))
r = np.abs(signal)

dtheta = np.gradient(theta)
dr = np.gradient(r)

eps = 1e-8
dr_dtheta = np.divide(dr, dtheta + eps)

flow_norm = np.sqrt(dtheta**2 + dr**2) + eps
yugo_theta = dtheta / flow_norm
yugo_r = dr / flow_norm
yugo_angle = np.arctan2(yugo_r, yugo_theta)

# --------------------------------------------------
# SWITCHING DENSITY
# --------------------------------------------------

switching = np.abs(np.diff(np.sign(dr_dtheta), prepend=0))
switching_density = np.convolve(
    switching,
    np.ones(WINDOW_SWITCH) / WINDOW_SWITCH,
    mode="same"
)

# --------------------------------------------------
# IOTA EVENTS
# --------------------------------------------------

iota_mask = np.abs(dr_dtheta) > SPIKE_THRESHOLD
iota_idx = np.where(iota_mask)[0]

# --------------------------------------------------
# GREYSPACE / PRE-IOTA SCORE
# --------------------------------------------------
# Components:
#   1. local YUGO angle volatility
#   2. switching density
#   3. radial pressure abs(dr)
#
# All normalized to [0,1].

def rolling_std(x, window):
    out = np.zeros_like(x)
    half = window // 2

    for i in range(len(x)):
        s = max(0, i - half)
        e = min(len(x), i + half + 1)
        out[i] = np.std(x[s:e])

    return out


def normalize(x):
    x = np.asarray(x)
    lo = np.nanmin(x)
    hi = np.nanmax(x)
    if hi - lo < 1e-12:
        return np.zeros_like(x)
    return (x - lo) / (hi - lo)


yugo_volatility = rolling_std(yugo_angle, WINDOW_SCORE)
radial_pressure = np.abs(dr)

Y = normalize(yugo_volatility)
S = normalize(switching_density)
R = normalize(radial_pressure)

# weighted score
greyspace_score = 0.45 * Y + 0.35 * S + 0.20 * R

# prevent direct IOTA points from defining "pre" score
pre_iota_score = greyspace_score.copy()
pre_iota_score[iota_mask] = np.nan

# adaptive warning threshold
valid = pre_iota_score[~np.isnan(pre_iota_score)]
warning_threshold = np.percentile(valid, 92)

warning_mask = pre_iota_score > warning_threshold
warning_idx = np.where(warning_mask)[0]

# --------------------------------------------------
# STATE MODEL FOR VISUAL CONTEXT
# --------------------------------------------------

states = np.zeros(N, dtype=int)

for i in range(N):
    if iota_mask[i]:
        states[i] = STATE_IOTA
    elif greyspace_score[i] > warning_threshold:
        states[i] = STATE_DAO
    elif switching_density[i] > 0.3:
        states[i] = STATE_TAO
    else:
        states[i] = STATE_THETA

# --------------------------------------------------
# PLOT 1 — SCORE OVER TIME
# --------------------------------------------------

plt.figure(figsize=(13, 5))

plt.plot(t, greyspace_score, color="purple", linewidth=1.5, label="Greyspace / pre-IOTA score")
plt.axhline(warning_threshold, color="orange", linestyle="--", label="warning threshold")
plt.axvline(TRANSITION_POINT, color="black", linestyle="--", label="true transition")

plt.scatter(
    warning_idx,
    greyspace_score[warning_idx],
    color="orange",
    s=18,
    label="warning points",
    zorder=4,
)

plt.scatter(
    iota_idx,
    greyspace_score[iota_idx],
    color="red",
    s=55,
    label="IOTA events",
    zorder=5,
)

plt.xlabel("time")
plt.ylabel("score")
plt.title("V29 — Greyspace Score as Pre-IOTA Warning Signal")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT_SCORE_TIME, dpi=180)
plt.close()

# --------------------------------------------------
# PLOT 2 — PHASE MAP
# --------------------------------------------------

plt.figure(figsize=(12, 7))

plt.scatter(theta, r, s=8, alpha=0.12, color="gray", label="all states")

plt.scatter(
    theta[warning_idx],
    r[warning_idx],
    s=24,
    color="orange",
    alpha=0.8,
    label="pre-IOTA warning",
)

plt.scatter(
    theta[iota_idx],
    r[iota_idx],
    s=70,
    color="red",
    edgecolor="black",
    linewidth=0.7,
    label="IOTA",
)

plt.axvline(theta[TRANSITION_POINT], color="black", linestyle="--", label="true transition")

plt.xlabel("theta (unwrapped phase)")
plt.ylabel("r")
plt.title("V29 — Greyspace Warning Regions in Phase Space")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT_PHASE_MAP, dpi=180)
plt.close()

# --------------------------------------------------
# PLOT 3 — LOCAL PRE-IOTA WINDOWS
# --------------------------------------------------

plt.figure(figsize=(13, 6))

for j, idx in enumerate(iota_idx):
    start = max(0, idx - 50)
    end = min(N, idx + 15)

    local_t = t[start:end]
    local_score = greyspace_score[start:end]

    plt.plot(
        local_t - idx,
        local_score,
        alpha=0.75,
        linewidth=1.7,
        label="pre-IOTA window" if j == 0 else None,
    )

plt.axvline(0, color="red", linestyle="--", label="IOTA moment")
plt.axhline(warning_threshold, color="orange", linestyle="--", label="warning threshold")

plt.xlabel("time relative to IOTA")
plt.ylabel("Greyspace score")
plt.title("V29 — Score Build-Up Before IOTA Events")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT_WARNING_WINDOWS, dpi=180)
plt.close()

# --------------------------------------------------
# METRICS
# --------------------------------------------------

lead_times = []

for idx in iota_idx:
    prior = warning_idx[warning_idx < idx]
    prior = prior[prior >= idx - 80]

    if len(prior) > 0:
        lead_times.append(idx - prior[-1])

lead_times = np.array(lead_times)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n--- V29 RESULTS ---")
print(f"Total points: {N}")
print(f"True transition index: {TRANSITION_POINT}")
print(f"IOTA events: {len(iota_idx)}")
print(f"Warning points: {len(warning_idx)}")
print(f"Warning threshold: {warning_threshold:.3f}")

print("\nIOTA indices:")
print(iota_idx.tolist())

if len(lead_times) > 0:
    print("\nPre-IOTA lead times:")
    print(lead_times.tolist())
    print(f"Mean lead time: {np.mean(lead_times):.2f}")
    print(f"Median lead time: {np.median(lead_times):.2f}")
else:
    print("\nNo pre-IOTA warning hits found within window.")

print("\nSaved:")
print(OUT_SCORE_TIME)
print(OUT_PHASE_MAP)
print(OUT_WARNING_WINDOWS)
