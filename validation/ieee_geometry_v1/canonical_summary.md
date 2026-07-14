# Phase V IEEE Geometry V1 — Canonical Validation Summary

Status: **gate passed**

## Frozen design

- Development case: IEEE-9
- Locked evaluation case: IEEE-14
- Development model: unchanged population standardization fitted on IEEE-9
- Operators: the six formulas frozen in `case_manifest.json`
- Parameter retuning after evaluation: none
- Campaign axis: ordered load scale, not elapsed time

## Canonical result

| Result | IEEE-9 development | IEEE-14 evaluation |
|---|---:|---:|
| Declared frames | 19 | 19 |
| Converged frames | 17 | 19 |
| Explicit failed frames | 2 | 0 |
| Available adjacent geometry steps | 16 | 18 |
| Available centered turns | 15 | 17 |
| Sampled solver-boundary records | 2 | 0 |

IEEE-14 accepts the frozen IEEE-9 representation without refitting. All 19
declared evaluation positions converge, so the frozen grid contains no sampled
solver boundary. This is an explicit absence of boundary evidence, not evidence
that no physical boundary exists.

## Reproducibility gate

The canonical runner verifies:

1. exact environment and adapter protocol;
2. exact replay of the IEEE-9 model and geometry;
3. fresh reconstruction of the IEEE-14 physical frames;
4. exact replay of evaluation geometry;
5. exact replay of all five probes and the Orientation Report;
6. JSON and Markdown briefs from the same typed result;
7. explicit failure preservation and a closed episodic-memory boundary.

Two independent runner executions produce byte-identical summaries.

## Interpretation boundary

Supported within the frozen benchmark protocol:

- reproducible benchmark computation under the locked environment;
- predeclared perspectives over one ordered campaign;
- failure-aware local geometry measurements;
- unchanged application of the IEEE-9 method to IEEE-14.

Not supported:

- elapsed-time or operational-trajectory interpretation;
- certified voltage-stability boundary;
- causal precursor, probability, or control recommendation;
- real-world grid generalization;
- physical tube, smooth global manifold, or universal field;
- historically untouched evaluation evidence;
- observed outcome or episodic-memory update.

The machine-readable authority is [`canonical_summary.json`](canonical_summary.json).
