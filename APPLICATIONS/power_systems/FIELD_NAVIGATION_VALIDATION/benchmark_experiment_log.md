# NEXAH Benchmark Suite

## Purpose

The previous validation phases established the existence, geometry, navigability, and controllability of the reconstructed NEXAH field.

These results are documented in:

- `navigation_experiment_log.md`
- `field_control_experiment_log.md`

Together, these experiments demonstrated:

```text
Dynamics
    ↓
Field Geometry
    ↓
Navigation
    ↓
Control
```

The objective of the benchmark phase is different.

The benchmark phase does not ask:

    Does the field exist?

or

    Can the field navigate?

These questions have already been investigated.

Instead, the benchmark phase asks:

    Is NEXAH useful?

and

    Does NEXAH provide measurable advantages
    compared to existing methods?

---

# Previous Validation Phases

## Phase A — Field Discovery

Document:

```text
navigation_experiment_log.md
```

Main Results:

- Real field geometry detected
- Transport corridors detected
- Gate structures detected
- Separatrix candidates detected
- Regime boundaries identified
- Regime transition corridors identified
- Gate-based navigation demonstrated

Core conclusion:

```text
The reconstructed state-space
is not random.

It forms a navigable field.
```

---

## Phase B — Field Control

Document:

```text
field_control_experiment_log.md
```

Main Results:

- Targeted regime steering
- Gate-aware navigation
- Region-to-region navigation
- Navigation efficiency analysis
- Robustness testing
- Backbone resilience analysis

Core conclusion:

```text
The field can be used
for directed intervention.

Navigation is controllable.
```

---

# Phase C — Benchmark Validation

Document:

```text
benchmark_experiment_log.md
```

Objective:

Evaluate NEXAH against engineering-relevant criteria.

Focus:

- Navigation efficiency
- Robustness
- Fault tolerance
- Partial information
- Dynamic failures
- Prediction capability
- Control performance
- Real-world applicability

The benchmark phase represents the transition from:

```text
Scientific Discovery
```

to

```text
Engineering Validation
```

---

# Benchmark Roadmap

## EXP_22 — Partial Knowledge Benchmark

Question:

```text
Can NEXAH navigate effectively
when only part of the field
is known?
```

Comparison:

- Classical shortest-path methods
- NEXAH field navigation

under incomplete information.

---

## EXP_23 — Dynamic Failure Benchmark

Question:

```text
Can NEXAH maintain navigation
while the field changes
during operation?
```

---

## EXP_24 — Prediction Benchmark

Question:

```text
Can field geometry provide
early-warning information
before regime transitions occur?
```

---

## EXP_25 — Control Benchmark

Question:

```text
Can NEXAH actively move
a system toward a desired
operating region?
```

---

# Benchmark Philosophy

The benchmark phase is intentionally conservative.

The goal is not to prove NEXAH correct.

The goal is to test whether NEXAH provides measurable engineering value.

Success will be evaluated using:

- quantitative comparisons
- reproducible experiments
- baseline methods
- robustness metrics
- control performance

Only improvements that survive direct comparison against established methods will be considered meaningful.

---

# Current Status

Field Discovery:

```text
COMPLETE
```

Field Control:

```text
ACTIVE
```

Benchmark Validation:

```text
STARTING
```

Next Experiment:

```text
EXP_22 — PARTIAL KNOWLEDGE BENCHMARK
```

# EXP_22 — PARTIAL KNOWLEDGE BENCHMARK

## Objective

One of the central questions for real-world deployment is:

> How much of the field must be known before navigation becomes reliable?

Previous experiments assumed that the navigation layer had access to the full discovered field geometry.

EXP_22 tests a more realistic scenario:

- incomplete field knowledge
- partially observed state spaces
- limited mapping coverage
- early-stage exploration

The experiment measures navigation performance while progressively revealing larger fractions of the discovered field.

---

## Method

Navigation was tested using the same left-to-right target navigation setup used in EXP_19.

The known field fraction was varied:

- Random baseline
- 25% known
- 50% known
- 75% known
- 100% known

For each scenario:

- navigation success was measured
- average arrival steps were recorded
- visible field geometry was visualized

---

## Results

| Knowledge Level | Success Rate | Average Steps |
|-----------------|-------------|--------------|
| Random          | 0.0080 | 99.93 |
| 25%             | 0.0000 | 100.00 |
| 50%             | 0.0000 | 100.00 |
| 75%             | 1.0000 | 36.18 |
| 100%            | 1.0000 | 27.54 |

---

## Visual Analysis

### Known Field Coverage

![EXP_22 Known Field Examples](./outputs/EXP_22_PARTIAL_KNOWLEDGE_BENCHMARK/exp22_known_field_examples.png)

**File:**

`exp22_known_field_examples.png`

The geometry reveals a clear transition:

- 25% knowledge shows isolated local fragments
- 50% knowledge shows larger connected regions
- 75% knowledge begins to expose the global transport structure
- 100% knowledge reveals the complete navigation field

A striking observation is that navigation does **not** improve gradually.

Instead, it exhibits a threshold-like transition.

---

### Success vs Knowledge

![EXP_22 Success vs Knowledge](outputs/EXP_22_PARTIAL_KNOWLEDGE_BENCHMARK/exp22_success_vs_knowledge.png)

**File:**

`exp22_success_vs_knowledge.png`

Navigation remains effectively impossible at:

- Random
- 25%
- 50%

but suddenly becomes fully reliable at:

- 75%
- 100%

This suggests the existence of a critical field-knowledge threshold.

---

### Steps vs Knowledge



![EXP_22 Steps vs Knowledge](./outputs/EXP_22_PARTIAL_KNOWLEDGE_BENCHMARK/exp22_steps_vs_knowledge.png)

**File:**

`exp22_steps_vs_knowledge.png`

Once the field becomes sufficiently known:

- success jumps to 100%
- travel cost drops dramatically

Average navigation effort decreases from:

```text
100 steps
↓
36 steps
↓
28 steps
```

as field knowledge increases.

---

## Key Finding

EXP_22 reveals that:

> Navigation requires only partial field knowledge,
> but a minimum global structure must be visible.

The transition is not linear.

Instead, the experiment shows a clear phase change:

```text
Below threshold:
No navigation

Above threshold:
Reliable navigation
```

---

## Interpretation

The discovered field appears to contain a global transport geometry.

Local fragments alone are insufficient.

However, once enough of the field becomes visible, the navigation layer can reconstruct effective movement corridors.

This behavior resembles:

- percolation transitions
- connectivity thresholds
- phase transitions in network accessibility

rather than conventional local search.

---

## Engineering Relevance

For real systems this is highly significant.

A controller may not need:

- full system observability
- complete state-space reconstruction
- exhaustive mapping

Instead, only enough field structure may be required to expose the dominant transport geometry.

Potential applications include:

- power-grid stabilization
- autonomous planning
- infrastructure resilience
- network routing
- adaptive control systems

---

## Conclusion

EXP_22 provides the first benchmark evidence that:

> Successful NEXAH navigation emerges once field knowledge exceeds a critical threshold.

The transition occurs between:

```text
50% known
and
75% known
```

within the current field geometry.

This motivates the next benchmark experiment:

**EXP_22B — Knowledge Threshold Scan**

which will determine the critical navigation threshold with significantly higher resolution.

