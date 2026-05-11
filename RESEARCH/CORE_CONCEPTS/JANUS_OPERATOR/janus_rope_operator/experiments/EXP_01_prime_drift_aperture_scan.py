# ============================================================
# EXP_01_prime_drift_aperture_scan.py
# JANUS Rope Operator — Prime Drift Aperture Scan
#
# Purpose:
# Compare harmonic synchronization vs prime-drift timing
# and measure whether moving apertures survive longer.
#
# Status:
# Exploratory symbolic experiment
#
# Author:
# Thomas Hofmann / NEXAH
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

T_MAX = 80
DT = 0.01

times = np.arange(0, T_MAX, DT)

# aperture threshold
APERTURE_THRESHOLD = 0.22

# ------------------------------------------------------------
# HARMONIC SYSTEM
# ------------------------------------------------------------

harmonic_freqs = [1, 2, 4, 8]

# ------------------------------------------------------------
# PRIME DRIFT SYSTEM
# ------------------------------------------------------------

prime_freqs = [2, 3, 5, 7]

prime_offsets = [
    np.pi,
    (1 + np.sqrt(5)) / 2,     # phi
    np.sqrt(2),
    np.pi / np.sqrt(2)
]

# ------------------------------------------------------------
# ROPE GENERATOR
# ------------------------------------------------------------

def generate_rope_field(freqs, offsets=None):

    ropes = []

    for i, f in enumerate(freqs):

        if offsets is None:
            phase = 0.0
        else:
            phase = offsets[i]

        rope = np.sin(f * times + phase)

        ropes.append(rope)

    return np.array(ropes)

# ------------------------------------------------------------
# APERTURE SCORE
# ------------------------------------------------------------

def aperture_score(ropes):

    # pairwise distance field
    distances = []

    n = len(ropes)

    for i in range(n):
        for j in range(i + 1, n):

            d = np.abs(ropes[i] - ropes[j])

            distances.append(d)

    distances = np.array(distances)

    # small distance = rope overlap
    # large distance = aperture opening

    score = np.mean(distances, axis=0)

    return score

# ------------------------------------------------------------
# APERTURE EVENTS
# ------------------------------------------------------------

def detect_apertures(score):

    return score > APERTURE_THRESHOLD

# ------------------------------------------------------------
# GENERATE SYSTEMS
# ------------------------------------------------------------

harmonic_ropes = generate_rope_field(harmonic_freqs)

prime_ropes = generate_rope_field(
    prime_freqs,
    offsets=prime_offsets
)

harmonic_aperture = aperture_score(harmonic_ropes)
prime_aperture = aperture_score(prime_ropes)

harmonic_events = detect_apertures(harmonic_aperture)
prime_events = detect_apertures(prime_aperture)

# ------------------------------------------------------------
# STATS
# ------------------------------------------------------------

harmonic_gate_count = np.sum(harmonic_events)
prime_gate_count = np.sum(prime_events)

harmonic_mean = np.mean(harmonic_aperture)
prime_mean = np.mean(prime_aperture)

print("\n==============================")
print("EXP_01 — PRIME DRIFT APERTURE SCAN")
print("==============================")

print("\nHARMONIC SYSTEM")
print("------------------------------")
print(f"gate count: {harmonic_gate_count}")
print(f"mean aperture score: {harmonic_mean:.6f}")

print("\nPRIME DRIFT SYSTEM")
print("------------------------------")
print(f"gate count: {prime_gate_count}")
print(f"mean aperture score: {prime_mean:.6f}")

# ------------------------------------------------------------
# PLOT 1 — ROPE OVERLAY
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 6))

for rope in harmonic_ropes:
    ax.plot(times, rope, alpha=0.7)

ax.set_title("Harmonic Rope System")
ax.set_xlabel("time")
ax.set_ylabel("amplitude")

plt.tight_layout()
plt.savefig("exp01_harmonic_ropes.png", dpi=300)

# ------------------------------------------------------------
# PLOT 2 — PRIME DRIFT ROPES
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 6))

for rope in prime_ropes:
    ax.plot(times, rope, alpha=0.7)

ax.set_title("Prime Drift Rope System")
ax.set_xlabel("time")
ax.set_ylabel("amplitude")

plt.tight_layout()
plt.savefig("exp01_prime_drift_ropes.png", dpi=300)

# ------------------------------------------------------------
# PLOT 3 — APERTURE COMPARISON
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    times,
    harmonic_aperture,
    label="harmonic",
    linewidth=2
)

ax.plot(
    times,
    prime_aperture,
    label="prime drift",
    linewidth=2
)

ax.axhline(
    APERTURE_THRESHOLD,
    color="red",
    linestyle="--",
    label="threshold"
)

ax.set_title("Aperture Score Comparison")
ax.set_xlabel("time")
ax.set_ylabel("aperture score")

ax.legend()

plt.tight_layout()
plt.savefig("exp01_aperture_comparison.png", dpi=300)

# ------------------------------------------------------------
# PLOT 4 — APERTURE EVENTS
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 4))

ax.scatter(
    times[harmonic_events],
    np.ones(np.sum(harmonic_events)),
    s=6,
    label="harmonic"
)

ax.scatter(
    times[prime_events],
    np.zeros(np.sum(prime_events)),
    s=6,
    label="prime drift"
)

ax.set_title("Detected Aperture Events")
ax.set_xlabel("time")

ax.set_yticks([0, 1])
ax.set_yticklabels([
    "prime drift",
    "harmonic"
])

ax.legend()

plt.tight_layout()
plt.savefig("exp01_aperture_events.png", dpi=300)

# ------------------------------------------------------------
# PLOT 5 — PHASE SPACE
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

ax.plot(
    prime_ropes[0],
    prime_ropes[1],
    linewidth=0.5,
    alpha=0.8,
    label="prime drift"
)

ax.plot(
    harmonic_ropes[0],
    harmonic_ropes[1],
    linewidth=0.5,
    alpha=0.8,
    label="harmonic"
)

ax.set_title("Rope Phase Geometry")
ax.set_xlabel("rope 1")
ax.set_ylabel("rope 2")

ax.legend()

plt.tight_layout()
plt.savefig("exp01_phase_geometry.png", dpi=300)

# ------------------------------------------------------------
# FINAL
# ------------------------------------------------------------

print("\nvisuals saved:")
print("------------------------------")

print("exp01_harmonic_ropes.png")
print("exp01_prime_drift_ropes.png")
print("exp01_aperture_comparison.png")
print("exp01_aperture_events.png")
print("exp01_phase_geometry.png")

print("\nDONE.")
