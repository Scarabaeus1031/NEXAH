# Source Adapter Contract

Status: Phase III contract implemented

Source adapters define the boundary between an independent data source and a
NEXAH representation backend. They transport observations and declared source
semantics. They do not detect regimes, construct maps, select actions, or assign
scientific meaning to results.

## Flow and ownership

```text
independent source
→ SourceAdapter
→ SourceBatch
→ representation backend
→ OrientationState
```

The implementations are under `nexah/sources/`. `ArraySourceAdapter` provides
the minimal reference path for finite NumPy-compatible trajectories.
`TableSourceAdapter` selects explicitly declared DataFrame columns through a
serializable `TableSchema`; undeclared columns do not enter the batch.

## `SourceBatch`

A batch contains:

- a stable batch ID
- an ordered, rectangular numeric matrix
- an explicit row axis: ordered sample, time, entity, or event
- ordered and unique feature declarations
- optional physical units
- optional strictly increasing timezone-aware timestamps
- explicit domain context
- mandatory provenance
- observed adapter-boundary quality facts
- a schema version

It is JSON-round-trippable. `to_numpy()` returns a detached matrix for a
computational backend; mutating that matrix cannot mutate the batch.

## Required invariants

The current strict reference policy rejects:

- empty, non-numeric, or higher-dimensional sources
- missing, NaN, or infinite values
- duplicate or dimensionally inconsistent feature names
- unit vectors that do not match source width
- timestamp vectors that do not match row count
- timestamps attached to any axis other than time
- naive, duplicate, or decreasing timestamps
- quality records inconsistent with the emitted rows

Later adapters may implement an explicit missing-data policy, but every
imputation, deletion, aggregation, or resampling step must be recorded as a
transformation. Silent cleaning is prohibited.

## Separation from other adapter roles

| Role | Input | Output | May analyze? | Phase |
|---|---|---|---:|---|
| Source adapter | External source | `SourceBatch` | No | III |
| Representation backend | Numeric observations | Backend structure | Yes, within declared method | Existing / III |
| Orientation backend adapter | Backend structure | `OrientationState` | Translation only | Existing |
| Execution adapter | Authorized action | External effect | Not part of orientation | Later |

Historical classes that construct graphs or expose actions are not source
adapters merely because their filename contains “adapter”.

The row axis is a semantic compatibility boundary. A bus-indexed snapshot
(`entity`) must not be passed silently to a backend expecting a temporal or
ordered trajectory. An adapter or backend bridge must reject that mismatch or
declare the transformation explicitly.

## Leakage boundary

Context and metadata must describe the source and acquisition conditions. An
adapter must not include the expected class, benchmark answer, desired action,
or evaluation result in any field used by representation, similarity, or
selection. Domain labels used only for stratified evaluation must remain in the
validation harness.

## Acceptance evidence

`tests/sources/test_array_source_adapter.py` verifies:

- value, feature, unit, context, and provenance preservation
- explicit one-dimensional expansion
- JSON round-trip behavior
- visible numeric, shape, semantic, and temporal failures
- a complete `SourceBatch → V07BackendAdapter → OrientationState` path

`tests/sources/test_table_source_adapter.py` additionally verifies explicit
column order, units and timestamps, exclusion of undeclared evaluation labels,
and visible schema, numeric, and temporal failures.

## Next adapter

The generic array and table boundaries are now validated. The next candidate is
the IEEE/pandapower source adapter. It must emit the same `SourceBatch` contract
and document its selected physical variables, units, load-case construction,
optional dependency, and failure behavior. Power-system assumptions must remain
identifiable rather than becoming implicit core behavior.
