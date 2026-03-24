# NEXAH Prime Modular Resonance — Extended Experimental Layer (v2)

**Path:** `ENGINE/research/experiments/NEXAH_experiment_prime_modular_resonance_v2.md`

---

## Purpose of v2

This document extends the base experiment by explicitly integrating **NEXAH-specific structures** discovered during exploratory analysis:

- Base 7 ↔ Base 17 coupling
- Mod 60 anchor set
- “Eris boundary” (~13.7 transition zone)
- FFT + Spiral Pulse observations
- Ghost-node candidate chains
- Mirror-chain dynamics

The goal is to **translate symbolic discoveries into testable modules**.

---

## Core Structural Elements

### 1. Modular Anchor System

Primary anchor set:

```text
Mod 60: [43, 37, 23, 17]
```

Interpretation layers:

- 43 → entry / phase onset
- 37 → mirror / reflection node
- 23 → transition / bridge
- 17 → stabilization / clamp

These form a **cyclic angular partition (≈ 360°)** and act as candidate attractors.

---

### 2. Base 7 ↔ Base 17 Dual System

Core mapping:

```math
a_n = p_n mod 7
b_n = p_n mod 17
c_n = (7 a_n + δ) mod 17
```

Interpretation:

- Base 7 → local rhythm / discrete beat
- Base 17 → stabilizing expansion space
- δ → gate offset (transition control)

Hypothesis:

> Instability in base-7 dynamics is reduced when lifted into base-17 space.

---

### 3. Eris Boundary (~13.7)

Observed transition zone:

```text
~12.6 – 13.7
```

Interpretation:

- breakdown of simple modular cycles
- onset of multi-branch behavior (“Medusa”)
- need for 17-clamp stabilization

Experimental role:

- detect phase transitions
- measure entropy spike / instability

---

## FFT + Spiral Pulse Layer

### Signal Construction

Define signal:

```math
x_n = p_n mod 60
```

or indicator-based:

```math
x_n = 1 if p_n ∈ anchor_set else 0
```

### Analysis

- FFT
- Autocorrelation
- Spiral projection (polar trajectory)

### Target Patterns

- 7-based periodicity
- mod 12 / 24 overlays
- harmonic clustering

---

## Ghost Node Hypothesis

Candidate sequence:

```text
33 – 137 – 233 – 337 – 433 – 437 – 533 – 537 ...
```

Interpretation:

- potential resonance corridor
- non-trivial recurrence across modular spaces

Test:

- frequency vs random primes
- clustering in FFT domain
- spatial density in trajectory maps

---

## Mirror Chain System

Examples:

```text
73 ↔ 37
137 ↔ 731
```

Hypothesis:

- reversal symmetry creates “resonance shortcuts” in graph topology

Test:

- enrichment in anchor corridors
- centrality in topology graphs
- spectral contribution

---

## Extended Experiment Modules

### Experiment A — Anchor Corridor Tracking

- track visits to [43,37,23,17]
- measure persistence length
- compare to controls

---

### Experiment B — Eris Transition Detection

- monitor entropy / variance vs index
- detect instability region
- correlate with modular collisions

---

### Experiment C — Ghost Node Validation

- build indicator signal
- run FFT + autocorrelation
- compare with shuffled sequences

---

### Experiment D — Mirror Chain Topology

- build graph including mirror links
- measure:
  - shortest paths
  - clustering
  - loop density

---

### Experiment E — Spiral Flow Comparison

- generate trajectories:
  - primes
  - random
- compare:
  - density
  - curvature
  - channel formation

---

## NEXAH Interpretation Layer

This system can be interpreted (non-physically) as:

- 7 → local oscillation / phase tick
- 17 → stabilization / global frame
- 60 → projection / compass layer
- Eris → instability boundary
- mirror chains → non-local shortcuts

---

## Minimal Implementation Hooks

Suggested scripts:

```text
scripts/
  anchor_corridor_scan.py
  eris_transition_detector.py
  ghost_node_fft.py
  mirror_chain_graph.py
  spiral_prime_vs_random.py
```

---

## Key Principle

> All symbolic structures must be tested against control systems.

No interpretation without:

- null models
- statistical comparison
- reproducibility

---

## Status

This is a **bridge document** between symbolic NEXAH structures and formal experimental validation.

Further iterations expected.

---

**Scarabæus1033 · NEXAH Research Layer**

