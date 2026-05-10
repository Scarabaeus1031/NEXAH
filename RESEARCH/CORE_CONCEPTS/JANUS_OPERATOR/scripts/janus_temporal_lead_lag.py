# janus_temporal_lead_lag.py
#
# EXPERIMENT 5
# Temporal Lead/Lag Analysis:
# JANUS coherence vs curvature
#
# Goal:
# Determine whether JANUS changes
# precede or follow curvature reconfiguration.
#
# Outputs:
# - cross_correlation_vs_lag.png
# - rolling_correlation.png
# - event_alignment.png
#
# Author: Thomas Hofmann + ChatGPT
# NEXAH / JANUS_OPERATOR


import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
from scipy.stats import pearsonr


# ============================================================
# CONFIG
# ============================================================

OUTPUT_DIR = "EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_LAG = 200
ROLLING_WINDOW = 500


# ============================================================
# LOAD DATA
# ============================================================

# IMPORTANT:
# Replace these with your actual arrays if needed.

# expected:
# janus_coherence -> shape (N,)
# curvature       -> shape (N,)

# Example:
# from janus_core import janus_coherence
# from curvature_core import curvature

# ------------------------------------------------------------
# TEMPORARY PLACEHOLDER
# ------------------------------------------------------------

# REMOVE THIS IF ARRAYS ALREADY EXIST
np.random.seed(0)

N = 8500
t = np.arange(N)

janus_coherence = (
    0.75
    + 0.08 * np.sin(0.03 * t)
    + 0.03 * np.sin(0.17 * t)
)

curvature = (
    0.10
    + 0.04 * np.sin(0.03 * (t - 30))
    + 0.02 * np.sin(0.15 * (t - 20))
)

# emulate anti-correlation
curvature = curvature - 0.10 * (janus_coherence - np.mean(janus_coherence))


# ============================================================
# PREPROCESS
# ============================================================

# log curvature
curv_log = np.log10(np.abs(curvature) + 1e-8)

# normalize
janus_z = (janus_coherence - np.mean(janus_coherence)) / np.std(janus_coherence)
curv_z = (curv_log - np.mean(curv_log)) / np.std(curv_log)


# ============================================================
# CROSS CORRELATION
# ============================================================

corr_full = correlate(janus_z, curv_z, mode="full")
lags_full = np.arange(-len(janus_z) + 1, len(janus_z))

# normalize
corr_full = corr_full / len(janus_z)

# restrict lag range
mask = (lags_full >= -MAX_LAG) & (lags_full <= MAX_LAG)

lags = lags_full[mask]
corrs = corr_full[mask]

peak_idx = np.argmax(np.abs(corrs))
peak_lag = lags[peak_idx]
peak_corr = corrs[peak_idx]

print("\n================================================")
print("TEMPORAL LEAD/LAG ANALYSIS")
print("================================================")
print(f"peak lag: {peak_lag}")
print(f"peak correlation: {peak_corr:.6f}")

if peak_lag > 0:
    print("INTERPRETATION:")
    print("JANUS leads curvature")
elif peak_lag < 0:
    print("INTERPRETATION:")
    print("Curvature leads JANUS")
else:
    print("INTERPRETATION:")
    print("Simultaneous coupling")


# ============================================================
# VISUAL 1
# Cross-correlation vs lag
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(lags, corrs, lw=2)

plt.axvline(0, color="black", ls="--", alpha=0.5)
plt.axvline(peak_lag, color="red", ls="--", alpha=0.7)

plt.title(
    f"JANUS vs Curvature — Temporal Lead/Lag\n"
    f"peak lag = {peak_lag}, peak corr = {peak_corr:.4f}"
)

plt.xlabel("lag")
plt.ylabel("cross correlation")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "cross_correlation_vs_lag.png"),
    dpi=300
)

plt.close()


# ============================================================
# ROLLING CORRELATION
# ============================================================

rolling_corr = []
rolling_time = []

for i in range(ROLLING_WINDOW, len(janus_z)):

    j_seg = janus_z[i - ROLLING_WINDOW:i]
    c_seg = curv_z[i - ROLLING_WINDOW:i]

    r, _ = pearsonr(j_seg, c_seg)

    rolling_corr.append(r)
    rolling_time.append(i)

rolling_corr = np.array(rolling_corr)
rolling_time = np.array(rolling_time)

print("\nRolling correlation:")
print(f"mean: {np.mean(rolling_corr):.6f}")
print(f"std : {np.std(rolling_corr):.6f}")


# ============================================================
# VISUAL 2
# Rolling correlation
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(rolling_time, rolling_corr, lw=1.5)

plt.axhline(0, color="black", ls="--", alpha=0.5)

plt.title(
    f"Rolling JANUS–Curvature Correlation\n"
    f"window = {ROLLING_WINDOW}"
)

plt.xlabel("time")
plt.ylabel("rolling Pearson r")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "rolling_correlation.png"),
    dpi=300
)

plt.close()


# ============================================================
# EVENT ALIGNMENT
# ============================================================

# low Janus events
janus_thresh = np.percentile(janus_coherence, 10)

# high curvature events
curv_thresh = np.percentile(curv_log, 90)

janus_events = janus_coherence < janus_thresh
curv_events = curv_log > curv_thresh

# ============================================================
# VISUAL 3
# Event overlays
# ============================================================

plt.figure(figsize=(14, 5))

plt.plot(
    janus_coherence,
    label="JANUS coherence",
    alpha=0.8
)

plt.plot(
    (curv_log - np.min(curv_log))
    / (np.max(curv_log) - np.min(curv_log)),
    label="normalized log curvature",
    alpha=0.8
)

# overlay events
plt.scatter(
    np.where(janus_events)[0],
    janus_coherence[janus_events],
    s=10,
    label="low Janus events"
)

plt.scatter(
    np.where(curv_events)[0],
    janus_coherence[curv_events],
    s=10,
    label="high curvature events"
)

plt.title("Event Alignment: JANUS vs Curvature")

plt.xlabel("time")
plt.ylabel("value")

plt.legend()

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "event_alignment.png"),
    dpi=300
)

plt.close()


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n================================================")
print("JANUS temporal experiment complete")
print("================================================")

print(f"samples: {len(janus_coherence)}")
print(f"peak lag: {peak_lag}")
print(f"peak correlation: {peak_corr:.6f}")

print(f"rolling corr mean: {np.mean(rolling_corr):.6f}")
print(f"rolling corr std : {np.std(rolling_corr):.6f}")

print("\noutputs saved to:")
print(os.path.abspath(OUTPUT_DIR))
