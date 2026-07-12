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
├── README.md                       package scope and entry point
└── docs/
    ├── CORE_V07_REFERENCE.md       historical v0.7 behavior reference
    ├── VALIDATION_STRATEGY.md      validation notes
    └── archive/                    historical status and building logs
```

## Orientation Layer

The planned layer will wrap this backend through explicit typed contracts. It
will add context, goals, constraints, provenance, evidence, uncertainty,
orientation reports, and later episodic memory. The backend remains a
characterized baseline rather than silently acquiring broader semantics.

See the **[Orientation Layer Bauplan](../ARCHITECTURE/orientation_layer/)**.

## Version note

Package metadata, the public module version, and CLI documentation use `0.7.0`.
Historical reports retain their original labels. See
**[BASELINE_STATUS.md](docs/BASELINE_STATUS.md)** for the characterized behavior,
test boundary, and known limitations of this freeze.
