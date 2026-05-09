# EXPERIMENT 10 — JANUS ATTRACTOR MEMORY
## Goal
#Test whether JANUS coherence contains:

#- temporal persistence
#- memory traces
#- delayed self-similarity
#- attractor retention
#- recurrence structure

#The question is:

#> Does JANUS only react locally,
#> or does it preserve long-range dynamical memory?

#---

# Script

# EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/scripts/janus_attractor_memory.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import pdist, squareform
from scipy.signal import correlate

# ============================================================
# LORENZ SYSTEM
# ============================================================

def lorenz_step(state, sigma=10.0, rho=28.0, beta=8/3, dt=0.01):
    x, y, z = state

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z

    return np.array([
        x + dx * dt,
        y + dy * dt,
        z + dz * dt
    ])

def simulate_lorenz(n=14000):
    state = np.array([1.0, 1.0, 1.0])

    traj = np.zeros((n, 3))

    for i in range(n):
        state = lorenz_step(state)
        traj[i] = state

    return traj

# ============================================================
# JANUS COHERENCE
# ============================================================

def compute_janus(traj):

    velocity = np.gradient(traj[:, 0])
    acceleration = np.gradient(velocity)

    signal = (
        np.sin(velocity * 0.7)
        + np.cos(acceleration * 1.3)
    )

    signal = (signal - signal.min()) / (signal.max() - signal.min())

    return signal

# ============================================================
# RECURRENCE MATRIX
# ============================================================

def recurrence_matrix(signal, threshold=0.03):

    embedded = np.column_stack([
        signal[:-2],
        signal[1:-1],
        signal[2:]
    ])

    dist = squareform(pdist(embedded))

    recurrence = dist < threshold

    return recurrence.astype(float)

# ============================================================
# DELAYED SELF CORRELATION
# ============================================================

def delayed_correlation(signal, max_lag=1500):

    lags = np.arange(1, max_lag)

    corrs = []

    for lag in lags:

        a = signal[:-lag]
        b = signal[lag:]

        c = np.corrcoef(a, b)[0, 1]

        corrs.append(c)

    return lags, np.array(corrs)

# ============================================================
# MEMORY DECAY
# ============================================================

def memory_decay(signal, windows=[50,100,200,400,800]):

    means = []

    for w in windows:

        rolling = np.convolve(
            signal,
            np.ones(w)/w,
            mode='valid'
        )

        means.append(np.var(rolling))

    return windows, means

# ============================================================
# MAIN
# ============================================================

print("\n================================================")
print("JANUS ATTRACTOR MEMORY")
print("================================================")

traj = simulate_lorenz()

janus = compute_janus(traj)

janus_smooth = gaussian_filter1d(janus, sigma=3)

# ============================================================
# RECURRENCE
# ============================================================

print("Computing recurrence matrix...")

rec = recurrence_matrix(janus_smooth)

# ============================================================
# DELAYED CORRELATION
# ============================================================

print("Computing delayed correlations...")

lags, corrs = delayed_correlation(janus_smooth)

# ============================================================
# MEMORY DECAY
# ============================================================

windows, variances = memory_decay(janus_smooth)

# ============================================================
# VISUALIZATION 1
# ============================================================

plt.figure(figsize=(10, 10))

plt.imshow(
    rec,
    origin="lower",
    cmap="magma",
    aspect="auto"
)

plt.title("JANUS Recurrence Matrix")
plt.xlabel("time")
plt.ylabel("time")

plt.tight_layout()

plt.savefig(
    "EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/janus_recurrence_matrix.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUALIZATION 2
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    lags,
    corrs,
    lw=2
)

plt.axhline(
    0,
    color='black',
    linestyle='--'
)

plt.title("JANUS Delayed Self-Correlation")
plt.xlabel("lag")
plt.ylabel("correlation")

plt.tight_layout()

plt.savefig(
    "EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/janus_delayed_correlation.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUALIZATION 3
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    windows,
    variances,
    marker='o',
    lw=2
)

plt.title("JANUS Memory Persistence")
plt.xlabel("window size")
plt.ylabel("variance")

plt.tight_layout()

plt.savefig(
    "EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/janus_memory_decay.png",
    dpi=300
)

plt.close()

# ============================================================
# VISUALIZATION 4
# ============================================================

plt.figure(figsize=(16, 5))

plt.plot(
    janus_smooth[:4000],
    lw=1
)

plt.title("JANUS Memory Trace")
plt.xlabel("time")
plt.ylabel("JANUS coherence")

plt.tight_layout()

plt.savefig(
    "EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs/janus_memory_trace.png",
    dpi=300
)

plt.close()

# ============================================================
# SUMMARY
# ============================================================

peak_corr = np.max(corrs[10:])
peak_lag = lags[np.argmax(corrs[10:]) + 10]

print("\n================================================")
print("JANUS ATTRACTOR MEMORY")
print("================================================")

print(f"samples: {len(janus_smooth)}")
print(f"peak delayed corr: {peak_corr:.6f}")
print(f"peak lag: {peak_lag}")

print("\nmemory variance decay:")

for w, v in zip(windows, variances):
    print(f"window={w:4d} variance={v:.6f}")

print("\nINTERPRETATION:")

if peak_corr > 0.5:
    print("strong long-range temporal memory")
elif peak_corr > 0.2:
    print("moderate delayed recurrence structure")
else:
    print("weak temporal persistence")

print("\noutputs saved to:")
print("EXPERIMENTAL/BUILDER_LAB/JANUS_OPERATOR/outputs")

print("================================================")
```

---

# Outputs

```text
janus_recurrence_matrix.png
janus_delayed_correlation.png
janus_memory_decay.png
janus_memory_trace.png
```

---

# What this experiment tests

This experiment asks:

```text
Does JANUS contain persistent dynamical memory?
```

We test this via:

- recurrence geometry
- delayed self-correlation
- persistence decay
- attractor trace continuity

---

# Expected Interesting Behaviors

Possible findings:

```text
- recurrence stripes
- diagonal attractor bands
- long-range delayed peaks
- persistent memory corridors
- fractal recurrence islands
- temporal echo structures
```

Especially important:

```text
If recurrence survives large lag distances,
JANUS may encode global attractor memory.
```
