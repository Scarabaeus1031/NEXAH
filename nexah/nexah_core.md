# NEXAH Core Specification

## Overview

NEXAH is a minimal system for analyzing and navigating dynamical behavior in time series data.

It transforms a trajectory into a discrete state system, extracts transition dynamics, and enables:

- structural analysis
- regime detection
- probabilistic navigation
- intervention suggestions

The system is intentionally minimal and interpretable.

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
- path_bfs: shortest path to target (if provided)
- path_prob: stochastic path sample
- dynamics: transition statistics (probability + time)
- intervention: path-based intervention cost
- control: suggested transition modification

---

## System Architecture

### 1. Representation Layer

Transforms raw trajectory into a state space representation.

Method:
- Sliding window embedding

python X_t = [x_t, x_{t+1}, ..., x_{t+w}] 

---

### 2. Structure Layer

Extracts discrete system states and transitions.

#### Clustering
- KMeans over embedded states

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

For a path ( s_0 \rightarrow s_1 \rightarrow ... \rightarrow s_n ):

[
\text{cost} = \sum_{i} (1 - P(s_i \rightarrow s_{i+1}))
]

Interpretation:
- high cost = unlikely transitions
- low cost = natural flow

---

## Transition Dynamics Estimation

Monte Carlo simulation:

For multiple trials:

- simulate until target reached or cutoff
- measure:

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

1. For each transition ( a \rightarrow b )
2. Slightly increase probability (+ε)
3. Renormalize
4. Recompute hit probability
5. Measure improvement

---

### Output

python {   "from": state_a,   "to": state_b,   "improvement": delta_probability,   "new_probability": updated_hit_probability } 

---

## State Scoring

Simple heuristic:

[
score(s) = P(s \rightarrow s) - \alpha (1 - P(s \rightarrow s))
]

Interpretation:
- rewards stability
- penalizes excessive lock-in slightly

---

## Design Constraints

- no deep learning
- no hidden latent models
- no symbolic abstraction layers
- fully interpretable
- minimal dependencies

---

## Limitations

- discrete approximation of continuous systems
- clustering instability (label permutations)
- control is local and heuristic
- no causal guarantees
- sensitive to embedding parameters

---

## Intended Use

- exploratory system analysis
- regime detection
- early-stage control prototyping
- educational / research use

---

## Future Extensions

- sensitivity analysis (transition gradients)
- continuous control models
- adaptive embeddings
- multi-dimensional trajectory support
- real-world system integration

---

## Summary

NEXAH Core provides a minimal, interpretable framework for:

- extracting structure from time series
- modeling transitions
- navigating state spaces
- estimating intervention strategies

It is designed as a foundation for further development into a full dynamical control system.

---
