# IEEE Orientation Validation V1 — Canonical Record

Status: frozen after the preregistered canonical run

Recorded timestamp: `2026-07-13T18:00:00+00:00`

## Result

| Metric | Result |
|---|---:|
| Cases | IEEE-9 reference; IEEE-14 held-out |
| Physical threshold references observed | 3 |
| Covered within load-scale distance 0.1 | 2/3 |
| Mean nearest-event distance | 0.166667 |
| Entity salience attribution overlap | 11/12 |
| Repeated canonical runs | Byte-identical |

IEEE-9 produced representation events at load scales 1.3, 1.7, and 2.0. Its
minimum-voltage crossing at 1.2 and line-overload crossing at 1.6 were each
within one load step of an event. Power flow first failed at 2.3; this failure
was recorded but not represented as a fabricated numeric state.

Held-out IEEE-14 produced events at 1.3, 1.7, and 2.1. Its minimum-voltage
crossing occurred at 2.4, with nearest-event distance 0.3, and therefore failed
the frozen alignment tolerance. No 100-percent line-loading crossing occurred
within the tested range, so none was scored.

Two consecutive executions produced identical artifacts:

- result SHA-256: `1149c9c00d7c742e3d15513b1e1a1832ae984309681d53fb1f6d28ffdef80ad1`
- summary SHA-256: `712d7e89d489e2be5acc75f168327ce18c3b60b0cba32dc7f9c4f3e9ed8bc850`

## Interpretation

The result supports a working, reproducible path from coupled pandapower source
data through scoped orientation and spatial co-change attribution. It also
shows that event alignment from IEEE-9 does not transfer uniformly to IEEE-14.

The 11/12 attribution overlap indicates that the largest voltage or loading
co-change usually identifies the currently most stressed bus or line in these
events. This is a salience association, not a causal contribution estimate.

## Boundaries

- Load cases are independent steady-state solutions, not time dynamics.
- v0.7 events are local-cluster label changes, not physical regime labels.
- The thresholds are engineering reference markers, not a full stability study.
- Non-convergence is observed but excluded from the rectangular numeric input.
- No controller, action recommendation, early-warning claim, or causal model is
  validated.
- IEEE-14 failure is retained; parameters were not retuned after inspection.
