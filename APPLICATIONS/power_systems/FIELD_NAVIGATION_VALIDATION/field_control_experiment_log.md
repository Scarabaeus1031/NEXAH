# 🎛️ NEXAH Control Experiment Log

## Phase C — Field Control & Intervention

### Background

The previous phase of the FIELD_NAVIGATION_VALIDATION program focused on the discovery and validation of navigable field geometry.

This work is documented in:

```text
navigation_experiment_log.md
```

and summarized in:

```text
navigation_findings.md
```

---

## Phase A — Geometry Discovery

The first objective was to determine whether real IEEE39 operating states exhibit meaningful geometric organization.

### Key Findings

- Continuous field geometry detected
- Dense operating regions detected
- Transport corridors detected
- Gate candidates detected
- Basin-only interpretation not supported

### Primary Experiments

```text
EXP_06
EXP_07
EXP_07B
EXP_08
```

### Result

```text
Dynamics
    ↓
Geometry
```

---

## Phase B — Navigation Validation

The second objective was to determine whether the discovered geometry can be used for navigation.

### Key Findings

- Corridor acquisition validated
- Corridor retention validated
- Risk-aware navigation validated
- Gate-aware routing validated
- Regime boundaries detected
- Transition corridors detected
- Finite-width gate structures detected

### Primary Experiments

```text
EXP_01 → EXP_15
```

### Result

```text
Geometry
    ↓
Navigation
```

---

## Current Status

The following validation chain has been established:

```text
Dynamics
    ↓
Geometry
    ↓
Transport Corridors
    ↓
Gate Structures
    ↓
Regime Boundaries
    ↓
Transition Corridors
    ↓
Navigation
```

At this stage, the existence of navigable field structure is supported by experimental evidence.

---

# Phase C — Control

The objective of the next phase is fundamentally different.

Previous phases answered:

```text
Can the field be discovered?

Can the field be navigated?
```

Phase C asks:

```text
Can the field be used
to intentionally change
system behavior?
```

The focus shifts from:

```text
Observation
```

to

```text
Intervention
```

---

## Core Questions

### C1

```text
Can a state be steered
from one regime
into another?
```

---

### C2

```text
What is the minimum
intervention required
for a regime transition?
```

---

### C3

```text
Do gate structures provide
control leverage?
```

---

### C4

```text
Can field-based control
prevent instability
or recover from degraded regimes?
```

---

### C5

```text
Can a complete
field-aware controller
be constructed?
```

---

## Planned Experiments

```text
EXP_16 — Targeted Regime Steering

EXP_17 — Minimal Intervention

EXP_18 — Gate Control

EXP_19 — Regime Recovery

EXP_20 — Field Controller Validation
```

---

## Working Hypothesis

If the reconstructed field geometry represents genuine system structure, then intervention through field-guided control should require less effort than blind control.

Formally:

```text
Field Knowledge
        +
Control Action

    >

Control Action Alone
```

---

## Phase Status

```text
PHASE A
Geometry
✓ Completed

PHASE B
Navigation
✓ Completed

PHASE C
Control
▶ Starting
```

# EXP_16 — TARGETED REGIME STEERING

## Objective

After establishing the existence of:

- field geometry (EXP_08),
- transport gates (EXP_09–10),
- separatrix structures (EXP_11),
- regime boundaries (EXP_12),
- transition corridors (EXP_13),
- navigation interactions (EXP_14),
- and finite crossing costs (EXP_15),

EXP_16 investigates whether targeted steering toward the discovered gate corridor improves regime-transition performance.

This is the first experiment of:

FIELD CONTROL & INTERVENTION

---

## Results

States:

    540

LEFT states:

    376

RIGHT states:

    164

Random Success:

    0.448148

Gate Success:

    0.564815

Random Effort:

    15.974074

Gate Effort:

    14.516667

Control Gain:

    1.100395

---

## Key Finding

Targeted steering toward the discovered gate corridor outperforms random steering.

Observed:

```text
Success Increase

44.8 %
      ↓
56.5 %
```

and

```text
Required Effort

15.97
      ↓
14.52
```

This is the first indication that the reconstructed field geometry contains actionable intervention structure.

---

# Visual Evidence

## Visual 1 — Transition Map

![Transition Map](./outputs/EXP_16_TARGETED_REGIME_STEERING/exp16_transition_map.png)

### Observation

The state-space separates into two large operating regions.

The discovered gate nodes lie inside the transition zone connecting both regimes.

Interestingly, the geometry resembles:

```text
R-shape
+
Mirrored L-shape
```

with a central transition corridor.

The gate system occupies the narrow connection region between these larger structures.

### Interpretation

The field does not appear isotropic.

Instead it contains preferred transport channels through which transitions occur more easily.

---

## Visual 2 — Crossing Success

![Crossing Success](./outputs/EXP_16_TARGETED_REGIME_STEERING/exp16_crossing_success.png)

### Observation

Targeted steering achieves a higher crossing success rate than random steering.

```text
Random : 44.8 %

Gate   : 56.5 %
```

### Interpretation

The gate corridor contains information relevant to regime transition.

Steering toward the gate increases the probability of successful crossing.

---

## Visual 3 — Required Effort

![Required Effort](./outputs/EXP_16_TARGETED_REGIME_STEERING/exp16_required_effort.png)

### Observation

Gate-guided intervention requires less displacement than random intervention.

```text
Random : 15.97

Gate   : 14.52
```

### Interpretation

The discovered gate corridor appears to reduce control cost.

The field therefore contains regions of differing intervention efficiency.

---

## Visual 4 — Control Advantage

![Control Advantage](./outputs/EXP_16_TARGETED_REGIME_STEERING/exp16_control_advantage.png)

### Observation

Measured control gain:

```text
1.10
```

Equivalent to approximately:

```text
10 %
```

improvement over random steering.

### Interpretation

The improvement is modest but systematic.

Even this simple steering strategy extracts useful information from the reconstructed field geometry.

---

## Scientific Assessment

EXP_16 is the first experiment demonstrating:

```text
Field Geometry
        ↓
Control Advantage
```

Previous experiments established that:

```text
Geometry
→ Gates
→ Navigation
```

EXP_16 extends this chain toward intervention:

```text
Geometry
→ Gates
→ Navigation
→ Control
```

The result suggests that transport structures discovered through NEXAH may be usable not only for observation and navigation but also for active steering.

---

## Relation To Previous Experiments

EXP_08

```text
Discovered field geometry.
```

EXP_09

```text
Discovered navigation advantage.
```

EXP_10

```text
Validated transport structure.
```

EXP_11–EXP_15

```text
Validated separatrix,
regimes,
transition corridors,
and crossing cost.
```

EXP_16

```text
Demonstrated the first
field-guided control advantage.
```

---

## Conclusion

The reconstructed IEEE39 field contains intervention-relevant structure.

Targeted steering toward the gate corridor:

- increases transition success,
- reduces required effort,
- produces measurable control gain.

This marks the transition from:

```text
Field Navigation
```

toward

```text
Field Control
```

and represents the first positive result of Phase C.

---

## Status

```text
FIELD-GUIDED CONTROL

DETECTED

Validation: PASSED
```
