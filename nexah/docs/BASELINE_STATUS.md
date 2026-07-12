# NEXAH v0.7 Baseline Status

Status: frozen computational baseline  
Package version: `0.7.0`  
Primary implementation: `nexah/core.py`

## Verified scope

The characterization suite verifies that the current package:

- preprocesses one- and multi-dimensional trajectories
- creates the historical sliding-window representation
- derives normalized empirical transition probabilities
- returns the documented analysis result structure
- produces repeatable non-stochastic analysis for a fixed input and seed
- reports trivial target reachability consistently
- compares identical trajectories with zero signature deltas
- exposes analysis through the command-line interface

These tests establish software behavior. They do not establish that inferred
states correspond to externally true regimes or that navigation and control
suggestions cause real-world outcomes.

## Frozen pipeline

```text
trajectory
→ optional global normalization
→ overlapping window embedding
→ KMeans labels
→ empirical transition probabilities
→ heuristic stability and change measures
→ graph and Monte Carlo navigation estimates
```

## Characterized legacy semantics

The following behavior is part of the recorded v0.7 baseline and is not silently
changed during the freeze:

1. `_embed` returns `T - window` samples, omitting the final mathematically
   possible window.
2. Embedded samples overlap by `window - 1` observations. Persistence measures
   can therefore reflect overlap as well as system behavior.
3. Regime and instability indices refer to embedded-sample positions, not raw
   trajectory indices. Consumers must apply an explicit alignment policy.
4. KMeans is fitted independently for every `analyze` call. Cluster IDs are
   local to that fit and are not persistent identities across analyses.
5. Stable states use the fixed rule `P(s→s) > 0.9`.
6. “Escape difficulty” is the self-transition probability, not a separately
   estimated energy barrier or causal escape model.
7. “Minimal intervention” first chooses an unweighted BFS path and then scores
   it. It is not a minimum-cost path optimizer.
8. Probabilistic navigation, dynamics estimation, and control sensitivity use
   Monte Carlo sampling. The constructor currently seeds process-global random
   generators; stochastic call order can influence later stochastic results.
9. “Control” perturbs an empirical transition matrix. It does not identify a
   validated physical intervention.
10. `compare` compares summary heuristics from separately fitted local maps; it
    does not align state identities.

## Evidence boundary

Running on synthetic or real-world time series demonstrates execution on those
inputs. Validation of regime truth, early warning, navigation quality, causal
intervention, or cross-domain generality requires labeled ground truth,
baselines, uncertainty analysis, and independent reproducibility appropriate to
the claim.

## Freeze policy

- bug fixes that change recorded outputs require a versioned decision and test
  update
- the Orientation Layer wraps v0.7 through an adapter rather than assigning new
  semantics to its outputs
- new memory, context, provenance, uncertainty, or reporting behavior belongs
  outside `core.py`
- historical documents remain available but do not override this status file

