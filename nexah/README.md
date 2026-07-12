# `nexah` — Minimal State-Space Backend

This directory contains the installable Python package and command-line
interface. It is the current computational baseline for the planned NEXAH
Orientation Layer; it is not the complete orientation architecture.

## What the package currently does

`core.py` implements a compact trajectory-analysis pipeline:

```text
trajectory
→ sliding-window embedding
→ KMeans state assignment
→ empirical transition matrix
→ heuristic stability and regime analysis
→ graph and Monte Carlo navigation estimates
```

The resulting map is fitted locally for each analysis. Cluster identifiers do
not currently provide persistent state identity across separate runs.
Navigation, intervention, and control outputs are exploratory heuristics; they
must not be interpreted as causal or production control guarantees.

## Quick use

From the repository root:

```bash
python -m pip install -e .
nexah analyze data.csv
nexah compare a.csv b.csv
nexah orient data.csv \
  --recorded-at 2026-07-13T08:00:00+00:00 \
  --domain example
```

Python API:

```python
from nexah import NEXAH

engine = NEXAH(n_clusters=4, window=10, random_state=42)
report = engine.analyze(trajectory)
```

## Package layout

```text
nexah/
├── __init__.py
├── core.py                         current computational baseline
├── cli.py                          command-line adapter
├── backends/
│   └── v07.py                      v0.7 → OrientationState adapter
├── orientation/                    typed Orientation Layer contracts
│   ├── primitives.py               scoped operational vocabulary
│   ├── evidence.py                 provenance and uncertainty
│   ├── state.py                    OrientationState input contract
│   ├── report.py                   OrientationReport output contract
│   ├── generator.py                evidence-bound report generation
│   └── memory.py                   episodes, retrieval, append-only storage
├── README.md                       package scope and entry point
└── docs/
    ├── CORE_V07_REFERENCE.md       historical v0.7 behavior reference
    ├── VALIDATION_STRATEGY.md      validation notes
    └── archive/                    historical status and building logs
```

## Orientation Layer

The contract layer is implemented under `nexah/orientation/`. It defines
context, goals, constraints, provenance, evidence, uncertainty,
`OrientationState`, and `OrientationReport`. `nexah/backends/v07.py` now wraps
the frozen baseline and translates its output without silently assigning
broader semantics: state IDs remain local, index alignment is explicit, and
uncertainty is reported as unknown rather than invented. Report generation
is implemented by `OrientationReportGenerator`; it reports local position,
representation-level change, empirical graph reachability, missing information,
assumptions, evidence, and uncertainty. Demonstrator validation, episodic
storage, and retrieval are now implemented as a transparent initial loop:
outcomes remain externally observed, similarity is explicitly heuristic, and
retrieval never mutates the backend. Decision support and execution remain later
work.

The first three-family memory benchmark is recorded under
`validation/memory_generalization/`: 11 of 12 synthetic clean, noisy, and
parameter-shifted queries retrieve the expected family, with a documented
Kuramoto-to-Lorenz confusion under parameter shift.

See the **[Orientation Layer Bauplan](../ARCHITECTURE/orientation_layer/)**.

## Version note

Package metadata, the public module version, and CLI documentation use `0.7.0`.
Historical reports retain their original labels. See
**[BASELINE_STATUS.md](docs/BASELINE_STATUS.md)** for the characterized behavior,
test boundary, and known limitations of this freeze.
