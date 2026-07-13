# IEEE Scaling Pattern V2 — Canonical Record

Status: frozen baseline-anchored continuation and held-out scale gate

Recorded timestamp: `2026-07-13T21:00:00+00:00`

## Why V2 was required

V1 used one global grid from `0.6` to `5.0`. IEEE-300 and PEGASE-9241 failed at
its lower endpoint, so the run could not distinguish an unsuitable scan origin
from the absence of a physical branch. In the six usable cases, the apparent
precursor peak was fixed to the derivative exclusion boundary and moved under
downsampling.

V2 does not alter V1. It starts a new experiment at each network's native
operating point and separates load direction, convergence-boundary estimation,
and pattern testing.

## Predeclared method

Development cases:

- IEEE-9, IEEE-14, IEEE-30, IEEE-57, IEEE-118, IEEE-300
- PEGASE-1354

Held-out scale gate:

- PEGASE-9241

Physical scan:

- native baseline: `lambda = 1.0`
- upward independent-point scan: step `0.025`, maximum `5.0`
- downward independent-point scan: step `0.05`, minimum `0.2`
- stop each branch after its first non-converged point
- refine bracketed upward boundaries by bisection to width `<= 0.005`
- retain the historical physical `c_struct` metric for comparability

Pattern test:

- seven-point local cubic estimate of the second derivative
- local maximum rather than a global edge maximum
- minimum relative prominence: `0.1`
- minimum refined-boundary distance: four grid steps
- location stability on every second converged point: two coarse steps
- quadratic monotone null must not produce an accepted peak

No parameter was changed after inspecting PEGASE-9241.

## H–I result: branches and boundaries

| System | Upward last converged | Upward first failed | Refined interval | Downward result |
|---|---:|---:|---:|---|
| IEEE-9 | 2.253125 | 2.256250 | 0.003125 | right-censored at 0.2 |
| IEEE-14 | 4.003125 | 4.006250 | 0.003125 | right-censored at 0.2 |
| IEEE-30 | 3.656250 | 3.659375 | 0.003125 | right-censored at 0.2 |
| IEEE-57 | 1.446875 | 1.450000 | 0.003125 | right-censored at 0.2 |
| IEEE-118 | 1.812500 | 1.815625 | 0.003125 | right-censored at 0.2 |
| IEEE-300 | 1.031250 | 1.034375 | 0.003125 | bracketed: 0.95 / 0.90 |
| PEGASE-1354 | 1.306250 | 1.309375 | 0.003125 | bracketed: 0.50 / 0.45 |
| PEGASE-9241 | 1.068750 | 1.071875 | 0.003125 | bracketed: 0.85 / 0.80 |

The native baseline converged in all eight systems. The V1 lower-bound failures
were therefore consequences of that global scan design, not proof that the
standard cases lacked a usable operating point.

These values describe pandapower Newton–Raphson convergence under the declared
setup. They are not certified physical voltage-stability limits or results from
a continuation-power-flow algorithm.

## J result: edge-independent pattern test

- six development cases had enough points for the frozen pattern test
- none produced a stable interior peak satisfying all criteria
- IEEE-300 had only two converged coarse points and was explicitly not testable
- zero development cases support the stronger candidate-precursor claim

The evidence remains consistent with boundary acceleration. It does not support
a universal, edge-independent `c_struct` precursor.

## K result: PEGASE-9241 held-out gate

All procedural gate criteria passed:

- native baseline converged
- separate branches and explicit failures were recorded
- the H–J parameters were not retuned
- the metric definition was unchanged
- uncertainty and limitations were retained

PEGASE-9241 had only three converged upward coarse points before its bracketed
boundary. The seven-point J method therefore cannot be evaluated. The canonical
gate outcome is:

```text
boundary_of_validity
```

This is neither confirmation nor refutation of an interior feature at finer
resolution. A new experiment could study that question, but PEGASE-9241 would
no longer be an untouched held-out case.

## Reproducibility

Two independent final executions produced byte-identical canonical artifacts
after declared 12-significant-digit JSON serialization:

- result SHA-256: `f995144188dc5b6e979d7a660839c35af5042be2404c5c07b1fe57827f1d1746`
- summary SHA-256: `a5dc3d73536c66a12a546f0cb41afb11769fceaf7e1da3f543a5f61eb5745d1b`

The serializer removes platform-level floating noise around `1e-18`; it does
not alter calculation branches, acceptance thresholds, or classifications.

## Phase III conclusion

The adapter ecosystem now has generic array and table sources plus a coupled
IEEE/Pandapower domain source, typed translation, scoped orientation, physical
attribution, versioned domain validation, baseline-anchored branch analysis,
resolved numerical boundaries, and an honest held-out scale gate.

Phase III closes with a bounded result: the end-to-end architecture works, but
the historical universal precursor claim is not supported by the frozen V2
test. Broader source families remain later ecosystem expansion, not missing
evidence for this closure.
