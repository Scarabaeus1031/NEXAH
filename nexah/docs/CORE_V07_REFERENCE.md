# NEXAH Core Specification (v0.7 – Frozen Kernel)

> **Historical behavior reference.** This document preserves the terminology
> of the v0.7 freeze. For the verified software scope, characterized legacy
> semantics, and evidence boundary, use
> **[BASELINE_STATUS.md](BASELINE_STATUS.md)**. In particular, stochastic target
> analysis is not deterministic, local cluster IDs are not persistent, and
> navigation/control outputs are heuristics rather than causal guarantees.

## Overview

NEXAH is a minimal system for analyzing and navigating dynamical behavior in time series data.

It transforms a trajectory into a discrete state system, extracts transition dynamics, and enables:

- structural analysis
- regime detection
- probabilistic navigation
- intervention suggestions
- system comparison (v0.7)

The system is intentionally minimal, interpretable, and deterministic.

---

## Core API

python nexah.analyze(trajectory, target_state=None)

### Input

- trajectory: 1D or n-dimensional time series
- target_state (optional): integer state index

---

### Output (Key Fields)

- current_state: last inferred state
- best_state: highest scoring state
- transitions: transition probability matrix
- stable_states: high self-transition states
- regime_shifts: indices of state changes
- instability: local instability scores
- escape_difficulty: difficulty to leave states
- state_scores: heuristic ranking of states
- signature: structural fingerprint (v0.7)

If target_state is provided:

- path_bfs: shortest path to target
- path_prob: stochastic path sample
- dynamics: transition statistics (probability + time)
- intervention: path-based intervention cost
- control: suggested transition modification

---

## System Architecture

### 1. Representation Layer

Transforms raw trajectory into a state space representation.

Steps:
- optional normalization
- reshape to (T, D)
- sliding window embedding

python X_t = [x_t, x_{t+1}, ..., x_{t+w}]

---

### 2. Structure Layer

Extracts discrete system states and transitions.

#### Clustering
- KMeans over embedded states
- deterministic via random_state

#### Transition Matrix

Let ( s_i ) be cluster labels.

Transition probability:

[
P(a \rightarrow b) = \frac{\text{count}(a \rightarrow b)}{\sum_{k} \text{count}(a \rightarrow k)}
]

---

### 3. State Graph

Directed graph:

- Nodes = states
- Edges = transition probabilities

---

## Stability Metrics

### Self-Transition Probability

[
S(s) = P(s \rightarrow s)
]

Interpretation:
- high → stable regime
- low → dynamic / unstable

---

### Escape Difficulty

[
D(s) = P(s \rightarrow s)
]

High value = hard to leave state

---

### Instability Score (local)

Based on label changes in a sliding window:

[
I_t = \frac{\text{state changes in window}}{\text{window size}}
]

---

## Navigation

### Shortest Path (BFS)

Graph-based reachability:

- ignores probabilities
- finds minimal step path

---

### Probabilistic Navigation

Monte Carlo sampling:

[
s_{t+1} \sim P(s_t \rightarrow \cdot)
]

Captures realistic system dynamics.

---

## Intervention Model

### Path Cost

For a path ( s_0 → s_1 → ... → s_n ):

[
\text{cost} = \sum_{i} (1 - P(s_i \rightarrow s_{i+1}))
]

Interpretation:
- high cost = unlikely transitions
- low cost = natural flow

---

## Transition Dynamics Estimation

Monte Carlo simulation:

### Hit Probability

[
\hat{P} = \frac{\text{successful runs}}{\text{total runs}}
]

### Expected Steps

[
E[T] = \frac{1}{N} \sum \text{steps to reach target}
]

---

## Control Layer (Heuristic)

Goal:
Identify which transition modification most improves reachability.

Method:

1. For each transition ( a → b )
2. Slightly increase probability (+ε)
3. Renormalize
4. Recompute hit probability
5. Measure improvement

---

### Output

python {
  "from": state_a,
  "to": state_b,
  "improvement": delta_probability,
  "new_probability": updated_hit_probability
}

---

## State Scoring

[
score(s) = P(s \rightarrow s) - \alpha (1 - P(s \rightarrow s))
]

Interpretation:
- rewards stability
- slightly penalizes excessive lock-in

---

## System Signature (v0.7)

Each trajectory produces a structural fingerprint:

- n_states_observed
- dominant_state
- occupancy distribution
- escape_difficulty
- transition_entropy

---

## System Comparison (v0.7)

Two systems are compared via:

- stability profile difference
- transition entropy difference

Similarity score:

[
similarity = \frac{1}{1 + \Delta_{stability} + \Delta_{entropy}}
]

---

## Design Constraints

- no deep learning
- no hidden latent models
- no symbolic abstraction layers
- fully interpretable
- deterministic behavior (via random_state)
- minimal dependencies

---

## Core Freeze (v0.7)

The NEXAH kernel is frozen.

No further changes will be made to:

- embedding logic
- clustering method
- transition modeling
- navigation algorithms
- control heuristic

Reason:

- preserve reproducibility
- ensure interpretability
- stabilize system behavior

All future extensions must be implemented as external layers.

---

## Limitations

- discrete approximation of continuous systems
- clustering instability (label permutations)
- comparison ignores phase alignment
- control is local and heuristic
- no causal guarantees
- sensitive to embedding parameters

---

## Intended Use

- exploratory system analysis
- regime detection
- transition modeling
- early-stage control prototyping
- cross-system comparison

---

## Future Extensions (Outside Core)

- sensitivity analysis
- continuous control fields
- improved similarity metrics
- advanced embeddings
- visualization layer
- CLI / tooling
- real-world integrations

---

## Summary

NEXAH Core v0.7 provides:

- structure extraction
- dynamic modeling
- navigation
- intervention estimation
- system comparison

It is a minimal, deterministic, and interpretable kernel for analyzing dynamical systems.

The core is now frozen.

Further value will come from:

→ applications  
→ tooling  
→ analysis layers  

not from modifying the kernel.

---
