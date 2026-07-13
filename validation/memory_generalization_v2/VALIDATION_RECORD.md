# Memory Generalization V2 — Validation Record

Status: canonical synthetic benchmark, frozen after the preregistered run

Recorded timestamp: `2026-07-13T12:00:00+00:00`

## Design

- 15 stored references: five each for Lorenz, Rössler, and Kuramoto
- six validation queries and six separately defined held-out test queries
- one generic context domain; family names do not enter similarity
- three methods declared before scoring: current signature, sequence profile,
  and a fixed 50/50 hybrid
- selection by validation Top-1, then MRR, then declared method order
- held-out results were not used to select or modify the method

## Result

The validation split selected `sequence_profile`.

| Split | Top-1 | Recall@3 | MRR | Mean margin | Minimum margin |
|---|---:|---:|---:|---:|---:|
| Validation | 1.000000 | 1.000000 | 1.000000 | 0.053166 | 0.001908 |
| Held-out test | 1.000000 | 1.000000 | 1.000000 | 0.053672 | 0.003172 |

All three predeclared methods reached 6/6 Top-1 on the held-out test. The
current signature reached only 5/6 on validation, while the selected sequence
profile reached 6/6.

Two consecutive canonical executions were byte-identical:

- result SHA-256: `e4bd8f5f95544ff964d66ab2bfee69289231aaeb78f8a48a01ff3f1dc004b8cb`
- summary SHA-256: `d9fb0f26aa44249dbff55072413516ea29e01e30d1124ddf39791a155df3a2ca`

## Interpretation and failure boundary

This benchmark supports deterministic family-level retrieval from a denser
episodic store under the tested parameter and noise changes. It does not show
semantic outcome relevance, real-world generalization, or decision quality.

The minimum positive held-out margin is small. Correct Top-1 classification is
therefore not the same as robust separation. The sequence profile is also a
validation feature derived from v0.7's exposed instability sequence; it is not
yet part of the production memory contract.

The next scientific step is not further tuning on these six test queries. It is
an adapter-level protocol that supplies independent domains and explicit
representation features, followed by a new benchmark version.
