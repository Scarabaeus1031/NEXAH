# Orientation MVP Alpha — Validation Record

Validation ID: `orientation-mvp-validation-v1`  
Recorded run time: `2026-07-13T08:00:00+00:00`  
Status: reproducible proxy validation; not external regime validation

## Configuration

```text
Demonstrator trajectory: deterministic Lorenz Euler simulation
steps: 8000
dt: 0.01
requested radial sheets: 6

v0.7 clusters: 6
v0.7 window: 10
v0.7 random state: 42
event matching tolerance: ±10 source samples
baseline: predict no transition events
```

Parameters were declared before reading validation scores and were not tuned
against this proxy result.

## Result

| Method | Predicted | Matched | Precision | Recall | F1 | Exact accuracy |
|---|---:|---:|---:|---:|---:|---:|
| v0.7 local label changes | 336 | 268 | 0.797619 | 0.451178 | 0.576344 | 0.890250 |
| Null: no changes | 0 | 0 | 0.000000 | 0.000000 | 0.000000 | 0.925750 |

Reference proxy events: 594  
Mean absolute timing error among matched events: 3.085821 samples

The higher exact accuracy of the null baseline is a class-imbalance artifact:
most samples are not transition samples. Event precision, recall, and F1 carry
the relevant comparison here.

## Reproducibility

Two complete runs with the same declared inputs produced byte-identical
artifacts:

| Artifact | SHA-256 |
|---|---|
| `orientation_state.json` | `183c4bb1d936f803c4225431e3c8c9fd32325ac9ce0044286ca14551fa184223` |
| `orientation_report.json` | `bd0b02f89a69ab52201adbbba3b788f8b588841ffe61ce3c9a9f1bf634be4e5f` |
| `baseline_comparison.json` | `e4084f6f4925c6a6150b36d0da99873addba2e0dc48e622d0d899432dca0fc33` |
| `failure_cases.json` | `745ca33495d0208bb79c621a5698325c459e39fe8f5ceed14fe67bd05fd75c65` |
| `validation_summary.md` | `163c6993b275a3e7a34526c2f7695c5d813012dc178e35e5b79b089e05ea9900` |

Generated artifacts live under ignored `outputs/orientation_mvp/`. The compact
comparison and failure-case records are committed beside this document.

## Interpretation

This validates that the first Orientation Layer path can reproducibly:

- consume the canonical Demonstrator trajectory
- preserve source/embedding alignment and provenance
- generate an evidence-bound Orientation Report
- compare representation-level changes with a declared proxy and baseline
- publish uncertainty, assumptions, and failure cases

It does not establish that radial sheets are true regimes, that KMeans labels
share sheet semantics, that detected changes are causal transitions, or that the
result generalizes beyond this deterministic Lorenz construction.

## Known failure cases

See **[failure_cases.json](failure_cases.json)**. Most notably, the historical
`num_sheets=6` construction produces seven observed labels because the maximum
radius falls into an additional `np.digitize` boundary bin. This is recorded and
left unchanged for the reproducibility baseline.

