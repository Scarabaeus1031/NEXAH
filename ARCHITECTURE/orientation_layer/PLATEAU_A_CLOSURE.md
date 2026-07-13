# Plateau A Closure — Status after Memory V2

Status: completed and regression-tested

This record closes the first implemented Orientation path before Phase III —
Adapter Ecosystem and Domain Testing. It summarizes repository evidence; it
does not introduce a new scientific claim.

## Implemented path

```text
raw dynamics
→ frozen v0.7 backend
→ typed backend adapter
→ OrientationState
→ evidence-bound OrientationReport
→ externally observed Outcome
→ append-only Episode
→ similarity retrieval
→ explicit context for a later orientation cycle
```

Retrieval does not mutate or train the v0.7 backend. Provenance and uncertainty
remain explicit across the typed contracts.

## Evidence at closure

| Evidence line | Result | Scope |
|---|---:|---|
| Repository regression suite | 73 passed | Current package, contracts, reports, memory, validations |
| Static type check | 14 modules clean | Orientation, backend, and V2 validation boundary |
| Demonstrator proxy | Reproducible | Constructed reference, not external ground truth |
| Memory V1 | 11/12 Top-1 | One reference per synthetic family |
| Memory V2 validation | 6/6 Top-1 | Method selection split |
| Memory V2 held-out test | 6/6 Top-1; Recall@3 6/6 | Six separately defined synthetic queries |
| Canonical reproducibility | Two byte-identical runs | Fixed timestamp, inputs, and configuration |

Memory V2 selected the predeclared `sequence_profile` method using validation
only. The held-out test was not used for selection. The complete record is in
**[validation/memory_generalization_v2/](../../validation/memory_generalization_v2/)**.

## Scientific boundary

The minimum held-out V2 margin is `0.003172`. The tested queries are correctly
classified, but the weakest separation is close. The result supports
deterministic family-level retrieval within the synthetic fixture. It does not
establish:

- semantic relevance of a retrieved Outcome
- calibrated confidence or uncertainty
- generalization to real-world data
- decision quality or causal intervention
- autonomous execution

V1 and V2 remain frozen. Further claims require a new version and independent
data rather than tuning against the existing held-out cases.

## Phase III entry gate

Phase III may begin because the internal path, persistence boundary, evaluation
fixture, and known limitations are explicit. Its first objective is a small
adapter ecosystem:

```text
independent source
→ source adapter
→ explicit domain context
→ representation backend
→ existing Orientation contracts
→ domain-specific validation
```

An adapter must not insert the expected family, result, or decision into a field
used by similarity. Each adapter needs contract tests, failure behavior,
provenance, and an independently scoped validation record.

The next design input is **[ADAPTER_LANDSCAPE.md](ADAPTER_LANDSCAPE.md)**; the
next implementation task is the minimal source-adapter contract.

## Visual record

![Orientation Core status](visuals/orientation-core-memory-v2-status-page-1.png)

![Memory V2 validation](visuals/memory-generalization-v2-validation-page-2.png)
