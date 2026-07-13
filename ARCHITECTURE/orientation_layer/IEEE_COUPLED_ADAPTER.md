# IEEE / Pandapower Coupled Source Adapter

Status: C–F implemented, tested, and canonically validated

The adapter implements one physical simulation source with two explicitly
different views. It does not treat bus identity as time and does not assign
NEXAH regimes, risk labels, navigation targets, or actions.

## C — Coupled observation

```text
pandapower IEEE case + ordered load scales
→ independent Newton–Raphson power flows
→ IEEEPhysicalSnapshot[]
   ├── bus SourceBatch   [row_axis = entity]
   └── line SourceBatch  [row_axis = entity]
→ campaign SourceBatch  [row_axis = ordered_sample]
→ IEEECoupledCampaign
```

Every load scale starts from a fresh standard case. The campaign therefore
describes an ordered parameter sweep, not physical time evolution and not a
path-dependent dynamic simulation.

## Physical entity views

Bus features:

| Feature | Unit |
|---|---|
| `vm_pu` | pu |
| `va_degree` | degree |
| `p_mw` | MW |
| `q_mvar` | MVAr |

Line features:

| Feature | Unit |
|---|---|
| `loading_percent` | percent |
| `p_from_mw` | MW |
| `q_from_mvar` | MVAr |

Rows carry stable IDs such as `bus:0` and `line:0:0-3`. These snapshots support
later spatial attribution. They are not passed directly to a temporal backend.

## Ordered campaign view

Each converged scenario produces one transparent summary row:

- load scale
- minimum and mean bus voltage
- bus-voltage standard deviation
- bus-angle range
- maximum line loading
- total bus active and reactive consumption

These are declared physical summaries, not learned features or stability
classes. The axis is `ordered_sample` because load scale is ordered but is not a
timestamp.

## Non-convergence policy

A failed power flow produces a failed `IEEEPhysicalSnapshot` with its exception
description and no bus or line batch. Fabricated collapse arrays are forbidden.
Failed scenarios are excluded from the rectangular numeric campaign and the
exclusion count is recorded in `SourceQuality.transformations`. A campaign in
which no scenario converges fails entirely.

## Supported cases

- IEEE 9-bus
- IEEE 14-bus
- IEEE 30-bus
- IEEE 57-bus
- IEEE 118-bus
- IEEE 300-bus
- PEGASE 1354-bus
- PEGASE 9241-bus

Pandapower is loaded lazily and remains an explicit optional runtime dependency
of this adapter line.

## Evidence

`tests/sources/test_ieee_pandapower_adapter.py` verifies:

- coupled entity and ordered views
- physical dimensions, units, row IDs, context, and provenance
- exclusion of regime, risk, and historical loop heuristics
- JSON round-trip behavior
- invalid campaign axes and unsupported cases
- the prohibition against physical arrays on failed snapshots

## D–F roadmap

### D — Orientation run

Feed only the ordered campaign view into v0.7, with its load-scale interpretation
made explicit. Establish a reproducible IEEE Orientation Report without calling
the sweep a temporal trajectory.

### E — Entity attribution

Map campaign changes back to the corresponding bus and line snapshots. Report
which physical entities changed, without claiming causality from co-occurrence.

### F — Domain validation

Compare NEXAH outputs against preregistered physical references: convergence,
voltage limits, line loading, load scale, and existing repository experiments.
Validation must be separated by case and held-out campaign; it must not tune on
the final benchmark cases.

Canonical V1 is recorded under
**[validation/ieee_orientation_v1/](../../validation/ieee_orientation_v1/)**.
IEEE-9 covers both observed physical threshold crossings within one load step;
held-out IEEE-14 misses its voltage crossing under the same fixed tolerance.
Entity salience attribution matches 11 of 12 checks. This closes the first D–F
path without establishing dynamic prediction or causality.

## Scaling-pattern reconstruction

The historical curvature hypothesis has been reconstructed across eight network
sizes under **[validation/ieee_scaling_pattern_v1/](../../validation/ieee_scaling_pattern_v1/)**.
Boundary acceleration is observable through PEGASE-1354, but the apparent
constant lead is derivative-edge and resolution sensitive. IEEE-300 and
PEGASE-9241 fail at the global lower scan bound and remain untested under this
design. The repository must not describe the V1 result as a validated universal
precursor.
