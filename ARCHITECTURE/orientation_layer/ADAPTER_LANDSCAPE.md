# Adapter Landscape

Status: audited; Phase III source boundary implemented

This inventory preserves earlier adapter work without treating every historical
interface as part of the new Orientation Layer. Existing adapters remain in
place until a specific migration is justified.

## Existing lines

| Line | Translation | Current condition | Future role |
|---|---|---|---|
| Graph adapter family | External or illustrative system → finite state graph | Active demo runs | Candidate `LegacyGraphBackendAdapter` |
| `LorenzAdapter` | Simulated trajectory → sampled temporal graph and heuristic regimes | Runnable; strongest current adapter example | Integration demonstrator |
| Static domain adapters | Conceptual domain model → hand-authored state graph | Runnable; illustrative rather than empirically derived | Report and UI fixtures |
| `PhaseSpaceAdapter` | NEXAH pipeline signatures → state graph | Import path is currently broken | Reconstruct later as a typed signature adapter |
| `base_adapter_vii` | Simulator environment → observations, risk, actions, reward | Importable but unused and incompatible with graph interface | Possible later execution/environment layer |
| IEEE topology adapter | Pandapower network → topology plus predefined regime graph | Importable; graph regimes are partly hand-authored | Domain graph adapter after validation |
| IEEE metric mapping | Electrical arrays → NEXAH-style summary metrics | Experimental function | Feature backend candidate |
| IEEE physical adapter | IEEE case and load scale → physical signal arrays | Importable when pandapower is available | Domain source adapter |
| Experimental bridges | Research object → research object | Numerous historical, task-specific scripts | Research history; review individually |

## Verified audit observations

- `python -m APPLICATIONS.adapters.run_adapter_demo` completes for Lorenz,
  Kuramoto, Power Grid, Supply Chain, and Traffic.
- `python -m APPLICATIONS.navigation.run_navigation_demo` completes, although
  several illustrative graphs settle into simple two-state loops.
- `PhaseSpaceAdapter` currently fails to import because it references
  `analysis.signature_to_graph` rather than its repository location.
- `EnergyGridAdapter` currently fails package import because it imports
  `base_adapter` as a top-level module.
- `base_adapter_vii` has no detected subclasses or active imports.
- The IEEE files called “adapter” perform three different jobs: source
  extraction, feature mapping, and graph construction.

## Architecture decision

Adapter roles are separated from now on:

```text
Source adapter
  domain system → observations

Representation backend adapter
  observations or backend output → scoped representation

Orientation backend adapter
  scoped representation + provenance → OrientationState

Execution adapter (later)
  authorized decision → external action
```

`APPLICATIONS/adapters/` remains the domain and legacy graph area.
`nexah/backends/` contains typed computational backend adapters for the current
package contracts.

`nexah/sources/` now contains the Phase III source contract and two strict
reference implementations. `ArraySourceAdapter` translates finite ordered
numeric observations into a serializable `SourceBatch`. `TableSourceAdapter`
adds explicit DataFrame column, unit, and timestamp selection while excluding
undeclared columns. Neither performs regime, graph, navigation, risk, or action
inference.

## Phase III disposition

| Existing line | Disposition | Reason |
|---|---|---|
| `LorenzAdapter` and graph demos | Preserve as legacy integration fixtures | They simulate and construct graphs rather than only ingesting data |
| Static domain graph adapters | Preserve as UI/report fixtures | Their states are authored examples, not observed source batches |
| `PhaseSpaceAdapter` | Defer reconstruction | Broken import and representation-specific responsibility |
| `base_adapter_vii` | Defer to execution phase | Environment actions and rewards exceed source scope |
| IEEE physical adapter | Reimplemented behind the coupled source contract | Raw bus/line physics retained; fabricated collapse arrays and heuristic loops removed |
| IEEE topology/regime adapters | Domain representation candidates | They mix physical topology with predefined states or regimes |
| CSV-reading research scripts | Feed through `TableSourceAdapter` case by case | The generic schema now exists; individual datasets still need declared columns and provenance |

The implemented contract is specified in
**[SOURCE_ADAPTER_CONTRACT.md](SOURCE_ADAPTER_CONTRACT.md)**.

The existing IEEE physical function returns one row per bus. That is an entity
snapshot, not a temporal trajectory. `IEEEPandapowerAdapter` now records bus and
line snapshots with the entity axis and couples them to an explicitly ordered
load-scale campaign. Only the campaign view is eligible for the first v0.7
integration. See **[IEEE_COUPLED_ADAPTER.md](IEEE_COUPLED_ADAPTER.md)**.

## Preservation rules

1. Existing adapter code is not moved or renamed during WP2.
2. Existing outputs are not presented as `OrientationState` without an explicit
   typed translation.
3. Good ideas may be reconstructed behind current contracts; old classes are
   not copied wholesale into the package.
4. Heuristic regimes, risk labels, and actions retain their provenance and must
   not be promoted to validated facts.
5. The first current backend is `V07BackendAdapter`. Legacy graph and
   Demonstrator adapters are separate later decisions.
