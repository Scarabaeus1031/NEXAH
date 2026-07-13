# Adapter Ecosystem V3 — Repository Audit and Promotion Map

Status: typed source foundation expanded; legacy and experimental lines audited

## Current typed source boundary

| Source | Current implementation | Row meaning | Validated scope |
|---|---|---|---|
| Numeric array | `ArraySourceAdapter` | ordered sample, time, entity, or event | finite declared numeric observations |
| Table | `TableSourceAdapter` | ordered sample or time | explicit columns, units, and timestamps |
| Directed graph | `GraphSourceAdapter` | entity | declared nodes and directed adjacency only |
| IEEE/Pandapower | `IEEEPandapowerAdapter` | entity snapshots plus ordered campaign | physical bus/line views and load branches |

The graph adapter is the first V3 ecosystem extension after the Phase III gate.
It consumes the shared `nodes`/`edges` structure already present in:

- `APPLICATIONS/datasets/supply_chain.json`
- `APPLICATIONS/datasets/ecosystem_food_web.json`

Regimes, collapse labels, risk targets, actions, and shock names in those files
are excluded from the source matrix. They are authored scenario metadata, not
observed evidence.

## Preserved repository preparation

### Legacy graph adapters

`APPLICATIONS/adapters/` contains runnable illustrative adapters for Lorenz,
Kuramoto, Power Grid, Supply Chain, and Traffic. They helped establish the
cross-domain graph idea. Most mix source structure with authored regimes,
risks, or actions and therefore remain fixtures rather than current source
adapters.

### Phase-space bridge

`PhaseSpaceAdapter` captures an important representation-bridge idea, but its
import path is broken and its job is representation construction rather than
source ingestion. Reconstruct it later behind a typed graph backend contract;
do not copy the old class into `nexah/sources/`.

### BTC result

`outputs/archive/root_cleanup/btc_result.json` and the archived v0.7 status
report preserve evidence that a BTC-USD series was analyzed historically. The
repository no longer contains the versioned raw series, acquisition record, or
executable validation harness needed to reproduce that claim. Treat BTC as a
candidate future table-source case, not current validation evidence.

### Supply-chain and coupled-system experiments

The repository contains:

- hand-authored supply-chain state graphs;
- a deterministic coupled-system experiment linking climate, energy, and
  supply-chain states; and
- an ARCHY geographic supply-network simulation.

These are useful design fixtures. The coupled engine uses authored transition
and coupling rules. The ARCHY model includes unseeded random parameters and is
not calibrated against observed supply-chain data. Neither is external ground
truth.

### Discovery Engine

`EXPERIMENTAL/BUILDER_LAB/DISCOVERY_ENGINE/` is a substantial experimental
lineage for phase spaces, resilience landscapes, transition detection,
architecture search, and symbolic-law exploration. Its own README correctly
classifies it as the historical exploration phase rather than the operational
core. Reuse individual methods only after a claim-specific audit; do not
promote “universal law” or control modules by directory name.

## Promotion map

| Existing asset | V3 disposition | Required next evidence |
|---|---|---|
| Supply-chain topology JSON | Typed graph source fixture | graph representation backend; observed event sequence |
| Ecosystem food-web JSON | Typed graph source fixture | empirical topology/provenance; dynamic observations |
| Legacy Lorenz adapter | Preserve as integration history | current contracts already use the stronger Demonstrator path |
| BTC result JSON | Preserve as historical output | raw versioned data, acquisition provenance, frozen evaluation |
| ARCHY supply simulation | Experimental generator | seed control, headless output contract, calibration boundary |
| Coupled-system engine | Authored scenario generator | repair pathing, typed events, explicit rule provenance |
| PhaseSpaceAdapter | Representation concept | typed graph backend and tests |
| Discovery Engine | Research archive / method inventory | method-by-method reconstruction and validation |

## Next executable plateau

```text
GraphSourceAdapter
→ typed graph representation backend
→ OrientationState without temporal reinterpretation
→ illustrative supply-chain report
→ observed event or topology dataset
→ held-out domain validation
```

The current graph batch must not be passed silently into the temporal v0.7
backend. Its rows are entities, not time steps. The next bridge must preserve
that distinction and derive graph semantics explicitly.
