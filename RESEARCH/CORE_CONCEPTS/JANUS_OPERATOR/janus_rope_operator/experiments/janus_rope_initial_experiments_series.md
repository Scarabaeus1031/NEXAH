# 🧪 JANUS Rope Operator — Initial Experimental Series

Location:
`JANUS_ROPE_OPERATOR/experiments/`

Naming Convention:

```text
EXP_XX_<experiment_name>.py
```

Each experiment receives:

- unique EXP number
- dedicated Python file
- visual outputs
- optional animation
- parameter log
- observations
- follow-up notes

---

# 🧪 EXP_01 — Prime Drift Aperture Scan

File:

```text
EXP_01_prime_drift_aperture_scan.py
```

Goal:

```text
Test whether prime-offset timing
creates more stable apertures
than harmonic synchronization.
```

Core Idea:

Compare:

## Harmonic Mode

```text
1:2:4:8
```

vs

## Prime Drift Mode

```text
2:3:5:7
+
π
+
φ
+
√2
```

We measure:

- aperture persistence
- gate density
- synchronization collapse
- repeating loops
- phase drift lifetime
- transport continuity

Visuals:

- aperture maps
- rotating rope overlays
- gate persistence heatmaps
- timing interference plots

Expected Observation:

```text
harmonic timing collapses faster,
while prime drift preserves moving apertures.
```

---

# 🧪 EXP_02 — Offset Pole Geometry

File:

```text
EXP_02_offset_pole_geometry.py
```

Goal:

```text
Test whether moving the transition pole
away from the center
creates directional routing geometry.
```

Core Idea:

Compare:

## centered pole

```text
0 | 0
```

vs

## offset pole

```text
10 | 0
```

Measure:

- diagonal transitions
- routing asymmetry
- vortex formation
- spiral corridors
- coherence spine generation

Visuals:

- pole-field maps
- transport trajectories
- routing density plots
- transition angle scans

Expected Observation:

```text
offset poles generate directional transport
instead of symmetric collapse.
```

---

# 🧪 EXP_03 — Root Thread Stabilization

File:

```text
EXP_03_root_thread_stabilization.py
```

Goal:

```text
Test whether a slow regulator thread
stabilizes the entire rope network.
```

Core Idea:

Add:

```text
ROOT THREAD
```

with slow modulation:

```text
√2-based drift
```

Compare:

## without root thread

vs

## with regulator thread

Measure:

- gate survival
- rope coherence
- phase collapse frequency
- aperture continuity
- recursive memory stability

Visuals:

- stabilization overlays
- coherence timelines
- recursive attractor plots
- thread coupling diagrams

Expected Observation:

```text
the root thread behaves like
a global phase regulator.
```

---

# 🔷 Suggested Shared Core Engine

All experiments should eventually share:

```text
janus_rope_core.py
```

containing:

- rope generators
- phase systems
- prime timing operators
- aperture detection
- synchronization analysis
- transition tracking
- visualization helpers

This keeps the system modular.

---

# 🔷 Proposed Folder Structure

```text
JANUS_ROPE_OPERATOR/

├── README.md
├── building_log.md
├── janus_rope_core.py

├── experiments/
│
├── EXP_01_prime_drift_aperture_scan.py
├── EXP_02_offset_pole_geometry.py
├── EXP_03_root_thread_stabilization.py

├── visuals/
│
├── exp_01/
├── exp_02/
├── exp_03/

├── animations/
│
├── exp_01/
├── exp_02/
├── exp_03/
```

---

# 🔥 Experimental Priority

Recommended order:

| Priority | Experiment | Reason |
|---|---|---|
| 1 | EXP_01 | tests the core prime hypothesis |
| 2 | EXP_02 | tests geometric routing |
| 3 | EXP_03 | tests stabilization logic |

---

# 🌌 Current Interpretation

The first three experiments test:

```text
whether controlled non-repetition
can generate stable transport geometry.
```

This is currently the central working intuition
behind the JANUS Rope Operator system.
